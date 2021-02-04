import os
import glob
import numpy as np
import heapq
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector
import numpy as np
import sys
from sys import exit

def tempvis(csv_file, dirname, cmap='plasma', showortell='show'):
    global glob_cached_paths
    global glob_cached_labels
    csv = np.genfromtxt(csv_file, delimiter=',')
    print("File name: "+csv_file)
    curr = float(input("Current: "))
    volt = float(input("Voltage: "))

    title ='\n Heat map: I = {0:.2f} A, V = {1:.2f} V, P = {2:.2f} W'.format(curr,volt,curr*volt)
    plt.figure()
    plt.imshow(csv,cmap=cmap)
    plt.colorbar()
    plt.title(title)
    plt.savefig(dirname+"/heatmap-"+str(curr)+"A-"+str(volt)+"V"+".pdf")

if len(sys.argv) < 2:
    print("Please supply a directory name and re-run the script")
    exit()

filelist = [f for f in sorted(glob.glob('./data/*.csv')) if ((not 'FLIR' in f) and ('.csv' in f)) ]

if os.path.isdir(sys.argv[1]):
    if input("A directory with that name already exists. Do you want to add more images?[y/n]: ") == "y":
        for i, csvfile in enumerate(filelist):
            tempvis(csvfile,sys.argv[1])
    else:
        exit()
else:
    os.mkdir(sys.argv[1])
    for i, csvfile in enumerate(filelist):
        tempvis(csvfile,sys.argv[1])

print('This script has now completed.')
