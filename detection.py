import cv2
import numpy as np
import argparse
import time

def detectPerson(confidenceThresholdLabel):

    label = -3
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "table",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "screen"]

    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")
    # optionally use DNN_TARGET_OPENCL_FP16
    # net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

    cap=cv2.VideoCapture(0)
    try:
        if cap.isOpened():
            try:
                ret,frame=cap.read()
            except cv2.error:
                return -2
            (h, w) = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob)
            detections = net.forward()
            for i in np.arange(0, detections.shape[2]):
                label = "0"
                confidence = detections[0, 0, i, 2]
                idx = int(detections[0, 0, i, 1])
                if confidence > confidenceThresholdLabel:
                    label = "{}:{:.2f}%".format(CLASSES[idx], confidence * 100)

    # for when the camera reads null
    except AttributeError as e:
        return -1

    cap.release()
    return label
