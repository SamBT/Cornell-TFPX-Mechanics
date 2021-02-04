# This file contains various functions that analyze csv data files, some of which are currently work in progress.

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sys import exit

# functions doing thermal workup of the files
def tempvis(csv_file, tmax, tmin, cmap, dirname):
    """This function converts the csv file into a black-and-white picture. It does not at present
    have a colorbar to indicate the temperature scale."""
    csv = np.genfromtxt(csv_file, delimiter=',')
    title ='\n Heat map of ' + csv_file.split("/")[-1][:-4] + '\n'
    fig, ax = plt.subplots()
    if cmap=='default':
        plt.matshow(csv, interpolation='none', vmin=tmin, vmax=tmax)
    else:
        plt.matshow(csv, interpolation='none', vmin=tmin, vmax=tmax, cmap=cmap)
    #ax.set(xlabel='\ndistance in pixels',ylabel='distance in pixels',title=title)
    plt.title(title);
    plt.colorbar();
    saveas = dirname+'/'+csv_file.split("/")[-1][:-4]+'.pdf'
    plt.savefig(saveas,format='pdf')

# functions that extract the useful information from files
def time(csv_file):
    """This function gets the time from the name of the file."""
    return str(csv_file)[:-4]

def maxminavg(csv_file):
    """This function goes through a .csv file containing a 'rectangle' of numbers, and gives you the
    maximum value, the minimum value and the average value of all these numbers in a tuple. """
    csv_reader = np.genfromtxt(csv_file, delimiter=',')
    maxval = csv_reader[0][0]
    minval = csv_reader[0][0]
    total = 0
    counter = 0
    for row in csv_reader:
        for value in row:
            if maxval < value:
                maxval = value
            if minval > value:
                minval = value
            total = total + value
            counter = counter + 1
    average = total/counter
    return (maxval, minval, average)

# functions that check whether the files are useful in the first place
    # helper function
def isequalto(testfile,reffile):
    """This function takes two csv files and checks if their contents are equal to each other."""
    test_mat = np.genfromtxt(testfile, delimiter=',')
    ref_mat = np.genfromtxt(reffile,delimiter=',')
    if test_mat.shape != ref_mat.shape: # is this how the shape thing works?
        return False
    else:
        (n,m) = test_mat.shape # think this is allowed syntax
        x=0
        y=0
        truthval=1
        while y<m:
            while x<n:
                if test_mat[x][y] != ref_mat[x][y]:
                    truthval=0
                x=x+1
            x=0
            y=y+1
        if truthval==1:
            return True
        else:
            return False

    # worker functions
def isaflir(csv_file):
    """This function is supposed to inform you when your picture displays nothing but the FLIR logo.
    Depends on the presence of the file FLIR.csv"""
    flir = '/Users/sambt/TFPX/FLIR_Pictures_Thermal/FLIR.csv'  # I think this should work, but TEST!
    iet = isequalto(csv_file,flir)
    if iet==True:
        print(str(csv_file)+' is a FLIR.')
    return iet

def checkdoubles(filelist):
    """This function is meant to check for files with the exact same contents for all the files
    within a directory."""
    n = len(filelist)
    count = 0
    cleanlist = []
    cleanlist.append(filelist[0])
    while count < n-1:
        rfl = filelist[count]
        for fl in filelist[count+1:]:
            doub = isequalto(rfl,fl)
            if doub==True:
                print(str(fl)+' is the same as '+str(filelist[count]))
            else:
                if fl not in cleanlist:
                    cleanlist.append(fl)
        count=count+1
    print('No (other) doubles were found.')
    return cleanlist

# Function that picks out the relevant files in a directory
def selectfiles(filelist):
    removelist = []
    for csvfile in filelist:
        if not csvfile.endswith('.csv'):
            removelist.append(csvfile)
        elif csvfile == 'FLIR.csv':
            removelist.append(csvfile)
        elif isaflir(csvfile) == True:
            removelist.append(csvfile)
        else:
            continue
    for badfile in removelist:
        filelist.remove(badfile)
    cdlist = checkdoubles(filelist)
    print(cdlist)
    return cdlist

# Execution

# Check if a results file does not exist already
if os.path.isfile('results.csv') == True:
    print('''Looks like you already have a results.csv file. Please move that somewhere else or rename it
    as a non-.csv before it is overwritten, and then run this script again.''')
    exit()

# Start counters
gatherer = []
times = []

# Do the actual work
data_dir = "./data/"
filelist = sorted(os.listdir(data_dir))
filelist = [data_dir+f for f in filelist]
goodlist = selectfiles(filelist)
for csvfile in goodlist:
        times.append(time(csvfile))
        gatherer.append(maxminavg(csvfile))

# Writing the results to results.csv
results = open('results.csv', 'w')
results.write('time,max,min,avg\n')
counter = 0
maxes = []
mins = []
for t_el in gatherer:
    results.write(times[counter]+','+str(t_el[0]) +','+str(t_el[1])+','+str(t_el[2])+'\n')
    counter = counter +1
    maxes.append(t_el[0])
    mins.append(t_el[1])
results.close()

tmax = max(maxes)
tmin = min(mins)
print("Temperatures vary between "+str(tmin)+" and "+str(tmax)+".")
if os.path.isdir('color') == True:
    print("Seems like you already have a dictionary named color. Please rename it and then run this script again!")
    exit()
else:
    os.mkdir('color')
    for csvfile in goodlist:
            tempvis(csvfile, tmax, tmin, cmap='default', dirname='color') #implement changes in function

if os.path.isdir('b+w') == True:
    print("Seems like you already have a dictionary named b+w. Please rename it and then run this script aga !")
    exit()
else:
    os.mkdir('b+w')
    for csvfile in goodlist:
            tempvis(csvfile, tmax, tmin, cmap=plt.cm.gray, dirname='b+w') #implement changes in function

print('This script has now completed.')
