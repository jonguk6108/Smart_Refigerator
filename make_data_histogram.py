# 히스토그램 비교 (histo_compare.py)

import cv2, numpy as np
import matplotlib.pylab as plt
import pandas as pd

inner_size = 3
outer_size = 22

values = [[[0 for k in range(10)] for j in range(outer_size)] for i in range(inner_size)]

for inner_index in range(inner_size) :
    img1 = cv2.imread('./test_set_7/inner0/inner_' + str(inner_index) + '.png')
    print('./test_set_7/inner' + str(inner_index) + '.png')
    for outer_index in range(outer_size):
        img2 = cv2.imread('./test_set_6/outer_crop_' + str(outer_index) + '.png')

        print('./test_set_6/outer_crop_' + str(outer_index) + '.png')
        imgs = [img1, img2]
        hists = []
        
        for i, img in enumerate(imgs) :
            plt.subplot(1,len(imgs),i+1)
            plt.title('img%d'% (i+1))
            plt.axis('off')
            #---① 각 이미지를 HSV로 변환
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            #---② H,S 채널에 대한 히스토그램 계산
            hist = cv2.calcHist([hsv], [0,1], None, [180,256], [0,180,0, 256])
            #---③ 0~1로 정규화
            cv2.normalize(hist, hist, 0, 1, cv2.NORM_MINMAX)
            hists.append(hist)

        query = hists[0]
        methods = {'CORREL' :cv2.HISTCMP_CORREL, 'CHISQR':cv2.HISTCMP_CHISQR, 
                'INTERSECT':cv2.HISTCMP_INTERSECT,
                'BHATTACHARYYA':cv2.HISTCMP_BHATTACHARYYA}

        values[inner_index][outer_index][0] = inner_index
        values[inner_index][outer_index][1] = outer_index

        for j, (name, flag) in enumerate(methods.items()):
            for i, (hist, img) in enumerate(zip(hists, imgs)):
                #---④ 각 메서드에 따라 img1과 각 이미지의 히스토그램 비교
                ret = cv2.compareHist(query, hist, flag)
                if flag == cv2.HISTCMP_INTERSECT: #교차 분석인 경우 
                    ret = ret/np.sum(query)        #비교대상으로 나누어 1로 정규화
                values[inner_index][outer_index][2 + j*2 + i] = ret
                #print("img%d:%7.2f"% (i+1 , ret), end='\t')
        #plt.show()

for inner_index in range(3) :
    for outer_index in range(22):
        print(values[inner_index][outer_index])



arr = np.array(values[0])
for inner_index in range(inner_size) :
    if inner_index == 0 :
        continue
    arr = np.append(arr, values[inner_index] , axis=0)

df = pd.DataFrame(arr)
df.to_csv('histogram.csv', index=False)