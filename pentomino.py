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
        self.pentomino = None

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
        self.size = (5, 5)

        # extracts info from text files
        sides_list = sides_from_file(sides_file)
        num_list = nums_from_file(nums_file)

        # builds array of cells
        self.cells = []
        all_cells = []   # 1d list of cells for pentomino frontier search
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

        # adds all pentomino to cell
        for p in self.pentominos:
            for cell in p:
                cell.pentomino = p

        self.domains = {}
        for pentomino in self.pentominos:
            lp = len(pentomino) # length pentomino
            for cell in pentomino:
                if cell.value == 0:
                    self.domains[cell] = list(range(lp, 0, -1)) # like 5, 4, 3, 2, 1 so higher values are taken first: less neighbor domain values ruled out by them
                else:
                    self.domains[cell] = [cell.value]
        print("initialization done")

    def show_grid(self):
        fig, ax = plt.subplots()
        ax.set_xlim(left=0, right=self.size[1])
        ax.set_ylim(bottom=0, top=self.size[0])
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
        if len(self.domains[cell])> 2: 
            print("bigger than 2")
        return(best_cell)

    def update_values(self, assignment):
        """
        update the values after backtrack: for a given assignment
        """
        for cell in assignment:
            cell.value = assignment[cell]

    def solve(self):
        """
        returns a solved version of the suguru else returns False
        """
        # node consistency enforced in domain creation
        # enforcing arc consistency
        while True:
            self.arc_consistency()
            if not self.unique_values():
                break
        print("logic elimination done")
        self.show_grid()
        
        assignment = {}
        for cell in self.domains:
            if len(self.domains[cell]) == 1:
                assignment[cell] = self.domains[cell][0]


        self.update_values(assignment)
        print("solved")

    def arc_consistency(self):
        # add arcs to a list of all arcs
        self.cc_arcs = [] # cell cell arcs
        self.cp_arcs = [] # cell pentomino arcs
        for cellx in self.domains:
            for celly in self.neighbors(cellx):
                self.cc_arcs.append((cellx, celly))
                cp_arc = (cellx, celly.pentomino)
                if cp_arc not in self.cp_arcs and celly.pentomino is not cellx.pentomino: 
                    self.cp_arcs.append(cp_arc)
        
        # check every arc, if they have to be changed then add all new arcs to list
        while True:
            if len(self.cc_arcs) != 0:
                cellx, celly = self.cc_arcs.pop()
                if cellx.coordinates == (19, 13):
                    print("here_cc")
                if self.arc_reduce_cc(cellx, celly):
                    if len(self.domains[cellx]) == 0:
                        print("error during arc-consistency: cannot make arc consistent")
                        return(False)
                    for cellz in self.neighbors(cellx):
                        if cellz != celly:
                            self.cc_arcs.append((cellz, cellx))
                        if (cellz, cellx.pentomino) not in self.cp_arcs:
                            self.cp_arcs.append((cellz, cellx.pentomino))

            elif len(self.cp_arcs) != 0:
                print("cp")
                # check consistency between cellx and pentomino_y
                cellx, py = self.cp_arcs.pop()
                if cellx.coordinates == (19, 13):
                    print("here_cp")
                if self.arc_reduce_cp(cellx, py):
                    if len(self.domains[cellx]) == 0:
                        print(f"error during arc-consistency-cp: cannot make arc consistent because of cell {cellx.coordinates}")
                        return(False)
                    for cellz in self.neighbors(cellx):
                        self.cc_arcs.append((cellz, cellx))
                        if (cellz, cellx.pentomino) not in self.cp_arcs and cellz.pentomino is not cellx.pentomino:
                            self.cp_arcs.append((cellz, cellx.pentomino))
            else:
                break

        for cell in self.domains:
            domain = self.domains[cell]
            if len(domain) == 1:
                cell.value = domain[0]
            elif len(domain) == 0:
                print(f"inconsistent arcs: no possible solution because of {cell.coordinates}")
                return(False)

        print("grid is now arc consistent")
        return(True)

    def unique_values(self):
        # for every pentomino, make a list of each possible domain value, and which cell has it in its domain
        change = False
        for pentomino in self.pentominos:
            numrange = {i+1:[] for i in range(len(pentomino))}
            for cell in pentomino:
                for d_val in self.domains[cell]:
                    numrange[d_val].append(cell)
            
            for d_val in numrange:
                # if only one cell has that value in its domain, it takes that value
                if len(numrange[d_val]) == 1:
                    cell = numrange[d_val][0]
                    if len(self.domains[cell]) != 1:
                        change = True  
                        print(cell.coordinates)                  
                        self.domains[cell] = [d_val]
                        cell.value = d_val

        return(change)

    def backtrack(self, assignment):
        """
        textbook backtrack algorithm
        """
        # checks if assignment is complete
        if self.is_complete(assignment):
            return(assignment)
        cell = self.select_unassigned_cell(assignment)
        #if len(self.domains[cell]) != 1:
            #print(len(assignment))
        print(len(assignment))
        odv = self.order_domain_values(cell) # ordered domain values
        for value in odv:
            #print("cell: ", cell.coordinates, "value", value)
            assignment[cell] = value
            if self.is_consistent(assignment):
                
                """                if len(assignment) == 98:
                    self.update_values(assignment)
                    self.show_grid()
                    plt.ion()
                    print("shown")"""
                result = self.backtrack(assignment)
                if result != False: 
                    return(result)
            if cell in assignment:
                assignment.pop(cell) 
        return(False)                

    def arc_reduce_cc(self, cellx, celly):
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

    def arc_reduce_cp(self, cellx, py):
        """
        for every value in cellx,
        can py be completed?
        """
        affected_cells = self.neighbors(cellx)
        change = False
        for vx in self.domains[cellx]:
            if vx in range(1, len(py)+1): # if vx has to be in py, check if it can still be there
                present = False
                for p_cell in py: # is there at least 1 cell that can take that value
                    if vx in self.domains[p_cell] and p_cell not in affected_cells: # value is present in this cell's domain, and is unaffected by vx
                        present = True
                if present == False: # cannot have this value in the pentomino
                    change = True
                    self.domains[cellx].remove(vx)
        return(change)

    def order_domain_values(self, cell):
        """
        orders the domain values such that the values that are least present in the cell's pentomino are taken first
        """
        for pentomino in self.pentominos:
            # we need only the pentomino in which our cell is
            if cell in pentomino:
                scores = {i:0 for i in self.domains[cell]}
                for other_cell in pentomino:
                    for d_val in self.domains[other_cell]:
                        if d_val in scores:
                            scores[d_val] += 1
            
                # taken from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
                scores = {i:j for i, j in sorted(scores.items(), key=lambda item: item[1])}
        return(scores.keys())

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
            # adds all neighbours that arent already in frontier or pentomino to frontier
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
        if len(pentomino) > 5:
            print("pentomino error ")
            for cell in pentomino:
                print(cell.coordinates)
            return(1)
        return(pentomino)


def main():
    grid = Grid("p5", "p5")
    grid.show_grid()
    grid.solve()
    grid.show_grid()

if __name__ == "__main__":
    main()