import RPi.GPIO as GPIO
import time
import os
import math
import numpy
from collections import deque
import sys

input1 = 22 
input2 = 27
input3 = 17
input4 = 5

input_us = 14

makin3 = 9  #lsb
makin2 = 11
makin1 = 10 #msb

def playSound(fileNum):
        os.system('aplay ' + 'audio_files/'+str(fileNum)+ '.wav')

def main():
    print('Script Running')
    sys.stdout.flush()
    GPIO.setmode(GPIO.BCM) #BCM pin numbering scheme from Pi
    
    GPIO.setup(input1, GPIO.IN)
    GPIO.setup(input2, GPIO.IN)
    GPIO.setup(input3, GPIO.IN)
    GPIO.setup(input4, GPIO.IN)

    GPIO.setup(makin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(makin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(makin3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    distarray = deque(maxlen=5)                
    mak1 = 0
    mak2 = 0
    mak3 = 0
    #while((mak1,mak2,mak3)!=(1,1,1)):
    while(0):
        mak1 = GPIO.input(makin1)
        mak2 = GPIO.input(makin2)
        mak3 = GPIO.input(makin3)
        #print((mak1,mak2,mak3))
        time.sleep(0.1)

    playSound(7)
    print('Jetson Initialised')
    sys.stdout.flush()

    while True:

        # Read Inputs
        value1 = GPIO.input(input1)
        value2 = GPIO.input(input2)
        value3 = GPIO.input(input3)
        value4 = GPIO.input(input4)
        mak1 = GPIO.input(makin1)
        mak2 = GPIO.input(makin2)
        mak3 = GPIO.input(makin3)

        # Read Ultrasonic
        GPIO.setup (input_us, GPIO.OUT)
        GPIO.output(input_us, False)
        GPIO.output(input_us, True )
        GPIO.output(input_us, False)
        GPIO.setup(input_us,GPIO.IN)

        while GPIO.input(14) == 0:
            start_time = time.time()

        while GPIO.input(14) == 1:
            end_time = time.time()
            duration = end_time - start_time
            distance = duration * 34000 / 2
            distarray.append(math.floor(distance))
        
        # Use Median of Last 5 Readings
        finalDist = numpy.median(distarray)
                
        if finalDist < 5:
            time.sleep(0.1)
        else:
            if value1:
                playSound(0)
            elif value2:
                playSound(1)
            elif value3:
                playSound(2)
            elif value4:
                playSound(3)

            if(finalDist>=55 and finalDist<70):                
                playSound(5)

            if(finalDist>=70):
                if((mak1,mak2,mak3) == (0,0,1)):
                    playSound('Dinner')
                elif((mak1,mak2,mak3) == (0,1,0)):
                    playSound('Good')
                elif((mak1,mak2,mak3) == (0,1,1)):
                    playSound('Home')
                elif((mak1,mak2,mak3) == (1,0,0)):
                    playSound('No')
                elif((mak1,mak2,mak3) == (1,0,1)):
                    playSound('Sorry')
            time.sleep(0.25)

if __name__ == '__main__':
    main()
