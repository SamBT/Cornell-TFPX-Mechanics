import random, sys, os
import numpy as np

def intersects(a,B):
    ra, pa = a[0], a[1]
    for b in B:
        rb, pb = b[0], b[1]
        if np.linalg.norm(pa-pb,ord=2) < 0.0*(ra+rb):
            return True
    return False

def n_intersects(a,B):
    n = 0
    ra, pa = a[0], a[1]
    for b in B:
        rb, pb = b[0], b[1]
        if np.linalg.norm(pa-pb,ord=2) < ra+rb:
            n+=1
    return n

def gen_particle(min_size,max_size,L):
    r = np.random.uniform(min_size,max_size)
    pos = np.random.uniform(r,L-r,size=3)
    v = (4/3)*np.pi*(r**3)
    return (r,pos,v)

def intersection(a,b):
    ra, pa = a[0], a[1]
    rb, pb = b[0], b[1]
    if np.linalg.norm(pa-pb,ord=2) < ra+rb:
        return True
    else:
        return False

def vol_intersect(r1,r2,d):
    return np.pi*((r1+r2-d)**2)*(d**2 + 2*d*r1 - 3*r1**2 + 2*d*r2 + 6*r1*r2 - 3*r2**2)/(12*d)

def tot_vol_intersect(parts):
    if len(parts) < 2:
        return 0
    intersect = 0
    for i in range(len(parts)-1):
        for j in range(i+1,len(parts)):
            pi = parts[i]
            pj = parts[j]
            ri = parts[i][0]
            rj = parts[j][0]
            vi = parts[i][1]
            vj = parts[j][1]
            d = np.linalg.norm(vi-vj,ord=2)
            if d < ri+rj:
                intersect += vol_intersect(ri,rj,d)
    return intersect

if len(sys.argv) < 5:
    print("Please input: vol_frac min_radius, max_radius, box_side_length")
    exit()

frac = float(sys.argv[1])
min_size = float(sys.argv[2]) #in microns
max_size = float(sys.argv[3]) #in microns
L = float(sys.argv[4]) #cube side length
print("fraction = "+str(frac))
V = L**3
vol_d = 0 #diamond volume
particle_info = []

while (vol_d-tot_vol_intersect(particle_info))/V < frac-0.01:
    print((vol_d-tot_vol_intersect(particle_info))/V)
    print("array length = "+str(len(particle_info)))
    print("diamond volume = "+str(vol_d))
    print('Intersecting volume = '+str(tot_vol_intersect(particle_info)))
    if len(particle_info) == 0:
        print("starting")
        r, pos, v = gen_particle(min_size,max_size,L)
        particle_info.append([r,pos])
        vol_d += v
    else:
        print("adding")
        r, pos, v = gen_particle(min_size,max_size,L)
        while (vol_d+v-tot_vol_intersect(particle_info+[[r,pos]]))/V >= frac+0.01 or intersects([r,pos],particle_info) or n_intersects([r,pos],particle_info) > 2:
            r, pos, v = gen_particle(min_size,max_size,L)
        particle_info.append([r,pos])
        vol_d += v

intersecting_volume = 0
for i in range(len(particle_info)-1):
    for j in range(i+1,len(particle_info)):
        if intersection(particle_info[i],particle_info[j]):
            ri = particle_info[i][0]
            rj = particle_info[j][0]
            pi = particle_info[i][1]
            pj = particle_info[j][1]
            d = np.linalg.norm(pi-pj,ord=2)
            intersecting_volume += vol_intersect(ri,rj,d)
            print("Particle {0} intersects particle {1} by l = {2:.3f}".format(i+1,j+1,ri+rj-d))

print("Volume Fraction = {0:.3f}".format(vol_d/V))
print("True Volume Fraction = {0:.3f}".format((vol_d-intersecting_volume)/V))

for i, p in enumerate(particle_info):
    print("Particle {0}:".format(i+1))
    print("r = {0:.2f}, (x,y,z) = ({1:.2f},{2:.2f},{3:.2f})".format(p[0],p[1][0],p[1][1],p[1][2]))
    print("---------------------------")
