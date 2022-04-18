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

image = cv2.imread('./test_set_2/shapes.png')
original = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

index = 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    if w < 50 or h < 50 :
        continue
    print("coor : " + str(x) +', '+ str(y)+ ', ' + str(w) + ', ' + str(h))
    index+=1
    cut_image = image[y:y+h, x:x+w].copy()
    cv2.imwrite("./test_set_2/outer_productt"+str(index)+".jpg", cut_image)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

#display('image', image)
cv2.imwrite('./test_set_2/output_shapes_1.jpg', image)
display('./test_set_2/output_shapes_1.jpg')
# display('Thresh',thresh)
cv2.waitKey()