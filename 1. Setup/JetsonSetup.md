
Jetson Nano Setup
===

Operating System Setup
---

1. Prepare microSD card(Minimum requirement 16GB UHS-1 microSD) and plug-in power supply(20 W). A high speed microSD card is critical in the smooth running of the OS.
2. Download and flash with Jetson Nano Developer Kit SD Card Image on microSD Card following the instructions from this link : https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write
3. Place the Jetson Nano module on top of the paper stand provided and insert the microSD card (with system image already written to it) into the slot on the underside of the Jetson Nano module. 
4. Connect and power on computer display via HDMI to HDMI or HDMI to DVI. Connect a keyboard and a mouse to Jetson Nano and finally power on the Jetson Nano.
5. After completing the initial setup, log in and you should see this screen :

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/jetson_initial.png "")

Network Connectivity Setup
---
1. Prepare Edimax EW-7811UN-N150 Wi-Fi USB Adaptor and an Ethernet cable.
2. Connect the Jetson Nano using the Ethernet cable.
3. Official built-in driver for EW-7811UN adaptor supports Linux kernel up to v3.9 only. For all other Linux kernels beyond v3.9, install the open source driver from github using a Command Line Interface(CLI) in a Terminal following the steps from this [link](https://askubuntu.com/questions/551522/netis-wf2120-wifi-adapter-drops-signal-within-seconds/551648#551648).
5. If Wi-Fi does not appear to connect, consider removing the Ethernet cable and trying again. During installation phase, it is advised to use Ethernet to ensure a consistent internet connection


Fan Cooling Setup
---
Adding a cooling fan will keep the Jetson from overheating and potentially stalling. To automatically initialise the cooling fan, a `cronjob` is added to call the `jetson_clocks` script at boot.
1. `$ sudo crontab -e`. You may be prompted for your password.
2. If this is your first time using a cronjob, select `nano` as your editor.
3. Add `@reboot /usr/bin/jetson_clocks` to the bottom of the file
4. `crtl-x` to exit, `Y` to confirm save and `Enter`
5. `$ sudo reboot`

Power Mode Selection
---
If facing power issues when running on a battery pack. The operating mode of the Jetson Nano can be altered to use less power.

1. To check the current operating model (default is Mode 0 NMAX)
`$ /usr/sbin/nvpmodel -q`

2. To set the model to Mode 1 5W,
`$ /usr/sbin/nvpmodel -m 1`
3. To make Mode 1 default,
	1. `$ sudo nano /etc/nvpmodel/nvpmodel_t210_jetson-nano.conf`
	2. At the bottom of the file, change ‘PM_CONFIG DEAFULT=N’, where N is the desired Mode (i.e 0 or 1)
4. It is possible to create a custom operating mode based on your requirements. For further information please refer to the official [documentation](https://docs.nvidia.com/jetson/l4t/index.html#page/Tegra%2520Linux%2520Driver%2520Package%2520Development%2520Guide%2Fpower_management_nano.html%23).
 
Tensorflow Installation
---
Adapted from https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

6. Update and upgrade apt-get,
`sudo apt-get update`
`sudo apt-get upgrade`

7. Install system packages as required by TensorFlow:
`$ sudo apt-get install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev`

8. Install pip3
`$ sudo apt-get install python3-pip`

9. Install required python3 packaged for Tensorflow
`$ sudo pip3 install -U numpy grpcio absl-py py-cpuinfo psutil portpicker six mock requests gast h5py astor termcolor protobuf keras-applications keras-preprocessing wrapt google-pasta`

10. Install the NVIDIA release of tensorflow-gpu for Jetson Nano
`$ sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v42 tensorflow-gpu==$1.13.1+nv NEED CHECK`

11. Verify that tensorflow-gpu is installed by importing into python3
`$ python3`
`$ import tensorflow`


OpenCV Installation
---

It is important to install OpenCV from source so as to reap the benefits of CUDA GPU acceleration.

1. Navigate to the waldo directory

2. Run the installation script for OpenCV
`sudo ./install_opencv4.0.0_Nano.sh .`

Script obtained from https://github.com/AastaNV/JEP/blob/master/script/install_opencv4.0.0_Nano.sh

Jetson GPIO Installaton
---

Installing Jetson GPIO for python3.6 will enable control of the Jetson GPIO pins with python.
1. `sudo pip3 install  PUT ACTUAL PACAKGE HERE`


GPU/CPU RAM Expansion using Swap File
---
The Jetson Nano’s RAM is shared between the CPU and the GPU. To ensure that there is sufficient RAM for both, the Swap File is activated. This allows the SD card memory to be temporarily used as RAM.

To increase the amount of RAM available on Jetson Nano, (Only about \~2.7GB left after allocation to kernel) go to the following site and follow the instructions provided :
https://www.jetsonhacks.com/2019/04/14/jetson-nano-use-more-memory/


GPU Verification
---
Run `python3 sanity/tf-test.py` to verify that the Jetson Nano GPU is being utilised by tensorflow.

Running the Model
---
To start the demo, run the following command in terminal, run `python3 demo.py`