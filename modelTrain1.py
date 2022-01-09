# most (all) of code taken from "traffic" project done with CS50: AI course

import cv2
import numpy as np
import os
import tensorflow as tf
from sklearn.model_selection import train_test_split

EPOCHS = 19
IMG_WIDTH = 64
IMG_HEIGHT = 64
NUM_CATEGORIES = 6
TEST_SIZE = 0.3

def main():
    images, labels = load_data()

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(np.array(images), np.array(labels), test_size=TEST_SIZE)

    x_train = np.expand_dims(x_train, axis=-1) # <--- add batch axis
    x_train = x_train.astype('float32') / 255
    x_test = np.expand_dims(x_test, axis=-1) # <--- add batch axis
    x_test = x_test.astype('float32') / 255
    #y_train = tf.keras.utils.to_categorical(y_train, num_classes=5)

    """x_train = x_train.reshape(-1, 28, 28, 1)
    x_test = x_test.reshape(-1, 28, 28, 1)"""

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    filename = "models/numext3.h5"
    model.save(filename)
    print(f"Model saved to {filename}.")


def load_data():
    path = os.path.join(os.getcwd(), "training_data")
    directory = os.scandir(path)

    # creates two empty lists containing the images and their corresponding labels
    images = []
    labels = []

    # for each subdirectory
    for entry in directory:
        if entry.is_dir():
            subdir = os.scandir(entry.path)
            # load images and corresponding labels into lists
            for image in subdir:
                img = cv2.imread(image.path, 0)
                
                res = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT),
                                 interpolation=cv2.INTER_LINEAR)
                images.append(res)
                labels.append(int(entry.name))
    print("labels: ", len(labels))
            

    data = tuple((images, labels))

    return(data)

def get_model():
    # cnn structure taken from https://www.tensorflow.org/tutorials/images/cnn
    # initiate the model as a sequential model
    model = tf.keras.models.Sequential()
    
    model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 1)))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.3))
    model.add(tf.keras.layers.Dense(64, activation="relu"))
    model.add(tf.keras.layers.Dense(6, activation=tf.nn.softmax))
        
    
    # compile and fit the model (like create and train)
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    model.summary()
    return(model)

if __name__ == "__main__":
    main()