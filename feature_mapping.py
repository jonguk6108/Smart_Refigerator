import cv2, numpy as np
import os
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

img2 = cv2.imread('./test_set_3/inner_example_1.jpg')
img1 = cv2.imread('./test_set_3/sample4.jpg')

#if os.path.exists("./test_set_3/outer_product*"):
    os.remove("./test_set_3/outer_product_"+str(i))

'''
img2 = cv2.imread('./test_set_3/sample1.jpg')
img2 = cv2.imread('./test_set_3/sample2.jpg')
img2 = cv2.imread('./test_set_3/sample3.jpg')
'''

sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2, k=2)
good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)

print(len(good))

# 결과 출력
#cv2.imshow('Good Match', res)
cv2.imwrite('./test_set_3/feature_mapping_output_1.jpg', img3)
#display('./test_set_3/feature_mapping_output_1.jpg')
cv2.waitKey()
cv2.destroyAllWindows()