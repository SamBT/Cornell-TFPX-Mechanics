import os
import numpy as np
import heapq
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
import sys
from sys import exit

def plotter(filelist,outputdir):
    temp_diffs = {}
    powers = {}
    fractions = {}

    df = pd.read_csv(filelist[0])
    for reg in df['Region']:
        powers[reg] = []
        temp_diffs[reg] = []
        fractions[reg] = float(df.loc[df['Region'] == reg]['Pixel Count'])/float(df.loc[df['Region'] == 'main']['Pixel Count'])
    regions = list(powers.keys())

    for f in filelist:
        df = pd.read_csv(f)
        for reg in regions:
            powers[reg].append(float(df.loc[df['Region'] == reg]['Power']))
            temp_diffs[reg].append(float(df.loc[df['Region'] == reg]['Avg T']))
    plt.figure()
    for reg in regions:
        pows = fractions[reg]*np.array(powers[reg])
        dTs = np.array(temp_diffs[reg])
        data = plt.plot(pows,dTs,"o",label=reg)
        x_for_fit = pows[pows/fractions[reg] > 1]
        y_for_fit = dTs[pows/fractions[reg] > 1]
        coeffs = np.polyfit(x_for_fit,y_for_fit,1)
        x_fit = np.linspace(np.min(pows),np.max(pows),num=50)
        plt.plot(x_fit,coeffs[0]*x_fit + coeffs[1],"--",color=data[0].get_color(),label="y = {0:.3f}x + {1:.3f}".format(coeffs[0],coeffs[1]))
    plt.xlabel("Power (W)",fontsize=16)
    plt.ylabel("Temperature (C)",fontsize=16)
    plt.legend()
    plt.savefig(outputdir+"/temp_vs_power.pdf")

if len(sys.argv) < 3:
    print("Incorrect input format. Correct format is scriptname inputdir outputdir")
    exit()
else:
    if not os.path.isdir(sys.argv[2]):
        os.mkdir(sys.argv[2])
    inputdir = sys.argv[1]
    filelist = sorted(os.listdir(inputdir))
    filelist = [inputdir+f for f in filelist]
    plotter(filelist,sys.argv[2])
