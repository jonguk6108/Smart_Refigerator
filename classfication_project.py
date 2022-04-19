#date : 20220419

from email.base64mime import body_encode
from re import X
from tkinter import N
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

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

def remove_file(file_path, file_extension):
    for i in range(100) :
        if os.path.exists(file_path + str(i) + file_extension):
            os.remove(file_path + str(i) + file_extension)


### Part 1 ### sta
# classfication boundary box in original picture and store each index's position informations

image = cv2.imread('./test_set_4/inner.png')
original = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

image_size_w = image.shape[1]
image_size_h = image.shape[0]

boundary_table = [[0 for i in range(5)] for j in range(100)]

index = 0
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    if w < 50 or h < 50 :
        continue
    boundary_table[index][0] = x
    boundary_table[index][1] = y
    boundary_table[index][2] = w
    boundary_table[index][3] = h
    boundary_table[index][4] = 1
    index+=1

#merge boundary box -1
for i in range(0, index):
    for j in range(0, index):
        if i == j :
            continue
        if boundary_table[j][4] != 1 :
            continue
        
        ix1, ix2, iy1, iy2 = boundary_table[i][0], boundary_table[i][0] + boundary_table[i][2], boundary_table[i][1], boundary_table[i][1] + boundary_table[i][3]
        jx1, jx2, jy1, jy2 = boundary_table[j][0], boundary_table[j][0] + boundary_table[j][2], boundary_table[j][1], boundary_table[j][1] + boundary_table[j][3]
        iremove = boundary_table[i][4]

        # remove edge box
        if (ix1 < 5 and iy1 < 5) or (ix2 > image_size_w - 5 and iy1 < 5) or (ix1 < 5 and iy2 > image_size_h - 5) or (ix2 > image_size_w - 5 and iy2 > image_size_h - 5):
            boundary_table[i][4] = -1
            continue

        # left up in jbox
        if jx1 <= ix1 <= jx2 and jy1 <= iy1 <= jy2  :
            if jx2 < ix2 :
                jx2 = ix2
            if jy2 < iy2 :
                jy2 = iy2
            iremove = -1

        # left down in jbox
        elif jx1 <= ix1 <= jx2 and jy1 <= iy2 <= jy2  :
            if jx2 < ix2 :
                jx2 = ix2
            if iy1 < jy1 :
                jy1 = iy1
            iremove = -1

        # right up in jbox
        elif jx1 <= ix2 <= jx2 and jy1 <= iy1 <= jy2  :
            if ix1 < jx1 :
                jx1 = ix1
            if jy2 < iy2 :
                jy2 = iy2
            iremove = -1
    
        # right down in jbox
        elif jx1 <= ix2 <= jx2 and jy1 <= iy2 <= jy2  :
            if ix1 < jx1 :
                jx1 = ix1
            if iy1 < jy1 :
                jy1 = iy1
            iremove = -1

        boundary_table[j][0], boundary_table[j][2], boundary_table[j][1], boundary_table[j][3] = jx1 , jx2 - jx1, jy1, jy2 - jy1
        boundary_table[i][4] = iremove

"""
        print( str(i) + str(j))
        for k in range(index) : 
            print(str( boundary_table[k][0] ) + " " + str( boundary_table[k][0] + boundary_table[k][2] ) + " " + str( boundary_table[k][1] ) + " " + str( boundary_table[k][1] + boundary_table[k][3] ) + " ")
        print(" ")

#merge boundary box -2
for i in range(0, index):
    for j in range(0, index):
        if i == j :
            continue
        if boundary_table[j][4] != 1 :
            continue
        
        ix1, ix2, iy1, iy2 = boundary_table[i][0], boundary_table[i][0] + boundary_table[i][2], boundary_table[i][1], boundary_table[i][1] + boundary_table[i][3]
        jx1, jx2, jy1, jy2 = boundary_table[j][0], boundary_table[j][0] + boundary_table[j][2], boundary_table[j][1], boundary_table[j][1] + boundary_table[j][3]
        iremove = boundary_table[i][4]

        ixm = (ix1 + ix2) /2
        iym = (iy1 + iy2) /2
        jxm = (jx1 + jx2)

"""



for i in range(index) : 
    print(boundary_table[i])

i = 0
while i <= index :
    if boundary_table[i][4] != 1 :
        index -= 1
        j = i
        while j < 99 :
            for k in range(5) :
                boundary_table[j][k] = boundary_table[j+1][k]
            j += 1

    else :
        i += 1

print(index)
for i in range(index+1) : 
    print(boundary_table[i])

remove_file("./test_set_4/inner_product_", ".png")
for i in range(index + 1):
    x,y,w,h = boundary_table[i][0], boundary_table[i][1], boundary_table[i][2], boundary_table[i][3]
    cut_image = image[y:y+h, x:x+w].copy()
    cv2.imwrite("./test_set_4/inner_product_"+str(i)+".png", cut_image)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

#display('image', image)
cv2.imwrite('./test_set_4/output_shapes.png', image)
display('./test_set_4/output_shapes.png')
#display('Thresh',thresh)
cv2.waitKey()

f = open("./test_set_4/positions.txt", 'w')
f.write( str(index+1) + '\n')
for i in range(index + 1):
    f.write( str(i) + ' ' + str(boundary_table[i][0])+ ' '+ str(boundary_table[i][1])+ ' '+ str(boundary_table[i][2])+ ' '+ str(boundary_table[i][3]) + '\n')
f.close()
### Part 1 ### fin


### Part 2 ### sta
# feature matching pick

outer_product_number = 3
inner_product_number = index + 1

matching_values = [[0 for col in range(outer_product_number)] for row in range( inner_product_number )]

for i in range(inner_product_number) :
    for j in range(outer_product_number) :

        imgi = cv2.imread('./test_set_4/inner_product_' + str(i) +'.png')
        imgj = cv2.imread('./test_set_4/product_' + str(j+1) +'.png')

        sift = cv2.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(imgi,None)
        kp2, des2 = sift.detectAndCompute(imgj,None)
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        good = []
        for m,n in matches:
            if m.distance < 0.5*n.distance:
                good.append([m])
#       img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
        matching_values[i][j] = len(good)

for i in range(inner_product_number):
    print(matching_values[i])

'''
# 결과 출력
#cv2.imshow('Good Match', res)
cv2.imwrite('./test_set_2/feature_mapping_3.jpg', img3)
display('./test_set_2/feature_mapping_3.jpg')
cv2.waitKey()
cv2.destroyAllWindows()
'''

### Part 2 ### fin