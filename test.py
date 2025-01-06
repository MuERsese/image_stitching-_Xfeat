import cv2
import numpy as np
import matplotlib.pyplot as plt
from modules.xfeat import XFeat

cap = cv2.VideoCapture('output.mp4')
if not cap.isOpened():
    print("Error: can't open video file")
    
else:
    print("Video file opened successfully.")
while True:
    ret, current = cap.read()
    if not ret:
        print("Error: can't get frame")
        break  # Exit the loop if there's an error