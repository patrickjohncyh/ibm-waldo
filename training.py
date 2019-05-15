import os
import numpy as np
import pandas as pd
import tensorflow as tf
import keras

from keras.preprocessing import image
from keras.utils import to_categorical

from sklearn.preprocessing import LabelEncoder,OneHotEncoder

from tqdm import tqdm

from Models import lstm,seqlstm,c3d_sports,c3d

class DataGenerator(keras.utils.Sequence):
	def __init__(self, df,  batch_size=32, num_frames = 30, dim=2048, n_channels=1, shuffle=True): 
	    # Initialization
		self.transform = None
		self.dim = dim
		self.batch_size = batch_size
		self.n_channels = n_channels
		self.shuffle = shuffle
		self.df = df
		self.num_frames  = num_frames
		self.num_classes = len(df['Action'].unique())
		self.on_epoch_end()

	def __len__(self):
		'''Denotes the number of batches per epoch'''
		return int(np.floor(self.df.shape[0]/self.batch_size))

	def __getitem__(self, index):
		y = []
		df_batch = self.df[index*self.batch_size:(index+1)*self.batch_size]
		X =  np.empty((self.batch_size , self.num_frames , self.dim), dtype=np.uint8)
		path = 'jester-data/jester-features/'
		for i in range (0,self.batch_size,1):
			v,label,num_frames = df_batch.iloc[i]
			X[i] = np.load(path+str(v)+"-"+"features-mobilenet" + ".npy")[:self.num_frames]
		y = to_categorical(df_batch['Action'].values,num_classes=self.num_classes)
		return X,y
			
	def on_epoch_end(self):
		# 'Updates indexes after each epoch'
		self.df = self.df.sample(frac=1.0)

def get_training_data(df):
	
	df = df[mask].head(6000)
	df = df.values
	X =  np.empty((6000,30,112,112,3),dtype=np.uint8)
	y = []
	pbar = tqdm(total=6000)
	for i in range(0,6000,1):
		v,label,num_frames= df[i]
		path = os.path.join('jester-data','20bn-jester-v1',str(v))
		files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))
		files = files[:30]
		X[i,] = [ image.img_to_array(image.load_img(path+"/"+f+".jpg", target_size=(112, 112))) for f in files]
		pbar.update(1)
	pbar.close()

	label_encoder = LabelEncoder()
	integer_encoded = label_encoder.fit_transform(df[:,1])
	onehot_encoder = OneHotEncoder(sparse=False)
	integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
	y = onehot_encoder.fit_transform(integer_encoded)
	return X,y



df = pd.read_csv( 'jester-train.csv',
					index_col = None,
					header=None,
					sep=';',
					names=['Folder','Action','Frames'])


mask = (df['Frames']>=30) & ((df['Action']=='Swiping Left') | (df['Action']=='Swiping Down') |
							(df['Action']=='Thumb Up')      | (df['Action']=='No gesture') |
							(df['Action']=='Rolling Hand Backward') | (df['Action']=='Zooming Out With Full Hand') )
df = df[mask]
label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(df['Action'])
df['Action'] = integer_encoded

dftrain = df.head(int(len(df)*0.8))
dfval   = df.tail(int(len(df)*0.2))

# model = seqlstm()
# model.summary()

# model.fit_generator(
# 	DataGenerator(dftrain,dim=1280),
# 	validation_data=DataGenerator(dfval,dim=1280),
# 	verbose=1,
# 	epochs=100,
# )

# model = c3d_sports()
model = c3d()
model.summary()

X,y = get_training_data(df)
model.fit(X,
 		  y,
 		  verbose=1,
 		  epochs=100,
 		  validation_split=0.2)

