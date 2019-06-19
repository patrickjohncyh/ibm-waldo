Raspberry Pi setup
==================

Ensuring Pi is running on the same version of OS
------------------------------------------------

The OS of the Pi must be checked to ensure that it is compatible with the setup described. 

In the current implementation, the Pi runs on Raspbian 1.2 OS. The OS release date can be checked by reading the content of the OS - release file. This can be done via the following command on the Pi’s terminal: `cat /etc/os-release`. 

Installation of Packages
------------------------

In the code “sound_to_text.py”, it utilises the IBM Watson text to speech function to generate the audio files. In order to use that function, the IBM Watson text to speech must first be installed onto the Pi. This is done by entering `sudo pip3 install ibm-watson` in the terminal. 

In “switchtest.py”, the NumPy library is required to accurately determine the distance between the user and Waldo. Running  `sudo apt-get install python3-numpy` on the terminal will install the package on the Pi. 

GPIO Numbering Schemes
----------------------

The Broadcom GPIO Numbers scheme (BCM)  is used in our implementation. This scheme would mean that the pins are identified by their GPIO numbers instead of the pin numbering on the board. An example would be in “switchtest.py” input 1 is written as 22, which corresponds to pin 15 on the Pi, which is labelled as GPIO22 instead of pin 22 on the Pi. 
