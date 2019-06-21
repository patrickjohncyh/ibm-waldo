
Machine Learning / Depp Learning
===

This section details the experimentation phase and the deployment phase of the Deep Learning model. The model is the backbone of the system, performing the crucial task of Makaton Sign Recognition. This section includes the key design decisions and the rationale behind them.


## Model Development History and Evolution

This sections explains and gives the performance of the Deep Learning models that were experimented with to determine the best model for Makaton Sign Recognition.

#### Dataset
In the experimentation phase, the [Jester Dataset](https://20bn.com/datasets/jester/v1#download) was utilised. 6 (Swiping Left,Swiping Down,Thumb Up,Drumming Fingers,Sliding Two Fingers Left,No gesture) out of the 26 Gestures available were selected and used througout all experiments. The Jester Dataset was used whilst the team was still building the Makaton Sign dataset. The use of a prebuilt dataset during the experimentation phase was critical as the dataset is large and diverse enough, providing suffucient data for Deep Learning. This lends to two important aspects in Machine Learning.

1. Training --- It is vital to have sufficient data for the training set to improve the model's ability to generalise.

2. Validation --- A validation set is used as a proxy to measure how well the model has generalised. A large validation set will ensure that the validation accuracy/loss measured is a good proxy of the true accuracy/loss of the model on unseen data.

Therefore, the Jester dataset provides confidence in the results of the experiments.

#### Experimental Results
The plot below gives a summary of the performance (accuracy) of the various models.

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/model_validation.png)

#### 1)<space> C3D

The model employs the use of 3D Convolution Networks to capture spatio-temporal features that are crucial in classifying Makaton signs that are non-static. The model achieved a validation accuracy of <b>54.25%</b> on 5+1(No action) classes on [20BN-Jester](https://20bn.com/datasets/jester) dataset.

Refer to [C3D Paper](https://arxiv.org/pdf/1412.0767.pdf) for more details


#### 2)<space> MobileNetV2 + LSTM

The model employs the use of 2D Convolution Networks pre-trained on [Imagenet](https://www.kaggle.com/c/imagenet-object-localization-challenge) and gives us a quick and lightweight method to capture spatial features. Spatial features learnt are then passed into a Long Short Term Memory(LSTM) module to further study its study time evolution. Model achieved a validation accuracy of <b>82.32%</b> on 5+1(No action) classes on 20BN-Jester dataset.

Refer to [CNN+LSTM Paper](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43455.pdf) for more details

#### 3)<space> MobileNetV2_L2Norm + LSTM

Just like <b>MobileNetV2 + LSTM</b>, this model employs the use of 2D Convolution Networks pre-trained on Imagenet. For this model, the learnt spatial features are L2 normalised to become vectors of unit length before passing them into the LSTM module. Model achieved a slight boost in validation accuracy to <b>86.35%</b> on 5+1(No action) classes on 20BN-Jester dataset.

4)<space> C3D_L2Norm + LSTM + UF4

The model employs the use of 3D Convolution Networks to capture spatio-temporal features that are crucial in classifying Makaton signs which are non-static. The learnt spatio-temporal features are then passed into the LSTM to further study its time evolution. Learning not only spatial but temporal features as well allowed the representations of makaton sings to be better captured. This facilitated a huge improvement over the <b>MobileNetV2_L2Norm + LSTM</b> model. Model achieved a validation accuracy of <b>94.64%</b> on 5+1(No action) classes on 20BN-Jester dataset.

Refer to [C3D+LSTM Paper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwiOjovI1vriAhUMilwKHVA_A8AQFjAAegQIAhAC&url=https%3A%2F%2Fwww.mdpi.com%2F1999-5903%2F11%2F2%2F42%2Fpdf&usg=AOvVaw2k7dwm_6BqK9GFhkHDnGis) for more details

#### 5)<space> C3D_L2Norm + LSTM + UF7

This is the same model as the model <b> C3D_L2Norm + LSTM + UF4 </b> above but with the final 7 layers unfrozen(3 more than UF4). This allowed the model to better learn the patterns on the Jester dataset as compared to just using the pre-trained weights that are not tuned specifically to Jester. Model achieved a validation accuracy of <b>96.69%</b> on 5+1(No action) classes on 20BN-Jester dataset.

## Model Deployment

The experimental phase allowed the team to determine which model was best suited for the task of Gesture Recognition. Based on the above results, the C3D + L2Norm + LSTM Models (Models 4 and 5) were shown to be superior over the other models. However, there were still 2 challenges to overcome.

#### 1. Deployment of Model on Jetson Nano

The model used in the experiments consisted of the full C3D model. In total, together with the LSTM componenet, the proposed model had \~ 30M Parameters. The model was run on the Jetson Nano and it was found that it had an inferece speed of \~1.25s. In other words, it could only run at 0.8 Frames Per Second (FPS). This is far too slow for real-time detection with video frames comining from a camera stream. Furthermore, with that many paramters, end-to-end training with all layers unfrozen will take extremely long.

It was therefore crucial to reduce the model size. 


#### 2. Training Model with Limited Dataset









