from UFLD import *
import cv2
import threading
import time
import numpy as np

detector = laneDetection()
detector.setResolution(640, 480)
detector.setScaleFactor(4)
frame = 0
currentImage = None


def threadDetect():
    print("Detection initiating")
    global detector, currentImage, frame
    fps = []
    print("Waiting for camera")
    time.sleep(1)
    ret = True
    print("Detection Begins:")
    while ret:
        t1 = time.time()
        detector.getFrame(currentImage) 
        detector.preprocess()
        detector.inference()
        detector.parseResults()
        t2 = time.time()
        if frame > 30:
            fps.append(1/(t2-t1))
            print("\ravg FPS: "+str(np.mean(fps)), end="", flush=True)

        

if __name__ == "__main__":
    
    cap = cv2.VideoCapture(2)
    
    detecting = threading.Thread(target=threadDetect)
    detecting.setDaemon(True)
    detecting.start()

    
    while True:    
        _, currentImage = cap.read()
        frame += 1
      
    detecting.join()


