
2.1 Machine Learning / Deep Learning
===

This section details the experimentation phase and the deployment phase of the Deep Learning model. The Deep Learning model forms the backbone of WALDO as it performs the crucial task of Makaton Sign Recognition. This section includes the key design decisions and the rationale behind them.

## Go To
* 2.1.1 [Model Development History and Evolution](#211-model-development-history-and-evolution)
* 2.1.2 [Model Deployment](#212-model-deployment)
* 2.1.3 [Conclusion](#213-conclusion)


## 2.1.1 Model Development History and Evolution

This section explains and provides the performance of the Deep Learning models that were experimented with to determine the best model for Makaton Sign Recognition.

#### 2.1.1.1 Dataset
In the experimentation phase, the [Jester Dataset](https://20bn.com/datasets/jester/v1#download) was utilised. 6 (Swiping Left,Swiping Down,Thumb Up,Drumming Fingers,Sliding Two Fingers Left,No gesture) out of the 26 Gestures available were selected and used througout all experiments. The Jester Dataset was used whilst the team was still building the Makaton Sign dataset. The use of a prebuilt dataset during the experimentation phase was critical as the dataset is large and diverse enough, providing suffucient data for Deep Learning. This lends to two important aspects in Machine Learning.

1. Training --- It is vital to have sufficient data for the training set to improve the model's ability to generalise.

2. Validation --- A validation set is used as a proxy to measure how well the model has generalised. A large validation set will ensure that the validation accuracy/loss measured is a good proxy of the true accuracy/loss of the model on unseen data.

Therefore, the Jester dataset provides confidence in the results of the experiments.

#### 2.1.1.2 Experimental Results
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

#### 4)<space> C3D_L2Norm + LSTM + UF4

The model employs the use of 3D Convolution Networks to capture spatio-temporal features that are crucial in classifying Makaton signs which are non-static. The learnt spatio-temporal features are then passed into the LSTM to further study its time evolution. Learning not only spatial but temporal features as well allowed the representations of makaton sings to be better captured. This facilitated a huge improvement over the <b>MobileNetV2_L2Norm + LSTM</b> model. Model achieved a validation accuracy of <b>94.64%</b> on 5+1(No action) classes on 20BN-Jester dataset.

Refer to [C3D+LSTM Paper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwiOjovI1vriAhUMilwKHVA_A8AQFjAAegQIAhAC&url=https%3A%2F%2Fwww.mdpi.com%2F1999-5903%2F11%2F2%2F42%2Fpdf&usg=AOvVaw2k7dwm_6BqK9GFhkHDnGis) for more details

#### 5)<space> C3D_L2Norm + LSTM + UF7

This is the same model as the model <b> C3D_L2Norm + LSTM + UF4 </b> above but with the final 7 layers unfrozen(3 more than UF4). This allowed the model to better learn the patterns on the Jester dataset as compared to just using the pre-trained weights that are not tuned specifically to Jester. Model achieved a validation accuracy of <b>96.69%</b> on 5+1(No action) classes on 20BN-Jester dataset.

## 2.1.2 Model Deployment

The experimental phase allowed the team to determine which model was best suited for the task of Gesture Recognition. Based on the above results, the C3D + L2Norm + LSTM Models (Models 4 and 5) were shown to be superior over the other models. However, there were still 2 challenges to overcome.

#### 2.1.2.1 Deployment of Model on Jetson Nano

The model used in the experiments consisted of the full C3D model. In total, together with the LSTM componenet, the proposed model had \~ 30M Parameters. The model was run on the Jetson Nano and it was found that it had an inferece rate of \~1.25 inferences/s. In other words, it could only run at 0.8 Frames Per Second (FPS). This is far too slow for real-time detection with video frames comining from a camera stream. Furthermore, with that many paramters, end-to-end training with all layers unfrozen will take extremely long.

It was therefore crucial to reduce the model size. This was achieved by tweaking the model in several ways.

Firstly, considering that 3D Convolution is computationally expensive, the last 2 3D Convolutional layers were removed.

Another aspect of convolution that can lead to computational savings is the number of output filters of the convolution operation. Theoretically, the computational complexity of each layer should scale linearly with the number of output filters. In reality, the computational savings may not be exactly linear due to optimizations applied by cuDNN on GPU hardware. Nevertheless, with the goal of improving inference rate, the number of filters for first 4 Convlutional layers was reduced by a factor of 2 and the by a factor of 4 for the last 2 layers.

Lastly, the dimensions (Width x Height x Depth) of the input to a convolution is another factor that determines its speed. The input layer has dimensions (30,112,112,3) and the input convolution in the original C3D model has strides (1,1,1) (D,W,H), padding set to 'same' and 64 output filters. Therefore it's output would be of shape (30,112,112,64). The sheer size of this layer will trickle down the rest of the model. Therefore, the first convolutional layer was modified to have stirdes (1,2,2) i.e stride 1 along the temporal domain, and stride 2 along the spatial domain, and the number of output filters halved, reducing its output to shape (30,56,56,32), a reduction by a factor of 4.

After applying the above modifications, the model was observed to have \~3M parameters. The model was then run on the Jetson Nano and an infernece rate of \~0.125 inferences/s or 8 FPS was observed. Sufficient for smooth, real-time gesture detection.

To test the limits of the minimized model, it was trained with the training data (118,562 samples) from the Jester Dataset which had 27 classes. We used 80% of the training data as the training set and 20% of the training data as the validation set. The model was trained for 5 epochs and it had obtained a training accuracy of 88% and a validation accuracy of 87%. We don’t believe that the model had overfitted yet (meaning that it was possible that the training and validation accuracy could still rise), but this provided sufficient evidence of the models’ capacity and capabilities.

#### 2.1.2.2 Training Model with Limited Dataset

Given the time constraints, the collected dataset was not as large and diverse as that of the Jester Dataset. The dataset collection process is detailed [here](https://github.com/patrickjohncyh/ibm-waldo/blob/master/5-Administrative/data_collection.md). We were only able to collect a total of 175 videos per class (5 in this case) for our training set. Of the 175 videos, 70 of them were of the three group members tasked with data collection, leaving 105 videos per class that is of random people. For our validation set, we had 50 videos per class, all of which are of random people.

The model was trained on our dataset with 6 classes (5 actions + 1 no gesture). It was able to achieve a training accuracy of 98.8% and a validation accuracy of 91.6%. This appeared to be a very positive result, but we were wary of the fact that our validation set had only a total of 300 samples.

Data augmentation was deployed to circumvent the problem of limited data. Data augmentation is a technique to artificially create new training data from existing training data. We performed this by applying the same affine transformations to all the frames of a given video sample that is 30 frames in length. This involved random translation (+/- 20% in x and y axis) , scaling (80%-120%), rotation (+/- 5 deg) and shear (+/- 5 deg) within the ranges specified. In addition, contrast normalization (0.75-1.5) and additive gaussian noise were also introduced.

Additionally, data from the Jester Dataset was also integrated into the model. Therefore, on top of the augmented data, the model was also trained with non-conflicting actions (i.e there is a _Thumb Up_ in Jester which clashes with the _Good_ action). Having more data from both our augmented dataset and the Jester dataset would enable the model to better learn the important spatio-temporal features for gesture recognition. Having additional gestures from Jester would force the model to learn a better representation of the gestures and to also focus on the salient parts of the data that are most pertinent to recognising gestures.

## 2.1.3 Conclusion

The model is able to achieve a peak validation accuracy of 89.5%. Whilst at first glance, this may seem like a downgrade from the 91.6% obtained without augmentation, it is important to point out that the 89.5% validation accuracy was obtained over 26 classes (3 times more classes that before) and also on substantially more data (22,462 samples). This gave confidence that the validation loss and accuracy reflects well the model’s out of sample performance.

Below is the plot of the final learning curve. The model used is **c3d_super_lite**, trained for 30 Epochs on the Jester Dataset combined with the collected dataset of 5 Makaton Signs. Augmentation was applied so the ratio of samples from each class was 1:1 across both datasets. **Adam** optimiser was used with **categorical crossentropy** as loss. The best model had a validation loss of 0.3683 and a validation accuracy of 0.9038.

Actions used:
```
['Dinner', 'Doing other things', 'Good', 'Home', 'No', 'No gesture', 'Pulling Hand In', 'Pulling Two Fingers In', 'Pushing Hand Away', 'Pushing Two Fingers Away', 'Rolling Hand Backward', 'Rolling Hand Forward', 'Sorry', 'Sliding Two Fingers Down', 'Sliding Two Fingers Left', 'Sliding Two Fingers Up', 'Stop Sign', 'Swiping Down', 'Swiping Left', 'Swiping Up', 'Turning Hand Clockwise', 'Turning Hand Counterclockwise', 'Zooming In With Full Hand', 'Zooming In With Two Fingers', 'Zooming Out With Full Hand', 'Zooming Out With Two Fingers']
```
The training log has been provided in this directory.

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/final_training_curve.png)

