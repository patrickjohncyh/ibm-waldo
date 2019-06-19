Overview of Pi Function
=======================

To relieve the computational load imposed on the Jetson, all functions other than running the machine learning model have been offloaded to a Raspberry Pi 3 Model B. This allows the Jetson to be used to identify Makaton signs with low latency and high inference rate. The functions the Pi performs are:

* Send audio files to speaker to provide device’s speech output
* Receive information from device buttons, output user-customised responses
* Receive information from proximity sensor
* Receive information from Jetson Nano regarding state of readiness and Makaton sign identified

Hence, the Pi runs the high level logic of the device, bringing together information from the sensors, buttons and Jetson, after which it determines the appropriate output and plays it on the connected speaker.

Proximity Sensor
---------------

The proximity sensor used is the Parallax PING Ultrasonic Sensor. The sensor works as follows: the I/O pin triggers an ultrasonic burst, after which it measures the time required for an echo to be received. In WALDO, the proximity sensor is used to give the user a gauge of an appropriate distance for the user to be at to use its different functions.

The diagram below shows the functions corresponding to the different ranges between WALDO and the user.

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/Test%20folder/sensor_ranges.png "Pi function at different ranges from ultrasonic sensor")

The device is disabled if the proximity sensor is blocked, since it detects a range of less than 5cm. Between 5 and 55cm, the user can use the buttons. Between 55 and 70cm, WALDO interprets the user’s intention to be to perform Makaton interpretation, and directs them to stand further away to ensure that the user’s sign can be properly captured by the camera. If the user is further than 70cm away, Makaton interpretation is carried out and the relevant output is transmitted to the speaker.

