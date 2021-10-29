# this file has as purpose to evaluate the model with the cases of the pentomino
import tensorflow as tf
import numpy as np
import os
import cv2

def testMnist():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # normalize the input data
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)
    print(x_test[0])
    print(x_test[0].shape)

    #test = x_test[0].reshape(784)
    #print(test.shape)

    model = tf.keras.models.load_model('digits.model')
    prediction = model.predict(x_test)
    print(y_test[0])
    cv2.imshow("image", x_test[0])
    print(prediction)
    print(np.argmax(prediction))

def testUncropped():
    """
        uncropped does not work : the inside of a case will have to be artificially selected
    """
     # list of the names of the cases files to test
    tests = ["0_4.jpg", "0_9.jpg", "0_15.jpg"]

    model = tf.keras.models.load_model('digits.model')

    for file in tests: 
        # load case image
        path = os.path.join(os.getcwd(), "cases/{}".format(file))
        case = cv2.imread(path, 0)
        case = cv2.resize(case, (28, 28))
        case = np.array([case])
        # normalize input data
        case = np.invert(case)
        case = tf.keras.utils.normalize(case, axis=1)
        print(case.shape)
        
        # output prediction
        prediction = model.predict(case)
        print(prediction)
        x = np.argmax(prediction)
        print(x)

    return(0)

def testCells():
    # list of the names of the cases files to test
    tests = ["0_4.jpg", "0_9.jpg", "0_15.jpg"]

    model = tf.keras.models.load_model('digits.model')

    for file in tests: 
        # load case image
        path = os.path.join(os.getcwd(), "cases/{}".format(file))
        case = cv2.imread(path, 0)

        # show image and require cropping
        rows, cols = case.shape
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
        cv2.imshow("gaussian img", case)
        cv2.waitKey()

        # this section warps the image to that the grid is square (sides should be parallel)
        # taken from https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html#geometric-transformations
        # pretty much directly (as much as there's not many ways to get the same thing...)
        pts1 = np.float32(points)
        pts2 = np.float32([[cols, 0], [0, 0], [0, cols], [cols, cols]])
        print(pts1, pts2)
        M = cv2.getPerspectiveTransform(pts1,pts2)
        case = cv2.warpPerspective(case,M,(cols,rows))

        cv2.namedWindow("warped", cv2.WINDOW_FREERATIO)
        cv2.imshow("warped", case)
        cv2.waitKey()
        cv2.destroyAllWindows()

        # resize img to network size (I arbitrarily know it is 28 (at least when i wrote this comment))
        # I think you can use model.summary() to figure out what should the input size be
        case = cv2.resize(case, (28, 28))
        case_arr = np.array([case])


        # normalize input data
        case_arr = np.invert(case_arr)
        norm_case = tf.keras.utils.normalize(case_arr, axis=1)
        print(norm_case)
        
        # output prediction
        prediction = model.predict(norm_case)
        print(prediction)
        x = np.argmax(prediction)
        print(x)
        


    return(0)

def main():

    #testMnist()
    #testUncropped()
    testCells()

if __name__ == "__main__":
    main()