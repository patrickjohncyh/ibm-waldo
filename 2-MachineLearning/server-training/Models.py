import numpy as np
import tensorflow as tf

import keras.backend as K
import keras

from keras.models import Sequential
from keras.models import Model,load_model

from keras.layers import Input,Flatten,Dense,Dropout,Activation,Reshape
from keras.layers import Conv2D
from keras.layers import Conv3D,MaxPooling3D,ZeroPadding3D,MaxPool3D
from keras.layers import LeakyReLU,ReLU,Lambda
from keras.optimizers import Adam,SGD
from keras.layers import LSTM,CuDNNLSTM
from keras.regularizers import l2

from keras.applications.mobilenet_v2 import MobileNetV2

def c3d_super_lite():
    """
    Lite C3D Model + LSTM
    L2 Normalisation of C3D Lite Feature Vectors 
    3M Parameters
    Able to Run on the Jetson Nano at 8FPS
    Final Dense Layer to bemodified to adjust the number of classes
    """
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
                   input_shape= (9,384),
                   dropout=0.5))
    model.add(keras.layers.Dense(512, activation='relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(6, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model 
    
def c3d():
    """
    Full C3D Model + LSTM
    L2 Normalisation of C3D Feature Vectors 
    30M Parameters
    Final Dense Layer to bemodified to adjust the number of classes
    
    """
    shape = (30,112,112,3)

    model = Sequential()
    model.add(Conv3D(64, 3, activation='relu', padding='same', name='conv1', input_shape=shape))
    model.add(MaxPooling3D(pool_size=(1,2,2), strides=(1,2,2), padding='same', name='pool1'))
    
    model.add(Conv3D(128, 3, activation='relu', padding='same', name='conv2'))
    model.add(MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool2'))
    
    model.add(Conv3D(256, 3, activation='relu', padding='same', name='conv3a'))
    model.add(Conv3D(256, 3, activation='relu', padding='same', name='conv3b'))
    model.add(MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool3'))
    
    model.add(Conv3D(512, 3, activation='relu', padding='same', name='conv4a'))
    model.add(Conv3D(512, 3, activation='relu', padding='same', name='conv4b'))
    model.add(MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool4'))
    
    model.add(Conv3D(512, 3, activation='relu', padding='same', name='conv5a'))
    model.add(Conv3D(512, 3, activation='relu', padding='same', name='conv5b'))

    model.add(MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool5'))
    
    model.add(Reshape((9,512)))

    model.add(Lambda(lambda x: K.l2_normalize(x,axis=-1)))
    model.add(CuDNNLSTM(512, return_sequences=False,
                   input_shape= (9,512),
                   dropout=0.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation='softmax'))

    
    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])
    return model

def lstm():
    """
    Simple LSTM network. 
    Pass the extracted features from CNN to this model.
    L2 normalisation of Input Feature Vectors
    """
    model = Sequential()
    model.add(Lambda(lambda x: K.l2_normalize(x,axis=-1), input_shape= (30,1280)))
    model.add(CuDNNLSTM(512, return_sequences=False,
                   input_shape= (30,1280)))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])
    return model

def mobilenetonly():
    model = MobileNetV2( weights ='imagenet', include_top = True)
    model = Model(inputs = model.input, outputs = model.get_layer('global_average_pooling2d_1').output )
    #model.add(Dense(12, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])
    return model

