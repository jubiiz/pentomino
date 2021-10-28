import numpy as np
import cv2
import tensorflow as tf

def main():
    # code mostly taken from https://www.youtube.com/watch?v=Zi4i7Q0zrBs&t=507s

    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # normalize the training data
    x_train = tf.keras.utils.normalize(x_train, axis=1)
    x_test = tf.keras.utils.normalize(x_test, axis=1)

    # initiate the model as a sequential model
    model = tf.keras.models.Sequential()
    # one input layer
    model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
    # add to the model two hidden dense layers
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    # one output layer (the softmax activation function returing a probability distribution for each node)
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))

    # compile and fit the model (like create and train)
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=20)

    # testing the model
    loss, accuracy = model.evaluate(x_test, y_test)
    print("loss : ", loss)
    print("accuracy : ",  accuracy)

    model.save('digits.model')


if __name__ == "__main__":
    main()