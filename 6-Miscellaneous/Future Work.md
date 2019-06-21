
# Future Work

  

## Discussion of Present Implementation

  

The table below shows the capabilities of WALDO that have and have not been implemented.

| No. 	| Capability                                                        	| Status                                                                                                                              	|
|-----	|-------------------------------------------------------------------	|-------------------------------------------------------------------------------------------------------------------------------------	|
| 1.  	| Makaton interpretation using machine learning                     	| **Implemented** - Interpretation of 5 signs with high accuracy and low latency.<br> **Not Implemented** - Interpretation of other Makaton signs 	|
| 2.  	| Buttons to output pre-set expressions                             	| **Implemented**                                                                                                                         	|
| 3.  	| User interface to change what expressions button presses output   	| **Not Implemented** - Strings that buttons output cannot be changed remotely, no user interface to change string output                 	|
| 4.  	| Ambient sensors to analyse and understand the user’s surroundings 	| **Not Implemented**                                                                                                                     	|
| 5.  	| Replicability of product                                          	| **Not Implemented** - Components are for prototyping use; low replicability of product                                                  	|

<Br>

## Improvements to Present Hardware

  

Presently, WALDO faces several challenges arising from the limited capabilities its hardware components can offer, namely:

  

-   The Nvidia Jetson Nano used for Makaton interpretation is a developer kit meant for rapid prototyping, and has insufficient RAM to run a larger and more complex model
    
-   The battery pack used, a Krisdonia 25000mAh battery pack, is unable to handle power surges from the Jetson when at its full computing potential, causing the battery pack to shut off power as a safety mechanism. Hence, the Jetson is run with only 3 out of its 4 cores, and at a clock speed lower than its maximum operating frequency
    
-   Several functions of WALDO have been offloaded to a Raspberry Pi to relieve computational load on the Jetson. This increases the amount of physical electronic hardware that has to be placed in the toy
    
<Br>
  

Using purpose-built electronic components in WALDO, with higher GPU RAM and more CPU cores or higher clock speeds, would obviate the need for two embedded devices to be present, reducing the physical space needed within the toy for electronic hardware and reducing the chance of failure of one of the components. In addition, using an appropriate battery, instead of a battery pack with a built-in safety mechanism, would allow computation to be performed at the embedded device’s full potential. A safety mechanism with a higher threshold could be used with the battery to ensure safety is not compromised.

  

The external physical components of WALDO could also stand to be improved. Improvements include sewing the electronic hardware onto the cotton of the device to improve robustness against rough handling, including a zip to allow easy access to WALDO’s interior devices, sewing holes into WALDO’s exterior to allow for convenient access to ports, and adding a physical on-off switch or a camera shutter for privacy.

<Br>  

## Additional Capabilities

  

The first, and most apparent, area in which WALDO could stand to be improved is in increasing the number of signs it can recognise. However, this is a time-consuming process due to the lack of an online Makaton database with which to train the machine learning model. As such, the following changes could be made to the data collection process if the number of signs to be recognised is to be drastically increased.

  

-   Use an institutionally-supported mechanism to collect training data. One method would be to offer volunteers a small amount of cash each, while keeping it within an educational institution. Another method would be to outsource data collection to a third party, such as through the use of Amazon’s Mechanical Turk[1], an online outsourcing platform where volunteers are paid for their effort.
    
-   Using machine learning or pattern recognition to automatically preprocess videos for training. This process was hugely time-consuming when performed manually.
    
-   Sourcing data from around the world, instead of only within the UK, to improve robustness of sign recognition
    
<Br>
  

Another capability that could be integrated into WALDO’s Makaton interpretation is the ability to learn on-the-go. Presently, WALDO uses a pre-trained model and does not retain user data for additional training. If WALDO is used by an individual user for an extended period of time, on-the-go learning could be implemented to enable predictions to improve over time.

  

However, implementing such a feature on WALDO faces several problems, which are not insurmountable. Firstly, there would have to be a mechanism by which the user labels the signs he is performing. This could be done through a feedback system, whereby the user provides positive or negative feedback to WALDO based on whether the prediction is correct. This feedback mechanism would in turn have to be implemented. Secondly, on-the-go learning raises a privacy concern as the user’s data would have to be stored, and may have to be uploaded to a remote server if WALDO does not have sufficient computing power to train the machine learning model. This could be addressed by clearer privacy guidelines on WALDO’s use and strict encryption protocols.

A user interface to change the expressions WALDO outputs when its buttons are pressed has not been implemented. Since both the Pi and the Jetson have Internet connectivity, implementing this function should be straightforward; the interface could either be a webpage or a phone app. The user (or carer) would change the expression to be output, which would in turn change the string passed into the IBM Watson text-to-speech software.

  

Ambient sensors to analyse and understand the user’s environment have yet to be implemented. These sensors could be integrated with the Pi, sending information via the GPIO pins or tailor-made breakout boards and stored on the Pi for later analysis by medical professionals. Understanding the environment and possible risk factors is important in caring for people with learning disabilities[2], hence sensors that could be implemented include ambient light, sound and temperature sensors.

<Br>

## Bibliography

  

[1] Amazon. Overview. *Amazon Mechanical Turk.* [Online] Available from: https://www.mturk.com/ [Accessed: 18 June 2019].

  

[2] National Institute for Health and Care Excellence. (2015) NG11. *Challenging behaviour and learning disabilities: prevention and interventions for people with learning disabilities whose behaviour challenges.* NICE. 
