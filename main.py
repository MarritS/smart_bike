# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 12:09:08 2021

@author: marri
"""


import yolo_opencv as yolo
import yolo_video as yolo_video


yolo.find_vehicles("tiny_test3.png", tiny=False)
yolo_video.find_vehicles("00108.MTS", "demo.mp4", tiny=True)
