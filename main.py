# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 12:09:08 2021

@author: marri
"""


import yolo_opencv as yolo
import yolo_video as yolo_video
import imutils
from imutils.video import FPS
from imutils.video import VideoStream

yolo.find_vehicles("test4.png")
yolo_video.find_vehicles("test_short.mp4", "Output_short.mp4")
