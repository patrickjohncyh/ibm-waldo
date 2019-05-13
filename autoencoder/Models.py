import numpy as np
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers import Dense,Dropout,MaxPooling3D,ZeroPadding3D,MaxPooling2D
from keras.layers import LeakyReLU,ReLU,Conv3D,Flatten,Conv2D,UpSampling2D
from keras.optimizers import Adam,SGD
import keras.backend as K

from keras.layers import Dense,Dropout,Conv3D,Input,MaxPool3D,Flatten,Activation
from keras.regularizers import l2
from keras.models import Model


def autoencoder():

  input_shape = (128,128,3)

  input_layer = Input(input_shape)

  x = Conv2D(32,
            (3,3),
            strides=(1,1),
            padding='same')(input_layer)
  x = ReLU()(x)
  x = MaxPooling2D(pool_size=(2, 2),
                   padding='valid')(x)

  x = Conv2D(16,
            (3,3),
            strides=(1,1),
            padding='same')(x)
  x = ReLU()(x)
  x = MaxPooling2D(pool_size=(2, 2),
                   padding='valid')(x)

  x = Conv2D(8,
            (3,3),
            strides=(1,1),
            padding='same')(x)
  x = ReLU()(x)
  x = Conv2D(3,
            (3,3),
            strides=(1,1),
            padding='same')(x)
  encoded = ReLU(name='encoded')(x)

  x = Conv2D(8,
            (3,3),
            strides=(1,1),
            padding='same')(encoded)
  x = ReLU()(x)
  x = UpSampling2D(size=(2, 2),
                  data_format=None,
                  interpolation='nearest')(x)

  x = Conv2D(16,
            (3,3),
            strides=(1,1),
            padding='same')(x)
  x = ReLU()(x)
  x = UpSampling2D(size=(2, 2),
                  data_format=None,
                  interpolation='nearest')(x)

  x = Conv2D(3,
            (3,3),
            strides=(1,1),
            padding='same')(x)
  decoded = ReLU()(x)


  model = Model(input_layer,decoded) 
  model.compile(loss='MAE',
                optimizer=Adam(),
                metrics=['MSE'])

  return model


def lstm():
    """Build a simple LSTM network. We pass the extracted features from
    our CNN to this model predomenently."""
    # Model .
    model = Sequential()
    model.add(LSTM(512, return_sequences=False,

                   input_shape= (30,2048),
                   dropout=0.5))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(),
                  metrics=['accuracy'])
    return model


def convlstm():
  """ LSTM with convolutional input transformation and recurrent 
  transformations."""

  input_layer = Input((30,112,112,3),name='top_input')

  x = (ConvLSTM2D(filters=8,
                      kernel_size=(3,3),
                      strides=(1, 1), 
                      padding='same'))(input_layer)

  x = Conv2D(128, 
           kernel_size=(3,3),
           strides=(1, 1), padding='valid')(x)                      
  x = ReLU()(x)
  x = BatchNormalization()(x)
  x = MaxPooling2D(pool_size=(2, 2),
                   strides=(2,2))(x)

  x = Conv2D(128, 
           kernel_size=(3,3),
           strides=(1, 1), padding='valid')(x)                      
  x = ReLU()(x)
  x = BatchNormalization()(x)
  x = MaxPooling2D(pool_size=(2, 2),
                   strides=(2,2))(x)

  x = Conv2D(128, 
           kernel_size=(3,3),
           strides=(1, 1), padding='valid')(x)                      
  x = ReLU()(x)
  x = BatchNormalization()(x)
  x = MaxPooling2D(pool_size=(2, 2),
                   strides=(2,2))(x)
  
  x = Conv2D(128, 
           kernel_size=(3,3),
           strides=(1, 1), padding='valid')(x)                      
  x = ReLU()(x)
  x = BatchNormalization()(x)
  x = MaxPooling2D(pool_size=(2, 2),
                   strides=(2,2))(x)
   
  x = Flatten()(x)
  # x = Dense(128, activation='relu')(x)
  x = Dropout(0.2)(x)
  x = Dense(8, activation='softmax')(x)

  model = Model(input_layer,x)

  model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])
  return model







