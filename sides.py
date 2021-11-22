import cv2
import os

MARGIN = 10

def main():
    path = os.path.join(os.getcwd(), f"loose_cases{os.sep}0_2.jpg")
    case = cv2.imread(path, 0)
    rows, cols = case.shape
    center = (rows/2, cols/2)
    # we want to check the four rectangle ROI, from the center to each side, having dimensions of rows(should=cols)/2x(cols-2margin)
    # north east south west
    # ASSUMES COLS = ROWS
    cardinals = []    
    line = slice(MARGIN,cols-MARGIN)
    mid_space_0 = slice(0, cols//2)
    mid_space_1 = slice(cols//2, cols)

    # north
    cardinals.append(case[mid_space_0, line])
    # east
    cardinals.append(case[line, mid_space_1])
    # south
    cardinals.append(case[mid_space_1, line])
    # west
    cardinals.append(case[line, mid_space_0])

    for c in cardinals:
        cv2.imshow("c", c)
        cv2.waitKey()

if __name__ == "__main__":
    main()