import cv2
import numpy as np
from collections import deque
import tensorflow as tf
import keras.backend as K
from keras.models import load_model,Model
from keras.layers import Input
from Models import c3d_super_lite,c3d_super_lite_sw
from keras.preprocessing import image
import os
import time
from threading import Timer
import threading

import sys
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/')
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')

import Jetson.GPIO as GPIO
import time

output_channel = (33,31,21)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(output_channel,GPIO.OUT,initial=GPIO.LOW)  # set pin as an output pin 

actionlist = ['D', 'Doing other things', 'G', 'H', 'N', 'No gesture', 'Pulling Hand In', 'Pulling Two Fingers In', 'Pushing Hand Away', 'Pushing Two Fingers Away', 'Rolling Hand Backward', 'Rolling Hand Forward', 'S', 'Sliding Two Fingers Down', 'Sliding Two Fingers Left', 'Sliding Two Fingers Up', 'Stop Sign', 'Swiping Down', 'Swiping Left', 'Swiping Up', 'Turning Hand Clockwise', 'Turning Hand Counterclockwise', 'Zooming In With Full Hand', 'Zooming In With Two Fingers', 'Zooming Out With Full Hand', 'Zooming Out With Two Fingers']

seq_length = 30
deque_frames = deque(maxlen = seq_length)
t1 = time.time()
while(1):
    # Ready for Inference
    GPIO.output(output_channel, (GPIO.HIGH,GPIO.LOW,GPIO.LOW))
   
