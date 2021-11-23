# this file has as purpose to evaluate the model with the cases of the pentomino
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import os
import cv2

def number_extractor(supervision = False):
    """
       extracts the numbers from the grid
       Returns a dictionary "numbers" of (x, y):num pairs
       num = 0 if there is no number 
    """
    # load the model from which to predict
    model = tf.keras.models.load_model('models/numext1.h5')

    numbers = {}

    # list of the names of the cases files to test
    tests = []
    for i in range(20):
        for j in range(20):
            tests.append((i, j))
    

    for i, j in tests: 
        # load case image
        path = os.path.join(os.getcwd(), f"tight_cases/{i}_{j}.jpg")
        case = cv2.imread(path, 0)
        case = cv2.resize(case, (28, 28))
        case = np.array([case])
        
        # predict and append value to dictionary
        prediction = model.predict(case)
        x = np.argmax(prediction)
        if prediction[0][x] < 0.6:
            pass
            #print("no number (probably) ")
        
        else: 
            cv2.namedWindow("img", cv2.WINDOW_FREERATIO)
            cv2.imshow("img", case[0])
            cv2.waitKey(20)
            if supervision == True:
                change = int(input(x))
                if change: 
                    x = change
            numbers[(i, j)] = x
                

    return(numbers)


def main():

    numbers = number_extractor(supervision=True)
    print(numbers)

if __name__ == "__main__":
    main()