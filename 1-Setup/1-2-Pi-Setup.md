1.2 Raspberry Pi setup
===

This section provides a step-by-step guide on how to setup the Rasberry Pi 3 environment as used in WALDO.

## Go To
* 1.2.1 [Setting up a Raspberry Pi and OS](#121-setting-up-raspberry-pi-and-raspbian-os)
* 1.2.2 [Ensuring Pi is running an up to date OS version](#122-checking-pi-os-version)
* 1.2.3 [Installation of Packages](#123-installation-of-packages)
* 1.2.4 [GPIO Numbering Schemes](#124-gpio-numbering-schemes)

1.2.1 Setting up Raspberry Pi and Raspbian OS
---
1. A micro SD card is required to store Raspbian OS, and a power source of 5V and a minimum of 2.5A is [recommended](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/2) to power the Raspberry Pi 3. 
2. If an SD with Raspbian OS has been provided with the Pi, skip to step 4. If not, continue to step 3.
3. The first step to downloading the OS would be to head to the Raspberry Pi Downloads page from this [link](https://www.raspberrypi.org/downloads/). This link contains the files to download the NOOBS files which would be flashed into the SD card. The guide to formatting and copying of files over to the SD card can be found [here](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3). 
4. Insert the SD card into the underside of the Pi. Connect the mouse and keyboard to the USB ports on the Pi. Lastly connect the HDMI cable from the Pi to a computer display the video output. 
5. Internet connectivity can either be through an Ethernet cable or through WiFi.
6. Connect the power cable to the Pi. The video output would display a boot up screen.
7. Adjust the date and time settings and language option for the Pi.



1.2.2 Checking Pi OS Version
---

The OS of the Pi must be checked to ensure that it is compatible with the setup described. 

In the current implementation, the Pi runs on Raspbian 1.2. Do make sure that the OS on your Pi is at least 1.2 or newer. This can be checked by entering the following command on the Pi’s terminal: `cat /etc/os-release`. 

1.2.3 Installation of Packages
---

1) IBM Watson Text-to-Speech is used to generate the audio files corresponding to detected Makaton Action or preset phrase. The IBM Watson API for python3 is required for this.

To install, run the following command in Terminal,

```
sudo pip3 install ibm-watson
``` 

2) NumPy library is used to perform certain mathematical computations. 

To install, run the following command in Terminal,

```
sudo apt-get install python3-numpy
```
1.2.4 GPIO Numbering Schemes
---

The Broadcom GPIO Numbers scheme (BCM) is used in this implementation. This scheme would mean that the pins are identified by their GPIO numbers instead of the pin numbering on the board. For example, in "main.py” input 1 is written as 22, which corresponds to Pin 15 on the Pi, which is labelled as GPIO22 instead of Pin 22 on the Pi. 

The image below is provided for easy reference. It shows the numbering of pins, as well as the GPIO tagged to the pins on the board. As mentioned above, in the BCM scheme, the GPIO numbers are used instead of the actual pin numbering on the board labelled as 1-40. 

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/Raspberry%20pi%203%20GPIO_pins_v2.png "GPIO Pins")
