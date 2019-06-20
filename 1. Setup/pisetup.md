Raspberry Pi setup
==================

Ensuring Pi is running an up to date OS version
------------------------------------------------

The OS of the Pi must be checked to ensure that it is compatible with the setup described. 

In the current implementation, the Pi runs on Raspbian 1.2. Do make sure that the OS on your Pi is at least 1.2 or newer. This can be checked by entering the following command on the Pi’s terminal: `cat /etc/os-release`. 

Installation of Packages
------------------------

In the code “IBM_text_to_speech.py”, it utilises the IBM Watson text to speech function to generate the audio files. In order to use that function, the IBM Watson text to speech must first be installed onto the Pi. This is done by entering `sudo pip3 install ibm-watson` in the terminal. 

In “main.py”, the NumPy library is required to accurately determine the distance between the user and Waldo. Running  `sudo apt-get install python3-numpy` on the terminal will install the package on the Pi. 

GPIO Numbering Schemes
----------------------

The Broadcom GPIO Numbers scheme (BCM)  is used in our implementation. This scheme would mean that the pins are identified by their GPIO numbers instead of the pin numbering on the board. An example would be in "main.py” input 1 is written as 22, which corresponds to pin 15 on the Pi, which is labelled as GPIO22 instead of pin 22 on the Pi. 
