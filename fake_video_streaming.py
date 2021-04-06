# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:07:14 2021

@author: marri
"""
import cv2
import yolo
from imutils.video import FPS
from imutils.video import VideoStream
from playsound import playsound
import winsound
import time


SAVE_VIDEO = True

fps = FPS().start()
mp3File = "bell.wav"
INPUT_FILE="00108.MTS"
fourcc = cv2.VideoWriter_fourcc(*"MJPG")

vs = cv2.VideoCapture(INPUT_FILE)
writer = cv2.VideoWriter("result.mp4", fourcc, 30,
        (800, 600), True)
cnt=0
bellcnt=0
framecnt=0
minsize = 200000
maxsize = 0
size=0
box = (0,0,0,0)
while True:
        #print('Min: ', minsize)
        #print('Max: ', maxsize)
        framecnt+=1
        bellcnt+=1
        cnt+=1
        #print ("Frame number", framecnt)
        try:
            (grabbed, frame) = vs.read()
        except:
            break
        if frame is None:
            break
        
        if cnt == 3:
            cnt=0
            
            boxes, img = yolo.find_vehicles(frame, tiny=True)
            sizes = []
            for box in boxes:
                size = (box[2]*box[3])
                sizes.append(size)
                if (size<minsize):
                    minsize = size
                if (size>maxsize):
                    maxsize = size
                
            img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow("output", cv2.resize(img,(800, 600)))
            if len(sizes)>0:
                #print('Closest car:', max(sizes))
                if (max(sizes)>30000 and bellcnt>8):
                    print('car')
                    #playsound(mp3File)
                    winsound.PlaySound(mp3File, winsound.SND_ASYNC | winsound.SND_ALIAS )
                    bellcnt=0
            writer.write(cv2.resize(img,(800, 600)))
            fps.update()
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            #cv2.waitKey()
        else: 
            if size is not None:
                print('blub')
                x = int(box[0])
                y = int(box[1])
                x_plus_w = int(box[0] + box[2])
                y_plus_h = int(box[1] + box[3])
                color = (100, 100, min(size/100, 255))
                cv2.rectangle(frame, (x, y), (x_plus_w, y_plus_h), color, 2)
                frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
                cv2.imshow("output", cv2.resize(frame,(800, 600)))
                #time.sleep(1)
                writer.write(cv2.resize(frame,(800, 600)))
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                   break
                #cv2.waitKey()
                fps.update()
                
        
        
        
         
fps.stop()

print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()

# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()
    
        #cv2.imshow('Input', img)