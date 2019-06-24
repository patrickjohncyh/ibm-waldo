3. Overview of Pi Function
=======================

To relieve the computational load imposed on the Jetson, all functions other than running the machine learning model have been offloaded to a Raspberry Pi 3 Model B. This allows the Jetson to be used to identify Makaton signs with low latency and high inference rate. The functions the Pi performs are:

* Send audio files to speaker to provide device’s speech output
* Receive information from device buttons, output user-customised responses
* Receive information from proximity sensor
* Receive information from Jetson Nano regarding state of readiness and Makaton sign identified

Hence, the Pi runs the high level logic of the device, bringing together information from the sensors, buttons and Jetson, after which it determines the appropriate output and plays it on the connected speaker.

<Br>
  
Proximity Sensor
---------------

The proximity sensor used is the Parallax PING Ultrasonic Sensor. The sensor works as follows: the I/O pin triggers an ultrasonic burst, after which it measures the time required for an echo to be received. In WALDO, the proximity sensor is used to give the user a gauge of an appropriate distance for the user to be at to use its different functions.

The diagram below shows the functions corresponding to the different ranges between WALDO and the user.

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/sensor_ranges.png "Sensor Ranges")

<Br>
  
The device is disabled if the proximity sensor is blocked, since it detects a range of less than 5cm. Between 5 and 55cm, the user can use the buttons. Between 55 and 70cm, WALDO interprets the user’s intention to be to perform Makaton interpretation, and directs them to stand further away to ensure that the user’s sign can be properly captured by the camera. If the user is further than 70cm away, Makaton interpretation is carried out and the relevant output is transmitted to the speaker.

<Br>
  
Function of Buttons
-------------------

WALDO has 4 hardware buttons. When one is pressed, the Pi detects the button press and plays the correct audio file using the connected speaker. This process is described by the flow diagram below.

<Br>

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/audio_flow.png "Logic flow diagram for audio output from Pi")

The IBM_text_to_speech.py code employs IBM Watson text-to-speech on Python to generate the audio files. The contents of the audio files can be edited to tailor the needs of the users by simply modifying or adding to the “predefined_actions” list in the code. The generated audio files are saved in a pre-determined folder on the Pi. In main.py, when a button is pressed, the relevant audio file is accessed and played via the speaker.

<Br>
  
Communication with Jetson
-------------------------

Makaton interpretation using machine learning has been implemented on the Jetson. As the output device, the speaker, is connected to the Pi, the Jetson needs to send the appropriate data to the Pi to produce the correct output. As only 7 messages are required in the present implementation, only 3 bits are necessary. Hence, the Jetson is connected to the Pi using 3 GPIO pins, as shown in the table below.

<Br>
  
|**Bit**|**Pin on Jetson**|**Pin on Pi**|
|-------|-----------------|-------------|
|Most significant|Pin 33 (GPIO38)|Pin 19 (GPIO10)|
|Middle|Pin 31 (GPIO200)|Pin23 (GPIO11)|
|Least significant|Pin 21 (GPIO17)|Pin21 (GPIO9)|

<Br>
  
When the Jetson has successfully booted up, a bit sequence of ‘111’ is transmitted to the Pi, producing an audio output of “I’m Ready”, letting the user know that the system is ready for use.

 <Br>

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/jetson_to_pi.png "Pin connection between Jetson and Pi")

<Br>

If the number of signs that can be interpreted increases, more GPIO pins can be used for communication.

<Br>

Overall Pi Function
-------------------

The logic flow diagram below describes the overall normal function of the Pi in WALDO.

<Br>

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/pi%20logic.jpg "Pi logic flow diagram")
