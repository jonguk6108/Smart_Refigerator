import cv2

src_img = cv2.imread('animal.jpg')
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
c_classifier = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_eye.xml")
d_objects = c_classifier.detectMultiScale(gray_img, minSize=(50, 50))
if len(d_objects) != 0:
    for (x, y, h, w) in d_objects:
        cv2.rectangle(src_img, (x, y), ((x + h), (y + w)), (0, 255, 255), 5)

cv2.imshow('Detected Objects', src_img)
cv2.waitKey(0)