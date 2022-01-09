import numpy as np
from matplotlib import pyplot as plt
import os
from sides import *
from math import *

# lots of parts of code taken from my previous PYECS project
# available at https://github.com/jubiiz/pyecs

class GridCreator():
    def __init__(self, sides_file, size):
        self.press = None

        # initiates sides
        self.size = size
        self.vector_convert = {(1, 0): 1, (-1, 0): 3, (0, 1): 2, (0, -1): 0} # translation table between a vector linking 2 cells and which side of cell1 it affects
        self.sides_file = sides_file
        self.sides = sides_from_file(sides_file)


    def connect(self):
        """connects the event functions then displays the graph"""
        self.cidpress = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cidrelease = self.fig.canvas.mpl_connect('button_release_event', self.onrelease)                   
    
    def show_grid(self):
        fig, ax = plt.subplots()
        self.fig = fig
        self.ax = ax
        ax.set_xlim(left=0, right=self.size[1])
        ax.set_ylim(bottom=0, top=self.size[0])
        ax.invert_yaxis()
        minor_ticks = np.linspace(0, self.size[0], self.size[0]+1)
        ax.set_xticks(minor_ticks)
        ax.set_yticks(minor_ticks)
        ax.grid(True)
        self.connect()
        for y_coord in range(len(self.sides)):
            row = self.sides[y_coord]
            for x_coord in range(len(row)):
                cell = self.sides[y_coord][x_coord]
            
                # displaying that cell's sides
                for i in range(4): # squares have 4 sides. That doesn't change.
                    side = cell[i]
                    if side == 1:
                        axis = (i)%2 # 1 for x, 0 for y (matrices order)
                        pos = (((i+1)//2)%2) # 0 or 1: shifts the wall to either extremities |_|
                        side_x = [x_coord, x_coord]
                        side_y = [y_coord, y_coord]
                        if axis == 0: # top/bot wall: on the x axis
                            side_x[1] += 1
                            side_y[0] += pos
                            side_y[1] += pos
                        else:
                            side_y[1] += 1
                            side_x[0] += pos
                            side_x[1] += pos
                        self.ax.plot(side_x, side_y, "k")
        print("modify here")
        plt.show()

    def onclick(self, event):
        "When there is a click in the axes, log info for the current point"
        if event.inaxes != None:
            self.press = ((event.x, event.y), (event.xdata, event.ydata))
            self.press_case = (floor(event.xdata), floor(event.ydata))#find this
            
    def onrelease(self, event):
        # need to 1) check if the click is happening in the same cell, if so, do nothing
        # if not same cell, take the two cell coordinates ()
        # at the end reset the self.press
        new_case = (floor(event.xdata), floor(event.ydata))
        print(new_case)
        # not same case
        if new_case != self.press_case:
            # switch presence of wall between cellx and celly
            cell1 = self.press_case
            cell2 = new_case
            v = (cell2[0]-cell1[0], cell2[1]-cell1[1])
            v_opp = (cell1[0]-cell2[0], cell1[1]-cell2[1])

            sides1 = self.sides[cell1[1]][cell1[0]]
            sides2 = self.sides[cell2[1]][cell2[0]]
            print("cells: ", cell1, cell2)
            print("initial sides: ", sides1, sides2)
            print("vectors: ", v, v_opp)


            # reverse the side at the desired location (0->1; 1->0)
            sides1[self.vector_convert[v]] = int(not(int(sides1[self.vector_convert[v]])))
            sides2[self.vector_convert[v_opp]] = int(not(int(sides2[self.vector_convert[v_opp]])))

            print("new sides: ", sides1, sides2)

        # ready for new press (delete past data, show new graph)
        self.press_case = None
        self.press = None  
        plt.close("all") 
        self.show_grid()
        
    def update_file(self):
        with open(f"sides/{self.sides_file}_corrected.txt", "w") as w:         

            for row in self.sides: 
                cursor = 0
                for cell in row:
                    for side in cell:
                            w.write(str(side))
                    w.write(" ")
                    cursor += 1
                    if cursor%self.size[1] == 0:
                        w.write("\n")
        print("updated")
                    

    def disconnect(self):
        """disconnects the connections"""
        self.fig.canvas.mpl_disconnect(self.cidpress)
        self.fig.canvas.mpl_disconnect(self.cidrelease)

def main():
    g = GridCreator("p6", (5, 5))
    g.show_grid()
    input("please modify the sides by dragging from cell to cell")
    g.update_file()

if __name__ == "__main__":
    main()
