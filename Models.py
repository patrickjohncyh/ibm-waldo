import numpy as np
import tensorflow as tf

import keras.backend as K

from keras.models import Sequential
from keras.models import Model

from keras.layers import Input,Flatten,Dense,Dropout,Activation,Reshape
from keras.layers import Conv2D
from keras.layers import Conv3D,MaxPooling3D,ZeroPadding3D,MaxPool3D
from keras.layers import LeakyReLU,ReLU,Lambda
from keras.optimizers import Adam,SGD
from keras.layers.recurrent import LSTM
from keras.regularizers import l2

from keras.applications.mobilenet_v2 import MobileNetV2


def lstm():
    """
    Simple LSTM network. 
    Pass the extracted features from CNN to this model.
    Perform L2 normalisation to input feature vector
    """
    model = Sequential()
    model.add(Lambda(lambda x: K.l2_normalize(x,axis=-1), input_shape= (30,1280)))
    model.add(LSTM(512, return_sequences=False,
                   input_shape= (30,1280), #1280 for mobilenet, 2048 for inception and exception
                   dropout=0.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])
    return model


def seqlstm():
    """
    Simple LSTM network.
    Output for each LSTM unit is used and average is used as prediction
    Pass the extracted features from CNN to this model.
    Perform L2 normalisation to input feature vector
    """
    model = Sequential()
    model.add(Lambda(lambda x: K.l2_normalize(x,axis=-1), input_shape= (30,1280)))
    model.add(LSTM(512, return_sequences=True,
                   input_shape= (30,1280), #1280 for mobilenet, 2048 for inception and exception
                   dropout=0.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(6, activation='softmax'))
    model.add(Lambda(lambda x : tf.keras.backend.mean(x[:,25:,:],axis=1)))

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])
    return model


def c3d_sports():

    shape = (16,112,112,3)

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
    model.add(ZeroPadding3D(padding=(0,1,1)))
    model.add(MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool5'))
    
    model.add(Flatten())
    
    model.add(Dense(4096, activation='relu', name='fc6'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu', name='fc7'))
    model.add(Dropout(0.5))
    model.add(Dense(487, activation='softmax', name='fc8'))
    
    model.load_weights('pretrained_weights/sports1M_weights_tf.h5')   

    return model

def c3d():

    pre_train = c3d_sports()

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
    model.add(ZeroPadding3D(padding=(0,1,1)))
    model.add(MaxPooling3D(pool_size=(2,2,2), strides=(2,2,2), padding='valid', name='pool5'))
    
    model.add(Reshape((16,512)))

    model.add(Lambda(lambda x: K.l2_normalize(x,axis=-1)))
    model.add(LSTM(512, return_sequences=False,
                   input_shape= (16,512),
                   dropout=0.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(12, activation='softmax'))

    for i in range(0,14,1):
        model.layers[i].set_weights(pre_train.layers[i].get_weights())

    for i in range(0,7,1):    
        model.layers[i].trainable = False

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])
    return model



    # for i in range(len(model.layers)):
    #   model.layers[i].trainable = False
