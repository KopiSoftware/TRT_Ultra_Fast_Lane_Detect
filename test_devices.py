import cv2

import time
import numpy as np

currentImage = None


        
frame = 0
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:    
        frame += 1
        _, currentImage = cap.read()
        cv2.imshow("",currentImage)
        key = cv2.waitKey(1)
        if key == 'a':
            cv2.imwrite(str(frame)+".jpg",currentImage)
    

