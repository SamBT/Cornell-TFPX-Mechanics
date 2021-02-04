import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt

from matplotlib.widgets import LassoSelector
from matplotlib.widgets import PolygonSelector
from matplotlib.widgets import Button
from matplotlib.path import Path

class SelectUtils(object):

    def __init__(self, ax, grid, csv, image):
        self.canvas = ax.figure.canvas
        self.grid = grid
        self.csv = csv
        self.ax = ax
        self.image = image
        self.tool = LassoSelector(ax, onselect=self.onselect)
        self.ind = []
        self.selection = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = path.contains_points(self.grid, radius=1)
        mask = ~self.ind
        alpha = (0.6+ma.masked_array(np.zeros_like(csv)+0.4,mask=mask)).data
        self.selection = ma.masked_array(self.csv,mask=mask)
        self.image.set_alpha(alpha)
        self.canvas.draw_idle()

    def lasso_select(self):
        self.disconnect()
        self.tool = LassoSelector(self.ax, onselect=self.onselect)
        self.canvas.draw_idle()

    def poly_select(self):
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
        ax.imshow(self.csv,cmap='plasma',vmin=self.csv.min(),vmax=self.csv.max(),interpolation='none')
        ax.set_title("Press enter to accept selected points.")
        self.canvas.draw_idle()



if __name__ == '__main__':

    fig, ax = plt.subplots()
    csv = np.genfromtxt('./data/07-16-2020-13-03-17-current-1p4A-voltage-9p1V.csv', delimiter=',')
    alph = np.ones(csv.shape)
    image = ax.imshow(csv,cmap='plasma',vmin=csv.min(),vmax=csv.max(),alpha=alph,interpolation='none')
    x, y = np.meshgrid(np.arange(csv.shape[1]), np.arange(csv.shape[0]))
    grid = np.vstack((x.flatten(), y.flatten())).T
    selector = SelectUtils(ax, grid, csv, image)

    def accept(event):
        if event.key == "enter":
            fig.canvas.draw()


    fig.canvas.mpl_connect("key_press_event", accept)
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
