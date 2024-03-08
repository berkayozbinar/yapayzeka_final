import tkinter as Tk
from tkinter import ttk
import matplotlib.pyplot as Plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
# from DataSet import all_problems
from Packer import RectanglePacker
from Node import Rect

sortTypes = {"width" : 0, "height" : 1, "max" : 2, "area" : 3}

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Rectangle Fitting App")

        self.widthLabel = ttk.Label(root, text = "Width : ")
        self.widthLabel.grid(row = 0, column = 0, padx = 10, pady = 10)

        self.widthEntry = ttk.Entry(root)
        self.widthEntry.grid(row = 0, column = 1, padx = 10, pady = 10)

        self.heightLabel = ttk.Label(root, text = "Height : ")
        self.heightLabel.grid(row = 1, column = 0, padx = 10, pady = 10)

        self.heightEntry = ttk.Entry(root)
        self.heightEntry.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.addButton = ttk.Button(root, text = "Add Rectangle", command = self.addRectangle)
        self.addButton.grid(row = 3, column = 0, columnspan = 2, pady = 10)

        self.startButton = ttk.Button(root, text = "Start", command = self.startAlgorithm)
        self.startButton.grid(row = 4, column = 0, columnspan = 2, pady = 10)

        self.rectangles = []

    def addRectangle(self):
        width = int(self.widthEntry.get())
        height = int(self.heightEntry.get())
        self.rectangles.append((width, height))
        print("Added Rectangle : ", (width, height))

    def startAlgorithm(self):
        p = RectanglePacker(20, 20)
        rects = [Rect(d) for d in self.rectangles]
        rects = p.fit(rects)
        self.plot(rects)

    def plot(self, rects):
        fig, ax = Plt.subplots(figsize = (7, 7))
        ax.set_xlim([0, rects[0].fit.w])
        ax.set_ylim([0, rects[0].fit.h])

        Plt.locator_params(axis = "both", integer = True, tight = True)
        
        for r in rects:
            if not r.fit:
                continue
            self.drawRect(ax, r)

        Plt.title("Rectangle Fitting Algorithm - 20x20")

        canvas = FigureCanvasTkAgg(fig, master = self.root)
        canvasWidget = canvas.get_tk_widget()
        canvasWidget.grid(row = 5, column = 0, columnspan = 2, pady = 10)

    def drawRect(self, ax, rect : Rect) -> None:
        box = Rectangle(rect.fit.origin, rect.w, rect.h, fc = 'lightblue', ec = 'black', alpha = 1.0)
        ax.add_patch(box)

    def sort(self, rects, sortAttribute = "width"):
        if sortAttribute == 'none':
            return rects

        attribute = [r + (max(r), r[0] * r[1]) for r in rects]
        sortAttributeIndex = sortTypes.get(sortAttribute, 0)

        attribute.sort(key = lambda x : x[sortAttributeIndex], reverse = True)

        return [x[:2] for x in attribute]

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()