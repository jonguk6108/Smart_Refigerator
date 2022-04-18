#date : 20220418

from re import X
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


### Part 1 ### sta
# classfication boundary box in original picture and store each index's position informations

image = cv2.imread('./test_set_3/original_image.jpg')
original = image.copy()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

ROI_number = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]


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

#merge boundary box
for i in range(index):
    for j in range(index):
        if i == j :
            continue
        if ((boundary_table[i][0] >= boundary_table[j][0] ) and ( boundary_table[i][0] <= boundary_table[j][0] + boundary_table[j][2] ) ) and (( boundary_table[i][1] >= boundary_table[j][1] ) and ( boundary_table[i][1] <= boundary_table[j][1] + boundary_table[j][3] ) ):
            boundary_table[i][4] = -1
        
        if ((boundary_table[i][0] + boundary_table[i][2] >= boundary_table[j][0] ) and ( boundary_table[i][0] + boundary_table[i][2] <= boundary_table[j][0] + boundary_table[j][2] ) ) and (( boundary_table[i][1] + boundary_table[i][3] >= boundary_table[j][1] ) and ( boundary_table[i][1] + boundary_table[i][3] <= boundary_table[j][1] + boundary_table[j][3] ) ):
            boundary_table[i][4] = -1

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

for i in range(index + 1):
    x,y,w,h = boundary_table[i][0], boundary_table[i][1], boundary_table[i][2], boundary_table[i][3]
    cut_image = image[y:y+h, x:x+w].copy()
    cv2.imwrite("./test_set_3/outer_product_"+str(i)+".jpg", cut_image)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0,0,255), 2)

#display('image', image)
cv2.imwrite('./test_set_3/output_shapes.jpg', image)
#display('./test_set_3/output_shapes.jpg')
#display('Thresh',thresh)
cv2.waitKey()

f = open("./test_set_3/positions.txt", 'w')
f.write( str(index+1) + '\n')
for i in range(index + 1):
    f.write( str(i) + ' ' + str(boundary_table[i][0])+ ' '+ str(boundary_table[i][1])+ ' '+ str(boundary_table[i][2])+ ' '+ str(boundary_table[i][3]) + '\n')
f.close()

### Part 1 ### fin