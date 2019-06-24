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

output_channel = (33 ,31,21)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(output_channel,GPIO.OUT,initial=GPIO.LOW)  # set pin as an output pin 

actionlist = ['Dinner', 'Doing other things', 'Good', 'Home', 'No', 'No gesture', 'Pulling Hand In', 'Pulling Two Fingers In', 'Pushing Hand Away', 'Pushing Two Fingers Away', 'Rolling Hand Backward', 'Rolling Hand Forward', 'Sorry', 'Sliding Two Fingers Down', 'Sliding Two Fingers Left', 'Sliding Two Fingers Up', 'Stop Sign', 'Swiping Down', 'Swiping Left', 'Swiping Up', 'Turning Hand Clockwise', 'Turning Hand Counterclockwise', 'Zooming In With Full Hand', 'Zooming In With Two Fingers', 'Zooming Out With Full Hand', 'Zooming Out With Two Fingers']

seq_length = 30
deque_frames = deque(maxlen = seq_length)
t1 = time.time()

def sampleframes(deque_frames):
    global frame
    global t1
    while(1):       
        #Sampling at 15 FPS
        #t2 = time.time()
        #print('FPS {:.1f}'. format(1/(t2-t1)))
        #t1 = t2
        frame_local = frame
        frame_in = cv2.resize(frame_local, (112, 112),interpolation = cv2.INTER_NEAREST)
        deque_frames.append(frame_in)
        time.sleep(1.0/15)

def predict(deque_frames):
    op_dict = { 'Dinner' : (GPIO.LOW,GPIO.LOW,GPIO.HIGH), 'Good' : (GPIO.LOW,GPIO.HIGH,GPIO.LOW), 'Home' : (GPIO.LOW, GPIO.HIGH,GPIO.HIGH),
                'No' : (GPIO.HIGH,GPIO.LOW,GPIO.LOW), 'Sorry' : (GPIO.HIGH, GPIO.LOW,GPIO.HIGH) }
    actions = [ 'No','Good','Sorry','Dinner','Home' ]

    deque_actions = deque(maxlen = 2)

    #Load Model Weights
    C3DModel = c3d_super_lite()
    C3DModel.load_weights('checkpoint_models/C3DLSTM_jester_all_mak_6_aug_epoch_23.h5')

    # Ready for Inference
    GPIO.output(output_channel, (GPIO.HIGH,GPIO.HIGH,GPIO.HIGH))
    time.sleep(1)
    GPIO.output(output_channel, (GPIO.LOW,GPIO.LOW,GPIO.LOW))
    while(True):
        # Wait for Queue To Fill
        if(len(deque_frames) >= 30) :
            list_frames = list(deque_frames)
            np_predict  = np.expand_dims(list_frames, axis=0)
            #start_time  = time.time()
            prediction  = C3DModel.predict(np_predict)[0]
            onehot      = np.argmax(prediction)
            #print("predict time : ", time.time()-start_time)
            action = actionlist[onehot]
            prob   = prediction[onehot] 

            if(action in actions and prob > 0.94):
                deque_actions.append(action)
                if(len(deque_actions) >= 2 and (deque_actions[0] == deque_actions[1])):
                    deque_actions.clear()
                    print(action) 
                    GPIO.output(output_channel, op_dict[action])
                    time.sleep(0.5)
                    GPIO.output(output_channel, (GPIO.LOW, GPIO.LOW, GPIO.LOW))
                    time.sleep(2.5)  

frame = np.empty((112,112,3))

predictThread = threading.Thread(target = predict,args=(deque_frames,))
predictThread.start()

framesThread = threading.Thread(target = sampleframes,args=(deque_frames,))
framesThread.start()

capture = cv2.VideoCapture(0)
while (capture.isOpened()):
    
    ret,frame = capture.read()  
    if ret:   
        start_time = time.time()
        #print('FPS {:.1f}'. format(1/(time.time()-start_time))) 
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') :
            break
    else:
        break

capture.release()
