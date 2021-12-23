import cv2
import numpy as np
import os


MARGIN = 10

def build_sides(path):    
    case = cv2.imread(path, 0)
    rows, cols = case.shape
    # we want to check the four rectangle ROI, from the center to each side, having dimensions of rows(should=cols)/2x(cols-2margin)
    # north east south west
    # ASSUMES COLS = ROWS
    cardinals = []    
    line = slice(MARGIN,cols-MARGIN)
    mid_space_0 = slice(0, MARGIN)
    mid_space_1 = slice(cols-MARGIN, cols)

    # north
    cardinals.append(case[mid_space_0, line])
    # east
    cardinals.append(case[line, mid_space_1])
    # south
    cardinals.append(case[mid_space_1, line])
    # west
    cardinals.append(case[line, mid_space_0])

    sides = []

    for c in cardinals:
        if is_solid(c):
            sides.append("1")
        else:
            sides.append("0")
    return(sides)

def is_solid(img):
    thr = max(img.shape) - 5
    lines = cv2.HoughLines(img,1,np.pi/180,thr)
    try:
        lines.any()
        return(True)
    except: AttributeError
    return(0)

def sides_from_file(filename):
    """
    from a textfile containing side quadruplets for each square, 
    it appends the quadruplets to a nxn list where n = the length
    of the side of the problem
    """
    path = f"sides{os.sep}{filename}.txt"
    with open(path, "r") as r:
        grid = []
        row = []
        square = []
        for char in r.read():
            if char == "1" or char == "0":
                square.append(int(char))
            elif char == " ":
                row.append(square)
                square = []
            elif char == "\n":
                grid.append(row)
                row = []
    return(grid)

def main():
    sides = []
    for i in range(20):
        for j in range(20):
            path = os.path.join(os.getcwd(), f"loose_cases{os.sep}{i}_{j}.jpg")
            sides.append(build_sides(path))
    side_len = 20
    cursor = 0
    sides_path = os.path.join(os.getcwd(), "sides/p93.txt")
    with open(sides_path, "w") as w:
        for square in sides: 
            for side in square:
                    w.write(side)
            w.write(" ")
            cursor += 1
            if cursor%side_len == 0:
                w.write("\n")
                

if __name__ == "__main__":
    #main()
    sides_from_file("p93")