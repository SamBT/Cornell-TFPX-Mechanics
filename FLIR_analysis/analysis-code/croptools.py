import numpy as np
import numpy.ma as ma
import heapq
import os

import matplotlib.pyplot as plt
from matplotlib.widgets import LassoSelector
from matplotlib.widgets import PolygonSelector
from matplotlib.widgets import Button
from matplotlib.path import Path

class SelectUtils(object):

    def __init__(self, ax, grid, csv, image, regions=[], labels=[], fracs=[]):
        self.canvas = ax.figure.canvas
        self.grid = grid
        self.csv = csv
        self.ax = ax
        self.image = image
        self.tool = LassoSelector(ax, onselect=self.onselect)
        self.ind = []
        self.selection = []
        self.region = []

        self.saved_regions = regions
        self.saved_labels = labels
        self.saved_fractions = fracs
        self.saved_max = []
        self.saved_min = []
        self.saved_avg = []
        self.saved_maxavg = []
        self.saved_pixcount = []

    def onselect(self, verts):
        print("selected!")
        reg = Path(verts)
        self.ind = reg.contains_points(self.grid, radius=1)
        mask = ~self.ind
        alpha = (0.6+ma.masked_array(np.zeros_like(self.csv)+0.4,mask=mask)).data
        self.selection = ma.masked_array(self.csv,mask=mask)
        self.region = reg
        self.image.set_alpha(alpha)
        self.canvas.draw_idle()

    def lasso_select(self,event):
        self.disconnect()
        self.tool = LassoSelector(self.ax, onselect=self.onselect)
        self.canvas.draw_idle()

    def poly_select(self,event):
        self.disconnect()
        self.tool = PolygonSelector(self.ax, onselect=self.onselect,markerprops={'markersize':3})
        self.canvas.draw_idle()

    def disconnect(self):
        self.tool.disconnect_events()
        self.canvas.draw_idle()

    def reset(self,event):
        self.disconnect()
        self.image.set_alpha(np.ones_like(self.csv))
        self.canvas.draw_idle()

    def clear_polygons(self,event):
        self.disconnect()
        self.ax.clear()
        self.image = self.ax.imshow(self.csv,cmap='plasma',vmin=self.csv.min(),vmax=self.csv.max(),interpolation='none')
        self.ax.set_title("Press enter to accept selected points.")
        self.canvas.draw_idle()

    def save_selection(self,event):
        if event.key == "enter":
            label = input("Label for this region: ")
            frac = float(input("Area fraction: "))
            max = np.max(self.selection)
            min = np.min(self.selection)
            avg = np.average(self.selection)
            avg_10max = np.average(heapq.nlargest(10,self.selection.compressed()))

            self.saved_regions.append(self.region)
            self.saved_labels.append(label)
            self.saved_fractions.append(frac)
            self.saved_max.append(max)
            self.saved_min.append(min)
            self.saved_avg.append(avg)
            self.saved_maxavg.append(avg_10max)
            self.saved_pixcount.append(self.selection.compressed().size)

    def refresh_results(self):
        #Used when paths are imported from prior image and results need to be re-calculated for the new image
        for reg in self.saved_regions:
            self.ind = reg.contains_points(self.grid, radius=1)
            mask = ~self.ind
            self.selection = ma.masked_array(self.csv,mask=mask)

            max = np.max(self.selection)
            min = np.min(self.selection)
            avg = np.average(self.selection)
            avg_10max = np.average(heapq.nlargest(10,self.selection.compressed()))
            self.saved_max.append(max)
            self.saved_min.append(min)
            self.saved_avg.append(avg)
            self.saved_maxavg.append(avg_10max)
            self.saved_pixcount.append(self.selection.compressed().size)

    def write(self,fname,volt,curr):
        output = open(fname,"a")
        if os.stat(fname).st_size == 0:
            output.write("Region,Max T,Avg Max T (10 largest),Min T,Avg T,Voltage,Current,Power,Area Fraction,Pixel Count\n")
        for i, label in enumerate(self.saved_labels):
            output.write("%s,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%i\n" % (label,self.saved_max[i],self.saved_maxavg[i],self.saved_min[i],self.saved_avg[i],volt,curr,volt*curr,self.saved_fractions[i],self.saved_pixcount[i]))
        output.close()

def manualcrop(filelist, dirname):
    selector = 0
    print("---------------------------------------------------------")
    for file in filelist:
        fig, ax = plt.subplots()

        fname = file.split("/")[-1].split(".")[0]
        print("File: "+fname)
        current = float(input("Current: "))
        voltage = float(input("Voltage: "))

        csv = np.genfromtxt(file, delimiter=',')
        alph = np.ones_like(csv)
        image = ax.imshow(csv,cmap='plasma',vmin=csv.min(),vmax=csv.max(),alpha=alph,interpolation='none')
        x, y = np.meshgrid(np.arange(csv.shape[1]), np.arange(csv.shape[0]))
        grid = np.vstack((x.flatten(), y.flatten())).T

        if selector != 0 and input("Use same regions as previous image? [y/n] : ") == "y":
            selector = SelectUtils(ax,grid,csv,image,regions=selector.saved_regions,labels=selector.saved_labels,fracs=selector.saved_fractions)
            selector.refresh_results()
            selector.write(dirname+"/selections_"+fname,voltage,current)
        else:
            selector = SelectUtils(ax, grid, csv, image)

            fig.canvas.mpl_connect("key_press_event", selector.save_selection)
            ax.set_title("Press enter to accept selected points.")

            axlas = plt.axes([0.52, 0.005, 0.15, 0.05])
            axpoly = plt.axes([0.68, 0.005, 0.15, 0.05])
            axreset = plt.axes([0.36,0.005,0.15,0.05])
            axclear = plt.axes([0.2,0.005,0.15,0.05])

            blas = Button(axlas, 'Lasso')
            blas.on_clicked(selector.lasso_select)

            bpoly = Button(axpoly, 'Polygon')
            bpoly.on_clicked(selector.poly_select)

            breset = Button(axreset,'Reset')
            breset.on_clicked(selector.reset)

            bclear = Button(axclear,'Clear Polys.')
            bclear.on_clicked(selector.clear_polygons)

            plt.show()
            selector.write(dirname+"/selections_"+fname+".csv",voltage,current)
        print("Finished processing file "+fname)
        print("---------------------------------------------------------")
    print("All files processed")

# Function that picks out the relevant files in a directory
def selectfiles(filelist):
    for i,f in enumerate(filelist):
        print(str(i+1)+": "+f)
    yn = input("Would you like to remove any? [y/n]: ");
    if (yn == "y"):
        remove = []
        out = input("Which ones? (comma separated list of numbers): ")
        for num in out.split(","):
            remove.append(filelist[int(num)-1])
        for el in remove:
            filelist.remove(el)
    print("New List:")
    for i,f in enumerate(filelist):
        print(str(i+1)+": "+f)
    ind = int(input("Which one do you want to process first? (number) : "))-1
    filelist.insert(0,filelist.pop(ind))
    return filelist
