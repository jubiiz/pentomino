import os
import cv2
import numpy as np
from processor import *
from sides import *
from numext import *

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
                inbounds = (0<=xcoord<problem_size[0], 0<=ycoord<problem_size[1])
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
        print("done")
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


if __name__ == "__main__":
    main()

