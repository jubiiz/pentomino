import cv2
import numpy as np
import os

PAD = 20

class Cell():
    def __init__(self, value, coordinates, sides):
        self.value = value
        self.coordinates = coordinates
        self.sides = sides

#def num_from_cell():
    #TODO

def extract_corners(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # before


    biggest = None
    max_a = 0
    cutoff = 20000
    # biggest contour function taken from https://www.youtube.com/watch?v=qOXDoYUgNlU&t=1440s
    for cnt in contours:
        a = cv2.contourArea(cnt)
        
        if a > cutoff:
            print(a)
            perimeter = cv2.arcLength(cnt, True) #true being the closed param? I guess?
            approx = cv2.approxPolyDP(cnt, 0.1*perimeter, True)
            if a > max_a and len(approx) == 4:
                biggest = approx
                max_a = a
    print(biggest)
    cv2.imshow("contours", contoured)
    cv2.waitKey()
    cv2.destroyAllWindows()
    print("shown")
    points = np.float32(biggest)
    return(points)

def pentomino_from_image(source_file):
    """
    source_file : string name of img file from cwd (normally images/{imgname}.{img_format})
    """
    path = os.path.join(os.getcwd(), source_file)
    img = cv2.imread(path, 0)


    img = cv2.resize(img, (500, 700))

    # this next section records the four corner of the image (automatically)
    #thresholds the image ; we need an image of size approx 300:500 (arbitrary, may be made better)
    _, bin = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # shows the image used
    bin = cv2.bitwise_not(bin)
    cv2.imshow("unprocessed image", bin)
    cv2.waitKey()    

    points = extract_corners(bin)
    print("extracted")

    rows, cols = bin.shape
    print("number of rows and collumns ; ", rows, cols)    

    # NEED TO CLEAN THIS PART
    
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

    cropped = copy[PAD:cols-PAD, PAD:cols-PAD]

    cv2.namedWindow("cropped", cv2.WINDOW_FREERATIO)
    cv2.imshow("cropped", cropped)
    cv2.waitKey()

    # from here on we will be working with the cropped image
    rows, cols = cropped.shape
    # calculations as to the pixel size of one square
    num_sqr = int(input("enter the number of squares along one side of the pentomino problem "))
    # we need a tuple of ints : we can't have half a pixel
    sqr_size = ((rows-(2*PAD))//num_sqr,(cols-(2*PAD))//num_sqr)

    # loop over every case, add coordinates to a dictionary, along with the cropped image of that tile
    cases = {}
    # watch out : margin need to be smaller than PAD
    margin = PAD
    for i in range(num_sqr):
        for j in range(num_sqr):
            # cell (i, j) = cropped[i:i+1, j:j+1]
            # could be a function that returns the cropped image
            case = cropped[(PAD+i*sqr_size[0])-margin:(PAD+(i+1)*sqr_size[0])+margin, (PAD+j*sqr_size[1])-margin:(PAD+(j+1)*sqr_size[1])+margin]
            cases[(i, j)] = case

            
            cv2.imshow("case", case)
            cv2.waitKey(200)
            cv2.destroyWindow("case")
            
    # choose if the images are good
    save = input("do you want to save this batch of images?")

    if save == "yes":
        for i in range(num_sqr):
            for j in range(num_sqr):
                # cell (i, j) = cropped[i:i+1, j:j+1]
                # could be a function that returns the cropped image
                case = cropped[(PAD+i*sqr_size[0])-margin:(PAD+(i+1)*sqr_size[0])+margin, (PAD+j*sqr_size[1])-margin:(PAD+(j+1)*sqr_size[1])+margin]
                cases[(i, j)] = case
                save_path = os.path.join(os.getcwd(), "cases/{}_{}.jpg".format(i, j))
                cv2.imwrite(save_path, case)

            


    return(cases)



def main():
    print("this section is still in development")

    # makes a pentomino from a source file

    source_file = "images/p3.jpg"

    # extracts a preprocessed image for each cell into a dictionary {(i, j):cv2.img} for every cell coordinate (i, j)
    cell_images = pentomino_from_image(source_file)


if __name__ == "__main__":
    main()