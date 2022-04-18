import cv2
import cvzone
from matplotlib import pyplot as plt
from cvzone.SelfiSegmentationModule import SelfiSegmentation

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

segmentor = SelfiSegmentation()
img = cv2.imread('./test_set_2/original_image.jpg')
img_Out = segmentor.removeBG(img, (255,255,255), threshold=10E-20)

#cv2.imshow('img',img_Out)
cv2.imwrite('./test_set_2/bg_sub.png', img_Out)
display('./test_set_2/bg_sub.png')
cv2.waitKey(0)
cv2.destroyAllWindows()