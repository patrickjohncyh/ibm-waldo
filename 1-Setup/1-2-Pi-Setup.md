1.2 Raspberry Pi setup
==================
Setting up a Raspberry Pi and OS :

1. A micro SD card is required to store Raspbian OS, and a power source of 2.5W is required to boot up the Raspberry Pi. 
2. Most sellers would have prepared an SD card with the Pi that is set up with Raspbian OS. If the sellers have provided an SD card with the OS, skip to step 5, if not, continue to step 3.
3. The first step to downloading the OS would be to head to the Raspberry Pi Downloads page from this link:  https://www.raspberrypi.org/downloads/  This link contains the files to download the NOOBS files which would be flashed into the SD card. The guide to formatting and copying of files over to the SD card can be found here:  https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3
4. After the files have been extracted and copied into the Pi, start to connect the Pi up. 
5. Insert the SD card into the underside of the Pi. Connect the mouse and keyboard to the USB ports on the Pi. Lastly connect the HDMI cable from the Pi to a monitor or a TV screen for the video output. 
6. An ethernet cable can be connected to the Pi if you wish to use the ethernet cable for internet connection. This might not be necessary as Raspberry Pi 3 should be able to connect wirelessly via WiFi.
7. Connect the power cable to the Pi. With all prior steps done, the video output would display a boot up screen and the Pi would be fully loaded on.  
8. The final step to the set up would be to adjust the time and date setting as well as a language option for the Pi. With all these done, the Pi is set up and ready to go. 


## Go To
* 1.2.1 [Ensuring Pi is running an up to date OS version](#121-ensuring-pi-is-running-an-up-to-date-os-version)
* 1.2.2 [Installation of Packages](#122-installation-of-packages)
* 1.2.3 [GPIO Numbering Schemes](#123-gpio-numbering-schemes)

<Br>
  
1.2.1 Ensuring Pi is running an up to date OS version
------------------------------------------------

The OS of the Pi must be checked to ensure that it is compatible with the setup described. 

In the current implementation, the Pi runs on Raspbian 1.2. Do make sure that the OS on your Pi is at least 1.2 or newer. This can be checked by entering the following command on the Pi’s terminal: `cat /etc/os-release`. 

<Br>

1.2.2 Installation of Packages
------------------------

In the code “IBM_text_to_speech.py”, it utilises the IBM Watson text to speech function to generate the audio files. In order to use that function, the IBM Watson text to speech must first be installed onto the Pi. This is done by entering `sudo pip3 install ibm-watson` in the terminal. 

In “main.py”, the NumPy library is required to accurately determine the distance between the user and Waldo. Running  `sudo apt-get install python3-numpy` on the terminal will install the package on the Pi. 

<Br>

1.2.3 GPIO Numbering Schemes
----------------------

The Broadcom GPIO Numbers scheme (BCM)  is used in our implementation. This scheme would mean that the pins are identified by their GPIO numbers instead of the pin numbering on the board. An example would be in "main.py” input 1 is written as 22, which corresponds to pin 15 on the Pi, which is labelled as GPIO22 instead of pin 22 on the Pi. 

<Br>

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/Raspberry%20pi%203%20GPIO_pins_v2.png) "GPIO Pins")
