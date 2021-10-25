import cv2
import numpy as np
import os

PAD = 50

def pentomino_from_image(source_file):
    """
    source_file : string name of img file from cwd (normally images/{imgname}.{img_format})
    """
    path = os.path.join(os.getcwd(), source_file)
    img = cv2.imread(path, 0)

    # shows the image used
    cv2.imshow("unprocessed image", img)
    cv2.waitKey()

    #thresholds the image ; we need an image of size approx 300:500 (arbitrary, may be made better)
    _, copy = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    rows, cols = copy.shape
    print("number of rows and collumns ; ", rows, cols)

    # this next section records the four corner of the image (from the user)
    points = []

    def get_pt(event, x, y, flags, params):
        if event == cv2.EVENT_RBUTTONDBLCLK or event == cv2.EVENT_LBUTTONDBLCLK:
            print((x, y))
            points.append([x, y])
    
    cv2.namedWindow("gaussian img", cv2.WINDOW_FREERATIO)
    # getting user to input the corners
    print("now is time to click corners (cartesian direction : 1, 2, 3, 4)")
    cv2.setMouseCallback('gaussian img', get_pt)
    cv2.imshow("gaussian img", copy)
    cv2.waitKey()

    # this section warps the image to that the grid is square (sides should be parallel)
    # taken from https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html#geometric-transformations
    # pretty much directly (as much as there's not many ways to get the same thing...)
    pts1 = np.float32(points)
    pts2 = np.float32([[cols-PAD, PAD], [PAD, PAD], [PAD, cols-PAD], [cols-PAD, cols-PAD]])
    print(pts1, pts2)
    M = cv2.getPerspectiveTransform(pts1,pts2)
    copy = cv2.warpPerspective(copy,M,(cols,rows))

    cv2.namedWindow("warped", cv2.WINDOW_FREERATIO)
    cv2.imshow("warped", copy)
    cv2.waitKey()


    print(copy.shape)
    # calculations as to the pixel size of one square
    sqr_size = int(input("enter the number of squares along one side of the pentomino problem"))


    return(0)



def main():
    print("this section is still in development")

    # makes a pentomino from a source file
    source_file = "images/p1.jpg"
    pentomino = pentomino_from_image(source_file)

if __name__ == "__main__":
    main()