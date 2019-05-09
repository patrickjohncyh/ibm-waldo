import numpy as np
from keras.models import Sequential
from keras.layers.recurrent import LSTM
from keras.layers import Dense,Dropout,MaxPooling3D,ZeroPadding3D
from keras.layers import LeakyReLU,ReLU,Conv3D,Flatten
from keras.optimizers import Adam,SGD
import keras.backend as K
from keras.layers import Dense,Dropout,Conv3D,Input,MaxPool3D,Flatten,Activation
from keras.regularizers import l2
from keras.models import Model



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


def fcn():
    model = Sequential()
    model.add(Flatten(input_shape=(1,4096)))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu', name='fcx'))
    model.add(Dropout(0.2))
    model.add(Dense(4, activation='softmax', name='fc8'))
    model.compile(loss='categorical_crossentropy',
            optimizer=Adam(),
            metrics=['accuracy'])

    return model


def c3d_pretrain():
    input_shape = (112,112,16,3)
    weight_decay = 0.005
    nb_classes = 101

    inputs = Input(input_shape)
    x = Conv3D(64,(3,3,3),strides=(1,1,1),padding='same',
               activation='relu',kernel_regularizer=l2(weight_decay))(inputs)
    x = MaxPool3D((2,2,1),strides=(2,2,1),padding='same')(x)

    x = Conv3D(128,(3,3,3),strides=(1,1,1),padding='same',
               activation='relu',kernel_regularizer=l2(weight_decay))(x)
    x = MaxPool3D((2,2,2),strides=(2,2,2),padding='same')(x)

    x = Conv3D(128,(3,3,3),strides=(1,1,1),padding='same',
               activation='relu',kernel_regularizer=l2(weight_decay))(x)
    x = MaxPool3D((2,2,2),strides=(2,2,2),padding='same')(x)

    x = Conv3D(256,(3,3,3),strides=(1,1,1),padding='same',
               activation='relu',kernel_regularizer=l2(weight_decay))(x)
    x = MaxPool3D((2,2,2),strides=(2,2,2),padding='same')(x)

    x = Conv3D(256, (3, 3, 3), strides=(1, 1, 1), padding='same',
               activation='relu',kernel_regularizer=l2(weight_decay))(x)
    x = MaxPool3D((2, 2, 2), strides=(2, 2, 2), padding='same')(x)

    x = Flatten()(x)
    x = Dense(2048,activation='relu',kernel_regularizer=l2(weight_decay))(x)
    x = Dropout(0.5)(x)
    x = Dense(2048,activation='relu',kernel_regularizer=l2(weight_decay))(x)
    x = Dropout(0.5)(x)
    x = Dense(nb_classes,kernel_regularizer=l2(weight_decay))(x)
    x = Activation('softmax')(x)
    model = Model(inputs, x)
    model.load_weights('weights_c3d.h5')    
    for i in range(len(model.layers)-4):
      model.layers[i].trainable = False
    return model

def c3d_model():

  weight_decay = 0.005
  model = c3d_pretrain()
  output_layer = Dense(512,kernel_regularizer=l2(weight_decay))(model.layers[-3].output)
  output_layer = Dense(512,kernel_regularizer=l2(weight_decay))(output_layer)
  output_layer = Dense(2,kernel_regularizer=l2(weight_decay))(output_layer)
  output_layer = Activation('softmax')(output_layer)

  model = Model(model.inputs,output_layer)
  model.compile(loss='categorical_crossentropy',
              optimizer=Adam(),
              metrics=['accuracy'])
  return model

def c3d_sports():
    
    if K.image_data_format() == 'channels_last':
        shape = (16,112,112,3)
    else:
        shape = (3,16,112,112)
    
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

    model.load_weights('sports1M_weights_tf.h5')    
    for i in range(len(model.layers)):
      model.layers[i].trainable = False

    model.pop()
    model.add(Dense(2, activation='softmax', name='fc8'))
    model.compile(loss='categorical_crossentropy',
            optimizer=Adam(),
            metrics=['accuracy'])

    return model


