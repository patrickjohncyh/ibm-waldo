import numpy as np
import tensorflow as tf

import keras.backend as K

import keras

from keras.models import Sequential
from keras.models import Model

from keras.layers import Input,Flatten,Dense,Dropout,Activation,Reshape
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Conv3D,MaxPooling3D,ZeroPadding3D,MaxPool3D
from keras.layers import LeakyReLU,ReLU,Lambda
from keras.optimizers import Adam,SGD
from keras.layers import LSTM,CuDNNLSTM
from keras.regularizers import l2

from keras.applications.mobilenet_v2 import MobileNetV2


def c3d_super_lite():

    shape = (30,112,112,3)

    model = keras.models.Sequential()

    model.add(keras.layers.InputLayer(input_shape=shape))
    model.add(keras.layers.Conv3D(32, 3,strides=(1,2,2), activation='relu', padding='same', name='conv1', input_shape=shape))
    model.add(keras.layers.MaxPooling3D(pool_size=(1,2,2), strides=(1,2,2), padding='same', name='pool1'))
    
    model.add(keras.layers.Conv3D(64, 3, activation='relu', padding='same', name='conv2'))
    model.add(keras.layers.MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool2'))
    
    model.add(keras.layers.Conv3D(128, 3, activation='relu', padding='same', name='conv3a'))
    model.add(keras.layers.Conv3D(128, 3, activation='relu', padding='same', name='conv3b'))
    model.add(keras.layers.MaxPooling3D(pool_size=(3,2,2), strides=(2,2,2), padding='valid', name='pool3'))
    
    model.add(keras.layers.Conv3D(128, 3, activation='relu', padding='same', name='conv4a'))
    model.add(keras.layers.Conv3D(128, 3, activation='relu', padding='same', name='conv4b'))
    model.add(keras.layers.MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool4'))
    
    model.add(keras.layers.Reshape((9,384)))

    model.add(keras.layers.Lambda(lambda x: K.l2_normalize(x,axis=-1)))
    model.add(keras.layers.LSTM(512, return_sequences=False,
                   input_shape= (9,384)))
            
    model.add(keras.layers.Dense(512, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(26, activation='softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
