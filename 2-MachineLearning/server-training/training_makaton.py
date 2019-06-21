
'''
Obsolete as Makaton Dataset deleted
for Data Privacy reasons
'''
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import keras
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import load_model

from sklearn.preprocessing import LabelEncoder,OneHotEncoder

from Models import c3d_super_lite


df_mak = pd.read_csv( 'new-makaton-data.csv',
					index_col = None,
					header=None,
					sep=',',
					names=['Folder','Action', 'V1', 'V2' , 'V3' , 'V4' , 'V5'])

df_jest = pd.read_csv( 'jester-train-all.csv',
					index_col = None,
					header=None,
					sep=';',
					names=['Folder','Action', 'Frames'])

df_jest = df_jest[(df_jest['Frames']>=30)]
df_jest = df_jest.drop(columns='Frames')
mask = ((df_jest['Action'] != 'Thumb Up') 					& 
		(df_jest['Action'] != 'Thumb Down') 				& 
		(df_jest['Action'] != 'Swiping Right') 				&
		(df_jest['Action'] != 'Sliding Two Fingers Right')	&
		(df_jest['Action'] != 'Drumming Fingers') 			& 
		(df_jest['Action'] != 'Shaking Hand'))

df_jest = df_jest[mask]


df_mak = df_mak.drop(columns=['V1','V2','V3','V4'])
df_mak['Path'] = os.path.join('makaton-data-new-resized','makaton_vids')
df_mak = df_mak[df_mak['Action']!='NN']

# df_mak = df_mak.sample(frac=0.0)
dftrain = df_mak[(df_mak['V5'] == 'T')]
dfval   = df_mak[(df_mak['V5'] =='V')]

dftrain = dftrain.drop(columns='V5')
dfval = dfval.drop(columns='V5')

dftrain_unique = pd.DataFrame(np.repeat(dftrain[dftrain.index>900].values,35,axis=0),columns=['Folder','Action','Path'])
dftrain = pd.concat([dftrain,dftrain_unique])

dfval_unique = pd.DataFrame(np.repeat(dfval.values,16,axis=0),columns=['Folder','Action','Path'])
dfval = pd.concat([dfval,dfval_unique])

df_jest['Path'] = os.path.join('jester-data','20bn-jester-v1')

df_jest_train = df_jest.head(int(len(df_jest)*0.8)) 
df_jest_valid = df_jest.tail(int(len(df_jest)*0.2)) 

dftrain = pd.concat([dftrain,df_jest_train])
dfval = pd.concat([dfval,df_jest_valid])

print(sorted((dftrain['Action'].unique())))


label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(dftrain['Action'])
dftrain['Action'] = integer_encoded

label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(dfval['Action'])
dfval['Action'] = integer_encoded

for i in range(0,40,1):
	print(i,dftrain[dftrain['Action']==i].shape)

for i in range(0,40,1):
	print(i,dfval[dfval['Action']==i].shape)


model = c3d_super_lite()


model.fit_generator(
 	DataGeneratorIA(dftrain,dim=(112,112)),
 	validation_data=DataGeneratorIA(dfval,dim=(112,112)),
 	verbose=1,
 	epochs=1000 ,
 	callbacks=[ModelCheckpoint('checkpoint_models/C3DLSTM_jester_all_mak_6_aug.h5',
                                monitor='val_loss',
                                verbose=1,
                                save_best_only=True,
                                save_weights_only=True,
                                mode='min',
                                period=1)]
 )

