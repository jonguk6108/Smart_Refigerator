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
def bounding_box(pos, ID):
    if(pos == "entire") :
        image = cv2.imread("./img/entire/outer_entire_"+ str(ID) + ".png")
    else :
        image = cv2.imread("./img/inner/inner.png")
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

    if(pos == "inner"):
        remove_file("./img/inner/inner_", ".png")
        for i in range(index + 1):
            x,y,w,h = boundary_table[i][0], boundary_table[i][1], boundary_table[i][2], boundary_table[i][3]
            cut_image = image[y:y+h, x:x+w].copy()
            cv2.imwrite("./img/inner/inner_"+str(i)+".png", cut_image)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

        #display('image', image)
        cv2.imwrite('./img/inner/output_shapes.png', image)
        display('./img/inner/output_shapes.png')
        #display('Thresh',thresh)
        cv2.waitKey()

        f = open("./img/inner/positions.txt", 'w')
        f.write( str(index+1) + '\n')
        for i in range(index + 1):
            f.write( str(i) + ' ' + str(boundary_table[i][0])+ ' '+ str(boundary_table[i][1])+ ' '+ str(boundary_table[i][2])+ ' '+ str(boundary_table[i][3]) + '\n')
        f.close()
    else :
        remove_file("./img/crop/outer_crop_", ".png")
        
        big_index = 0
        max_size = -1
        for i in range(index + 1):
            x,y,w,h = boundary_table[i][0], boundary_table[i][1], boundary_table[i][2], boundary_table[i][3]
            if( w*h >= max_size) :
                big_index = i
                max_size = w*h

        x,y,w,h = boundary_table[big_index][0], boundary_table[big_index][1], boundary_table[big_index][2], boundary_table[big_index][3]
        cut_image = image[y:y+h, x:x+w].copy()
        cv2.imwrite("./img/crop/outer_crop_"+str(ID)+".png", cut_image)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)
        cv2.waitKey()
        index = 0

    return index + 1
### Part 1 ### fin