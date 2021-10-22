import cv2
import numpy as np
import os

def pentomino_from_image(source_file):
    """
    source_file : string name of img file from cwd (normally images/{imgname}.{img_format})
    """
    path = os.path.join(os.getcwd(), source_file)
    img = cv2.imread(path, 0)

    # shows the image used
    cv2.imshow("unprocessed image", img)
    cv2.waitKey()

    # resizes and thresholds the image ; we need an image of size approx 300:500 (arbitrary, may be made better)
    _, copy = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    copy = cv2.resize(copy, (1000, 700))
    cv2.imshow("gaussian img", copy)
    cv2.waitKey()
    return(0)



def main():
    print("this section is still in development")

    # makes a pentomino from a source file
    source_file = "images/p1.jpg"
    pentomino = pentomino_from_image(source_file)

if __name__ == "__main__":
    main()