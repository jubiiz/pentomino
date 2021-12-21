import os
import cv2
import numpy as np
import math
from processor import *
from sides import *
from numext import *
from matplotlib import pyplot as plt

class Cell():
    def __init__(self, value, coordinates, sides):
        self.value = value
        self.coordinates = coordinates
        self.sides = sides

    def find_neighbors_proxi(self, problem_size):
        """
        returns all proximity neighbours (cells around)
        """
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                same_cell = (i==0 and j==0)
                xcoord = self.coordinates[0]+i
                ycoord = self.coordinates[1]+j
                inbounds = 0<=xcoord<problem_size[0] and 0<=ycoord<problem_size[1]
                #checks if 1) not the same cell, 2) cell not out of bounds
                if not same_cell and inbounds:
                    neighbors.append((xcoord, ycoord))
        return(neighbors)

class Grid():
    def __init__(self, sides_file, nums_file):
        """
        from text files containing the numbers and edge types for each square,
        builds an nxn array of cell objects.

        Then builds a list of pentomino from edge information
        """
        self.size = (20, 20)

        # extracts info from text files
        sides_list = sides_from_file(sides_file)
        num_list = nums_from_file(nums_file)

        # builds array of cells
        self.cells = []
        # 1d list of cells for pentomino frontier search
        all_cells = []
        row = []
        for i in range(len(num_list)):
            num_row = num_list[i]
            for j in range(len(num_row)):
                coordinates = (i, j)
                value = num_row[j]
                sides = sides_list[i][j]
                cell = Cell(value, coordinates, sides)
                row.append(cell)
                all_cells.append(cell)
            self.cells.append(row)
            row = []

        # builds list of pentominos
        self.pentominos = []
        while len(all_cells) != 0:
            current = all_cells[0]
            pentomino = self.find_pentomino(current.coordinates)
            self.pentominos.append(pentomino)
            for cell in pentomino:
                try:
                    all_cells.remove(cell)
                except Exception:
                    print(cell.coordinates)

        self.domains = {}
        for pentomino in self.pentominos:
            lp = len(pentomino) # length pentomino
            for cell in pentomino:
                if cell.value == 0:
                    self.domains[cell] = list(range(1, lp+1))
                else:
                    self.domains[cell] = [cell.value]
        print("initialization done")

    def show_grid(self):
        fig, ax = plt.subplots()
        ax.set_xlim(left=0, right=20)
        ax.set_ylim(bottom=0, top=20)
        ax.invert_yaxis()
        minor_ticks = np.linspace(0, self.size[0], self.size[0]+1)
        ax.set_xticks(minor_ticks)
        ax.set_yticks(minor_ticks)
        ax.grid(True)


        for cell in np.reshape(self.cells, self.size[0]*self.size[1]):
            y_coord, x_coord = cell.coordinates
            pad = self.size[0]/100

            # displaying the value of that cell
            if cell.value != 0:
                ax.text(x_coord+pad, y_coord+pad, str(cell.value), {'ha': 'left', 'va': 'top', 'weight':'bold'}, c="red")

            # displaying that cell's sides
            for i in range(4): # squares have 4 sides. That doesn't change.
                side = cell.sides[i]
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
                    ax.plot(side_x, side_y, "k")
                    

        self.fig = fig
        self.ax = ax
        plt.show()

    def neighbors(self, cell):
        neighbors = []
        for p in self.pentominos: 
            # this is the right pentomino:
            # other cells in the same pentomino are neighbors
            if cell in p:
                for other_cell in p:
                    if cell is not other_cell:
                        neighbors.append(other_cell)
        for coords in cell.find_neighbors_proxi(self.size):
            n = self.cells[coords[0]][coords[1]]
            if n not in neighbors:
                neighbors.append(n)
        return(neighbors)

    def is_complete(self, assignment):
        if len(assignment) == len(self.domains):
            return True
        return False
    
    def is_consistent(self, assignment):
        """ 
        return True only if there are no two neighbor cells with a same value
        it doesn't check if a value is higher than supposed to (for a pentomino)
        because it removes unfit values during domain creation
        """ 
        for cell in assignment:
            value = assignment[cell]
            for other_cell in self.neighbors(cell):
                if other_cell in assignment:
                    other_value = assignment[other_cell]
                    if value == other_value:
                        return False
        return(True)

    def select_unassigned_cell(self, assignment):
        """
        selects an unassigned cell
        NEEDS TO BE OPTIMIZED: PRIORITIZE THE LEAST DOMAIN VALUES, THEN HIGHEST DEGREE (MOST NEIGHBORS)
        """
        least_d_vals = math.inf
        highest_degree = 0
        for cell in self.domains:
            if cell not in assignment:
                num_d_vals = len(self.domains[cell])
                if num_d_vals < least_d_vals:
                    best_cell = cell
                    least_d_vals = num_d_vals
                    highest_degree = len(self.neighbors(cell))
                elif num_d_vals == least_d_vals and len(self.neighbors(cell)) > highest_degree:
                    best_cell = cell
                    highest_degree = len(self.neighbors(cell))
        return(best_cell)

    def update_values(self, assignment):
        for cell in assignment:
            cell.value = assignment[cell]

    def solve(self):
        """
        returns a solved version of the suguru else returns False
        """
        # node consistency enforced in domain creation
        # enforcing arc consistency
        self.ac3()
        assignment = self.backtrack(dict())
        self.update_values(assignment)
        print("solved")

    def ac3(self):
        # add arcs to a list of all arcs
        self.arcs = []
        for cellx in self.domains:
            for celly in self.neighbors(cellx):
                self.arcs.append((cellx, celly))
        
        while len(self.arcs) != 0:
            cellx, celly = self.arcs.pop()
            if self.arc_reduce(cellx, celly):
                if len(self.domains[cellx]) == 0:
                    print("error during arc-consistency: cannot make arc consistent")
                    return(False)
                for cellz in self.neighbors(cellx):
                    if cellz != celly:
                        self.arcs.append((cellz, cellx))
        print("grid is now arc consistent")
        return(True)

    def backtrack(self, assignment):
        """
        textbook backtrack algorithm
        """
        # checks if assignment is complete
        if self.is_complete(assignment):
            return(assignment)
        cell = self.select_unassigned_cell(assignment)
        for value in self.domains[cell]:
            if self.is_consistent(assignment):
                assignment[cell] = value
                result = self.backtrack(assignment)
                if result != False: 
                    return(result)
        assignment.pop(cell) #this causes an error: it gets removed multiple times
        return(False)                

    def arc_reduce(self, cellx, celly):
        change = False
        for vx in self.domains[cellx]:
            possible_variable = False # does there exist a variable in the domain of celly such that cellx and celly are consistent
            for vy in self.domains[celly]:
                if vx != vy: 
                    possible_variable = True
            if possible_variable == False:
                self.domains[cellx].remove(vx)
                change = True
        return(change)

    def find_pentomino(self, cell_coords):
        """
        finds the rest of the cells in the same pentomino as cell_coords (excluding cell_coords)
        returns a list of cell objects
        """
         # current cell in the pentomino (to differentiate from current cell in grid)
        p_current = self.cells[cell_coords[0]][cell_coords[1]]
        frontier = [p_current]
        pentomino = []
        while len(frontier) != 0:           
            p_current = frontier.pop()
            pentomino.append(p_current)
            # adds all neighbours that arent already in p_current to p_current
            for i in range(len(p_current.sides)):
                side = p_current.sides[i]
                if side == 0: # if there is no side here, there is neighbour beside
                    axis = (i)%2 # 1 for x, 0 for y (matrices order)
                    sign = ((((i+1)//2)%2)*2)-1 # ±1
                    new_coords = list(p_current.coordinates)
                    new_coords[axis]+=sign                   
                    new_x, new_y =  tuple(new_coords)
                    new_cell= self.cells[new_x][new_y]
                    # if it's not already explored, add it to frontier
                    if new_cell not in pentomino and new_cell not in frontier:
                        frontier.append(new_cell)
        return(pentomino)


def main():
    grid = Grid("p93_corrected", "p93")
    grid.show_grid()
    grid.solve()
    grid.show_grid()

if __name__ == "__main__":
    main()