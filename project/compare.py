### Part 2 ### sta
# feature matching pick

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

def compare(inner_product_number, outer_product_number, threshold, matching_list_inner, matching_list_outer) :
    matching_values = [[0 for col in range(outer_product_number)] for row in range( inner_product_number )]

    for i in range(inner_product_number) :
        for j in range(outer_product_number) :
            imgi = cv2.imread("./img/inner/inner_"+str(i)+".png")
            imgj = cv2.imread('./img/crop/outer_crop_'+ str(j) + ".png")

            sift = cv2.xfeatures2d.SIFT_create()
            kp1, des1 = sift.detectAndCompute(imgi,None)
            kp2, des2 = sift.detectAndCompute(imgj,None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1,des2, k=2)
            good = []
            for m,n in matches:
                if m.distance < threshold * n.distance:
                    good.append([m])
                    #img3 = cv2.drawMatchesKnn(imgi,kp1,imgj,kp2,good,None,flags=2)
                    #cv2.imwrite('./trash/tmp.png', img3)
                    #display('./trash/tmp.png')
            matching_values[i][j] = len(good)

    for i in range(inner_product_number):
        print(matching_values[i])

    for i in range(inner_product_number):
        max_index = 0
        max_value = -1

        for j in range(outer_product_number):
            if(matching_list_outer[j] != -1):
                continue

            if(matching_values[i][j] > max_value):
                max_index = j
                max_value = matching_values[i][j]
        
        if(max_value > 30):
            matching_list_inner[i] = max_index
            matching_list_outer[max_index] = i
    

    matching_values = [[1000000 for col in range(outer_product_number)] for row in range( inner_product_number )]
    for inner_index in range(inner_product_number) :
        if(matching_list_inner[inner_index] != -1):
                continue
        for outer_index in range(outer_product_number) :
            if(matching_list_outer[outer_index] != -1):
                continue
            print('\ninner_index : ' +str(inner_index) + ' ,outer_index : '+ str(outer_index) + ' \n')
            img1 = cv2.imread("./img/inner/inner_"+str(inner_index)+".png")
            img2 = cv2.imread('./img/crop/outer_crop_'+ str(outer_index) + ".png")

            #cv2.imshow('query', img1)
            imgs = [img1, img2]
            hists = []
            for i, img in enumerate(imgs) :
                plt.subplot(1,len(imgs),i+1)
                plt.title('img%d'% (i+1))
                plt.axis('off') 
                #plt.imshow(img[:,:,::-1])
                #---① 각 이미지를 HSV로 변환
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                #---② H,S 채널에 대한 히스토그램 계산
                hist = cv2.calcHist([hsv], [0,1], None, [180,256], [0,180,0, 256])
                #---③ 0~1로 정규화
                cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
                hists.append(hist)

            query = hists[0]
            methods = {'CHISQR':cv2.HISTCMP_CHISQR, 'BHATTACHARYYA':cv2.HISTCMP_BHATTACHARYYA}
            methods_size = 1
            for j, (name, flag) in enumerate(methods.items()):
                print('%-10s'%name, end='\t')
                for i, (hist, img) in enumerate(zip(hists, imgs)):
                    #---④ 각 메서드에 따라 img1과 각 이미지의 히스토그램 비교
                    ret = cv2.compareHist(query, hist, flag)
                    if flag == cv2.HISTCMP_INTERSECT: #교차 분석인 경우 
                        ret = ret/np.sum(query)        #비교대상으로 나누어 1로 정규화

                    if(i != 0):
                        methods_size *= ret
                    print("img%d:%7.2f"% (i+1 , ret), end='\t')
                print()
            
            matching_values[inner_index][outer_index] = methods_size
            #plt.show()

    print("\n\nmatching_list : ")
    print(matching_list_inner)
    print(matching_list_outer)
    print("\n")

    for i in range(inner_product_number):
        print(matching_values[i])

    for i in range(inner_product_number):
        if(matching_list_inner[i] != -1):
            continue
        min_index = -1
        min_value = 10000000

        for j in range(outer_product_number):
            if(matching_list_outer[j] != -1):
                continue

            if(matching_values[i][j] < min_value):
                min_index = j
                min_value = matching_values[i][j]

        matching_list_inner[i] = min_index
        matching_list_outer[min_index] = i

### Part 2 ### fin