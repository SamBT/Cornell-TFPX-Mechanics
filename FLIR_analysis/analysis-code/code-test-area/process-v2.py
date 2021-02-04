# This file does the cropping, and only the cropping, on all the good csv files in a directory. You're expected to run w4 on both cropped and uncropped as needed.
# Cropping is done manually.

import os
import glob
import numpy as np
import heapq
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
from sys import exit
import croptools

# Execution
if len(sys.argv) < 2:
    print("Please supply a directory name and re-run the script")
    exit()

filelist = [f for f in sorted(glob.glob('./data/*.csv')) if (not 'FLIR.csv' in f)]
filelist = croptools.selectfiles(filelist)

if os.path.isdir(sys.argv[1]):
    if input("A directory with that name already exists. Do you want to add more regions to the files in this folder?[y/n]: ") == "y":
        for i, csvfile in enumerate(filelist):
            croptools.manualcrop(csvfile,sys.argv[1])
    else:
        exit()
else:
    os.mkdir(sys.argv[1])
    croptools.manualcrop(filelist,sys.argv[1])

print('Image processing completed')
