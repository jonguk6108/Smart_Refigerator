### Part 2 ### sta
# feature matching pick

def compare(inner_product_number, outer_product_number, threshold) :
    matching_values = [[0 for col in range(outer_product_number)] for row in range( inner_product_number )]

    for i in range(inner_product_number) :
        for j in range(outer_product_number) :
            imgi = cv2.imread("./img/inner/inner_"+str(i)+".png")
            imgj = cv2.imread('./img/entire/outer_entire'+ str(i) + ".png")

            sift = cv2.xfeatures2d.SIFT_create()
            kp1, des1 = sift.detectAndCompute(imgi,None)
            kp2, des2 = sift.detectAndCompute(imgj,None)
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1,des2, k=2)
            good = []
            for m,n in matches:
                if m.distance < threshold * n.distance:
                    good.append([m])
                    #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)
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