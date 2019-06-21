
Server environment setup for further model training
===

Installing Nvidia Driver, CUDA and cuDNN
---

You may refer to this [link](https://medium.com/@zhanwenchen/install-cuda-and-cudnn-for-tensorflow-gpu-on-ubuntu-79306e4ac04e) for step-by-step instructions on installing and setting up your Nvidia driver, CUDA and cuDNN to exploit GPU capabilities for machine learning training.


Note : Versions listed on that site may be outdated, but you can check their compatibility via these sites - [Nvidia Driver and CUDA compatibility](https://stackoverflow.com/questions/30820513/what-is-the-correct-version-of-cuda-for-my-nvidia-driver/30820690#30820690) and [CUDA and cuDNN compatibility](https://docs.nvidia.com/deeplearning/sdk/cudnn-support-matrix/index.html)

The steps from the link above may be summarised as follows:

1. Install Nvidia Driver on your machine via `sudo apt-get install nvidia-410 nvidia-modprobe` (We used V410.48, you can enter `nvidia-smi` on terminal to check your existing Nvidia Driver version if you already have one.

2. Download and Install a version of CUDA that is compatible with your Nvidia driver (We used CUDA V10.0 and enter `nvcc --version` to check if you already have CUDA).

3. Download and Install a version of cuDNN that is compatible with the CUDA version you installed. (We used CUDNN 7.5.0 and you may enter `CUDNN_H_PATH=$(whereis cudnn.h)` followed by `cat ${CUDNN_H_PATH} | grep CUDNN_MAJOR -A 2` to check your cuDNN version if you already have cuDNN installed.
<br>

Installing Nvidia Driver, CUDA and cuDNN
---
We used Python v3.5.2 but we recommend v3.6.8 or the latest version for compatibility with performing inference on Jetson Nano.

1.  Ensure python3 version is up to date and at least 3.6.8 (run `python3 -v` to verify)
 
2.  Get pip3 by entering `sudo apt-get install python3-pip`

3.  From the MachineLearning folder directory, run the following command to install the required python3 packages on to the server/machine for further training : `pip3 install -r requirements.txt`

Below is a summary of the main packages required and the versions we used for model training:

h5py==2.9.0 

Keras==2.2.4

Keras-Applications==1.0.7

Keras-Preprocessing==1.0.9

matplotlib==3.0.3

numpy==1.16.3

pandas==0.24.2

Pillow==6.0.0

scikit-learn==0.20.3

scipy==1.2.1

tensorflow==1.13.1

tensorflow-gpu==1.13.1

tqdm==4.31.1

