import cv2
import cv2
import numpy as np
from matplotlib import pyplot as plt

def display(im_path):
    dpi = 80
    im_data = plt.imread(im_path)
    height, width = im_data.shape[:2]

    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)
    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    #Hide spines, ticks, etc.
    ax.axis('off')
    # Display the image
    ax.imshow(im_data, cmap='gray')
    plt.show()
    
img = cv2.imread("./inner_ca.png")
print(img.shape)
cropped = img[70:768, 60:1024-60]

cv2.imwrite("./inner_ca1.png", cropped)
display("./inner_ca1.png")