# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:07:14 2021

@author: marri
"""
import cv2
import yolo_return_boxes as yolo
from imutils.video import FPS
from imutils.video import VideoStream
from playsound import playsound
import winsound


fps = FPS().start()
mp3File = 'bell.mp3'
INPUT_FILE="00108.MTS"
fourcc = cv2.VideoWriter_fourcc(*"MJPG")
vs = cv2.VideoCapture(INPUT_FILE)
writer = cv2.VideoWriter("result", fourcc, 30,
        (800, 600), True)
cnt=0
bellcnt=0
framecnt=0
while True:
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
                size = (box[0] - box[1]) * (box[2] - box[3])
                sizes.append(size)
                
            img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow("output", cv2.resize(img,(800, 600)))
            if len(sizes)>0:
                #print('Closest car:', max(sizes))
                if (max(sizes)>50000 and bellcnt>4):
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
    
        #cv2.imshow('Input', img)