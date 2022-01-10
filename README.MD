SUGURU SOLVER

This personnal project was meant to test my ability to build a big project from the ground up (from idea to result, with no premade youtube tutorial available). I also practiced using github and git in the process: all my coordination was done via those two tools. 

Although it is far from user friendly, I am able to use it to solve 20x20 extra-hard sugurus in less than an hour. These usually take upwards of 5 hours by hand. Just for that, I consider it a success.

usage:
The project takes as input an image of a suguru, then via many separate program files, the image is segmented into cases, the useful data is extracted from those images, then the suguru is represented in the code (as to be manipulated) and then solved. The solved version is displayed at the end.

The most important technologies it leverages are:
CNNs: to extract number data
cv2: for all image manipulation
matplotlib: for solving process updates (lets the user see where it's at, useful for debugging)
ac3 algorithm: for solving
