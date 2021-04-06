# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 21:26:16 2021

@author: marri
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 20:43:55 2021

@author: marri
"""

#############################################
# Object detection - YOLO - OpenCV
# Author : Arun Ponnusamy   (July 16, 2018)
# Website : http://www.arunponnusamy.com
############################################


import cv2
import argparse
import numpy as np




def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes):

    label = str(classes[class_id])
    
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
def find_vehicles(image, tiny):
    
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    
    classes = None
    
    with open('yolov3.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    

    if tiny:
         net = cv2.dnn.readNet('yolov2-tiny.weights', 'yolov3-tiny.cfg')
    else:     
        net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
   
    
    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
    
    net.setInput(blob)
    
    outs = net.forward(get_output_layers(net))
    
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    
    
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    cars = {}
    
    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        crop_image = image[round(y):round(y)+h, round(x):round(x)+w]
        #cv2.imshow("", crop_image)
        #cv2.waitKey()
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), classes)
        #cv2.destroyAllWindows()

    
    #cv2.imshow("object detection", image)
    #cv2.waitKey()
    return boxes, image
        
    #cv2.imwrite("object-detection.jpg", image)
    #cv2.destroyAllWindows()
