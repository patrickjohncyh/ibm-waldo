
Model History and Evolution
===

![alt text](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/model_validation.png)

1)<space> C3D
---
The model employs the use of 3D Convolution Networks to capture spatio-temporal features that are crucial in classifying Makaton signs that are non-static. Model achieved a validation accuracy of <b>54.25%</b> on 5+1(No action) classes on [20BN-Jester](https://20bn.com/datasets/jester) dataset.

Refer to [C3D Paper](https://arxiv.org/pdf/1412.0767.pdf) for more details
<br>

2)<space> MobileNetV2 + LSTM
---
The model employs the use of 2D Convolution Networks pre-trained on [Imagenet](https://www.kaggle.com/c/imagenet-object-localization-challenge) and gives us a quick and lightweight method to capture spatial features. Spatial features learnt are then passed into a Long Short Term Memory(LSTM) module to further study its study time evolution. Model achieved a validation accuracy of <b>82.32%</b> on 5+1(No action) classes on 20BN-Jester dataset.

Refer to [CNN+LSTM Paper](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/43455.pdf) for more details
<br>

3)<space> MobileNetV2_L2Norm + LSTM
---
Just like <b>MobileNetV2 + LSTM</b>, this model employs the use of 2D Convolution Networks pre-trained on Imagenet. For this model, the learnt spatial features are L2 normalised to become vectors of unit length before passing them into the LSTM module. Model achieved a slight boost in validation accuracy to <b>86.35%</b> on 5+1(No action) classes on 20BN-Jester dataset.
<br>

4)<space> C3D_L2Norm + LSTM + UF4
---
The model employs the use of 3D Convolution Networks to capture spatio-temporal features that are crucial in classifying Makaton signs which are non-static. The learnt spatio-temporal features are then passed into the LSTM to further study its time evolution. Learning not only spatial but temporal features as well allowed the representations of makaton sings to be better captured. This facilitated a huge improvement over the <b>MobileNetV2_L2Norm + LSTM</b> model. Model achieved a validation accuracy of <b>94.64%</b> on 5+1(No action) classes on 20BN-Jester dataset.

Refer to [C3D+LSTM Paper](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwiOjovI1vriAhUMilwKHVA_A8AQFjAAegQIAhAC&url=https%3A%2F%2Fwww.mdpi.com%2F1999-5903%2F11%2F2%2F42%2Fpdf&usg=AOvVaw2k7dwm_6BqK9GFhkHDnGis) for more details
<br>

5)<space> C3D_L2Norm + LSTM + UF7
---
This is the same model as the model <b> C3D_L2Norm + LSTM + UF4 </b> above but with the final 7 layers unfrozen(3 more than UF4). This allowed the model to better learn the patterns on the Jester dataset as compared to just using the pre-trained weights that are not tuned specifically to Jester. Model achieved a validation accuracy of <b>96.69%</b> on 5+1(No action) classes on 20BN-Jester dataset.
<br>




