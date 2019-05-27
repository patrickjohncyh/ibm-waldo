import os
import numpy as np
import pandas as pd
import tensorflow as tf
import keras

from keras.preprocessing import image
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import load_model


from sklearn.preprocessing import LabelEncoder,OneHotEncoder

from tqdm import tqdm

from Models import lstm,seqlstm,c3d_sports,c3d,c3d_super_lite

class DataGenerator(keras.utils.Sequence):
	def __init__(self, df,  batch_size=32, num_frames = 30, dim=1280, n_channels=1, shuffle=True): 
	    # Initialization
		self.transform = None
		self.dim = dim
		self.batch_size = batch_size
		self.n_channels = n_channels
		self.shuffle = shuffle
		self.df = df
		self.num_frames  = num_frames
		self.num_classes = len(df['Action'].unique())
		self.path = os.path.join('makaton-straight-data','makaton_vids')
		self.on_epoch_end()

	def __len__(self):
		'''Denotes the number of batches per epoch'''
		return int(np.floor(self.df.shape[0]/self.batch_size))

	def __getitem__(self, index):
		y = []
		df_batch = self.df[index*self.batch_size:(index+1)*self.batch_size]
		X =  np.empty((self.batch_size,self.num_frames,) + self.dim + (self.n_channels,), dtype=np.uint8)
		for i in range (0,self.batch_size,1):
			v,label = df_batch.iloc[i]
			folder_path = self.path+"/"+str(v)	
			files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(folder_path)]))
			files = files[:self.num_frames]
			X[i] = [image.img_to_array(image.load_img(folder_path+"/"+str(f)+".jpg", target_size=self.dim)) for f in files]
		y = to_categorical(df_batch['Action'].values,num_classes=self.num_classes)
		return X,y
			
	def on_epoch_end(self):
		# 'Updates indexes after each epoch'
		self.df = self.df.sample(frac=1.0)

#def get_training_data(df):
#	num_classes = len(df['Action'].unique())
#	df = df.head(6000)
#	df = df.values
#	X =  np.empty((6000,30,112,112,3),dtype=np.uint8)
#	y = []
#	pbar = tqdm(total=6000)
#	for i in range(0,6000,1):
#		v,label,num_frames= df[i]
#		path = os.path.join('jester-data','20bn-jester-v1',str(v))
#		files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))
#		files = files[:30]
#		X[i,] = [ image.img_to_array(image.load_img(path+"/"+f+".jpg", target_size=(112, 112))) for f in files]
#		pbar.update(1)
#	pbar.close()
#	y = to_categorical(df[:,1],num_classes=num_classes)
#	return X,y


df = pd.read_csv( 'vids_csv.csv',
					index_col = None,
					header=None,
					sep=',',

					names=['Folder','Action', 'V1', 'V2' , 'V3' , 'V4' , 'V5'])

label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(df['Action'])
df['Action'] = integer_encoded
df = df.sample(frac=1.0)

mask = ( (df['Folder']<=1160) | (df['Folder']>=1341))
df = df[mask]


dftrain = df[(df['V5'] == 'T')]
dfval   = df[(df['V5'] =='V')]


dftrain = dftrain[['Folder', 'Action']]
dfval = dfval[['Folder', 'Action']]


model = c3d_super_lite()

model.fit_generator(
 	DataGeneratorF(dftrain,dim=(112,112)),
 	validation_data=DataGeneratorF(dfval,dim=(112,112)),
 	verbose=1,
 	epochs=50 ,
 	callbacks=[ModelCheckpoint('checkpoint_models/C3DLSTM_makaton_clean_weightsonly.h5',
                                monitor='val_loss',
                                verbose=1,
                                save_best_only=True,
                                save_weights_only=True,
                                mode='min',
                                period=1)]
 )

