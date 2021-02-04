# This file does the cropping, and only the cropping, on all the good csv files in a directory. You're expected to run w4 on both cropped and uncropped as needed.
# Cropping is done manually.

import os
import numpy as np
import heapq
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector
import numpy as np
import sys
from sys import exit

glob_cached_paths = []
glob_cached_labels = []
glob_cached_fractions = []

# functions doing thermal workup of the files
def tempvis(csv_file, tmax, tmin, cmap, showortell='show'):
    """This function converts the csv file into a black-and-white picture. It does not at present
    have a colorbar to indicate the temperature scale."""
    global glob_cached_paths
    global glob_cached_labels
    global glob_cached_fractions
    csv = np.genfromtxt(csv_file, delimiter=',')
    title ='\n Heat map of ' + csv_file.split("/")[-1][:-4] + '\n'
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax1.imshow(csv)
    ax1.set(title=title)
    ax2 = fig.add_subplot(122)
    ax2.imshow(np.zeros_like(csv))
    plt.subplots_adjust()
    cached_paths = []
    cached_labels = []
    cached_fractions = []

    x, y = np.meshgrid(np.arange(csv.shape[1]), np.arange(csv.shape[0]))
    pix = np.vstack((x.flatten(), y.flatten())).T
    saved_localmax = [];
    saved_localmaxavg = [];
    saved_localmin = [];
    saved_localavg = [];
    saved_fractions = []

    print("File name: "+csv_file)
    curr = float(input("Current: "))
    volt = float(input("Voltage: "))

    def onselect(verts):
        #Driver for lasso selection on images
        p = Path(verts)
        ind = p.contains_points(pix, radius=1)
        selected = np.zeros_like(csv)
        selected.flat[ind] = csv.flat[ind]
        data = csv.flat[ind]
        ax2.imshow(selected)
        fig.canvas.draw_idle()
        save = input("Save data in selection?[y/n]: ")
        if (save == "y"):
            max = np.amax(data);
            maxavg = np.average(heapq.nlargest(10,data))
            min = np.amin(data);
            avg = np.average(data);
            saved_localmax.append(max)
            saved_localmaxavg.append(maxavg)
            saved_localmin.append(min)
            saved_localavg.append(avg)
            lab = input("Label for this region: ")
            frac = float(input("Approx. area fraction: "))
            cached_paths.append(p);
            cached_labels.append(lab)
            cached_fractions.append(frac)
            saved_fractions.append(frac)

    if (glob_cached_paths and input("Use same regions as last image?[y/n]: ") == "y"):
        for i, p in enumerate(glob_cached_paths):
            ind = p.contains_points(pix,radius=1)
            data = csv.flat[ind]
            max = np.amax(data);
            maxavg = np.average(heapq.nlargest(10,data))
            min = np.amin(data);
            avg = np.average(data);
            saved_localmax.append(max)
            saved_localmaxavg.append(maxavg)
            saved_localmin.append(min)
            saved_localavg.append(avg)
        print("Done with processing")
        print("--------------------------------------")
        return (saved_localmax, saved_localmaxavg, saved_localmin, saved_localavg, glob_cached_labels, volt, curr, glob_cached_fractions)
    else:
        lasso = LassoSelector(ax1, onselect)
        plt.show()
        glob_cached_paths = cached_paths
        glob_cached_labels = cached_labels
        glob_cached_fractions = cached_fractions
        print("Done with processing")
        print("--------------------------------------")
        return (saved_localmax, saved_localmaxavg, saved_localmin, saved_localavg, cached_labels, volt, curr, cached_fractions)

# functions that extract the useful information from files
def maxminavg(csv_file):
    """This function goes through a .csv file containing a 'rectangle' of numbers, and gives you the
    maximum value, the minimum value and the average value of all these numbers in a tuple. """
    csv_reader = np.genfromtxt(csv_file, delimiter=',')
    maxval = np.amax(csv_reader)
    minval = np.amin(csv_reader)
    average = np.average(csv_reader)
    return (maxval, minval, average)

# cropping functions
#def basiccrop(csv_file, xmin, xmax, ymin, ymax, dirname):
def basiccrop(csv_file,max,min,avg,labels,dirname):
    """This function takes some limits and crops the file."""
    #csv = np.genfromtxt(csv_file, delimiter=',')
    #print(csv.shape)
    croppedcsv = csv[ymin:ymax,xmin:xmax]
    filename = dirname+'/'+'cropped_'+csv_file
    np.savetxt(filename,croppedcsv,delimiter=',')
    return filename

def manualcrop(csv_file, dirname):
    """This function shows the user a color picture of the file to be cropped. The user can then manually
    specify what limits he wants to set on the cropping. A cropped csv file is then created, as well as a
    color picture of that file."""
    mma = maxminavg(csv_file)
    (tmax, tmin) = (mma[0],mma[1])
    (max, maxavg, min, avg, labels, volt, curr, fracs) = tempvis(csv_file, tmax, tmin, cmap='plasma', showortell='show')
    filename = dirname+'/'+'cropped_'+csv_file.split("/")[-1]
    output = open(filename,"a")
    if os.stat(filename).st_size == 0:
        output.write("Region,Max T,Avg Max T (10 largest),Min T,Avg T,Voltage,Current,Power,Area Fraction\n")
    for i, label in enumerate(labels):
        output.write("%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f\n" % (label,max[i],maxavg[i],min[i],avg[i],volt,curr,volt*curr,fracs[i]))
    output.close()

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
    flir = data_dir+'FLIR.csv'  # I think this should work, but TEST!
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
    for i,f in enumerate(cdlist):
        print(str(i+1)+": "+f)
    yn = input("Would you like to remove any? [y/n]: ");
    if (yn == "y"):
        remove = []
        out = input("Which ones? (comma separated list of numbers): ")
        for num in out.split(","):
            remove.append(cdlist[int(num)-1])
        for el in remove:
            cdlist.remove(el)
    print("New List:")
    for i,f in enumerate(cdlist):
        print(str(i+1)+": "+f)
    ind = int(input("Which one do you want to process first? (number) : "))-1
    cdlist.insert(0,cdlist.pop(ind))
    return cdlist

# Execution
data_dir = "./data/"
filelist = sorted(os.listdir(data_dir))
filelist = [data_dir+f for f in filelist]
goodlist = selectfiles(filelist)
if len(sys.argv) < 2:
    print("Please supply a directory name and re-run the script")
    exit()
elif os.path.isdir(sys.argv[1]):
    if input("A directory with that name already exists. Do you want to add more regions to the files in this folder?[y/n]: ") == "y":
        for i, csvfile in enumerate(goodlist):
            manualcrop(csvfile,sys.argv[1])
    else:
        exit()
else:
    os.mkdir(sys.argv[1])
    for i, csvfile in enumerate(goodlist):
        manualcrop(csvfile,sys.argv[1])

print('This script has now completed.')
