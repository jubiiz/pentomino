import cv2
import numpy as np
import os


MARGIN = 10

def build_sides(path):    
    case = cv2.imread(path, 0)
    case = cv2.resize(case, (64, 64))
    # further filtering to ensure that the small sides are gone
    # erosion filter taken from https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#morphological-ops
    kernel = np.ones((5,5),np.uint8)
    case = cv2.erode(case, kernel, iterations = 1)  


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
        
    print(sides)
    """
    cv2.imshow("case", case)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
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
    rows, cols = 5, 5
    for i in range(rows):
        for j in range(cols):
            path = os.path.join(os.getcwd(), f"loose_cases{os.sep}p5{os.sep}{i}_{j}.jpg")
            sides.append(build_sides(path))
    cursor = 0
    sides_path = os.path.join(os.getcwd(), "sides/p5.txt")
    with open(sides_path, "w") as w:
        for square in sides: 
            for side in square:
                    w.write(side)
            w.write(" ")
            cursor += 1
            if cursor%rows == 0:
                w.write("\n")
                

if __name__ == "__main__":
    main()
    #sides_from_file("p93")