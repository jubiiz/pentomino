# this file has as purpose to extract the numbers from the suguru's cells
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
import os
import cv2

def number_extractor(supervision = False, size=(20, 20)):
    """
       extracts the numbers from the grid
       Returns a dictionary "numbers" of (x, y):num pairs
       num = 0 if there is no number 
    """
    # load the model from which to predict
    model = tf.keras.models.load_model('models/numext2.h5')


    numbers = {}

    # list of the names of the cases files to test
    tests = []
    for i in range(size[0]):
        for j in range(size[1]):
            tests.append((i, j))
    

    for i, j in tests: 
        # load case image
        path = os.path.join(os.getcwd(), f"tight_cases/p6/{i}_{j}.jpg")
        case = cv2.imread(path, 0)
        case = cv2.resize(case, (64, 64))

        # potential roi focus needed
        case = case[12:52, 12:52]
        case = cv2.resize(case, (64, 64))

        # potential dilation needed
        case = cv2.dilate(case,np.ones(3),iterations = 1)

        case = np.array([case])

        

        case = np.expand_dims(case, axis=-1) # <--- add batch axis
        case = case.astype('float32') / 255

        # predict and append value to dictionary
        prediction = model.predict(case)
        x = np.argmax(prediction)
        if x == 1:
            avg = np.average(case)
            if avg < 0.00001:
                x = 0
                print("no number (probably) ")
            else:
                print("1 here")
        
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

def nums_from_file(filename):
    path = f"nums{os.sep}{filename}.txt"
    with open(path, "r") as r:
        grid = []
        row = []
        for num in r.read():
            if num != " " and num != "\n":
                row.append(int(num))
            elif num == "\n":
                grid.append(row)
                row = []
    return(grid)

def main():
    rows, cols = 5, 5
    numbers = number_extractor(supervision=True, size=(rows, cols))
    path = os.path.join(os.getcwd(), f"nums{os.sep}p6.txt")
    with open(path, "w") as w:
        cursor = 0
        for num in numbers:
            w.write(str(numbers[num]))
            w.write(" ")
            cursor += 1
            if cursor %rows == 0:
                w.write("\n")

if __name__ == "__main__":
    main()