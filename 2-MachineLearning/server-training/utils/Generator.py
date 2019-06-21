import os
import keras
import numpy as np
from tqdm import tqdm
from keras.preprocessing import image
from keras.utils import to_categorical
from utils.FramesAugmentation import FramesAugmentation

class DataGeneratorIA(keras.utils.Sequence):
	'''
	Data Generator with optional Frames Augmentation
	'''
	
	def __init__(self, df,  batch_size=32, num_frames = 30, dim=(112,122), n_channels=3, shuffle=True, augment=False): 
	    # Initialization
		self.transform = None
		self.dim = dim
		self.batch_size = batch_size
		self.n_channels = n_channels
		self.shuffle = shuffle
		self.df = df
		self.num_frames  = num_frames
		self.num_classes = len(df['Action'].unique())
		self.path = os.path.join('makaton-data-new-resized','makaton_vids')
		self.augment = augment
		self.fa = FramesAugmentation()
		self.on_epoch_end()

	def __len__(self):
		'''Denotes the number of batches per epoch'''
		return int(np.floor(self.df.shape[0]/self.batch_size))

	def __getitem__(self, index):
		y = []
		df_batch = self.df[index*self.batch_size:(index+1)*self.batch_size]
		X =  np.empty((self.batch_size,self.num_frames,) + self.dim + (self.n_channels,), dtype=np.uint8)
		for i in range (0,self.batch_size,1):
			v,label,path = df_batch.iloc[i]
			folder_path = path+"/"+str(v)	
			files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(folder_path)]))
			files = files[:self.num_frames]
			X[i] = [image.img_to_array(image.load_img(folder_path+"/"+str(f)+".jpg", target_size=self.dim)) for f in files]
		if(self.augment == True):
			X = self.fa.augment_batch(X)
		y = to_categorical(df_batch['Action'].values,num_classes=self.num_classes)
		return X,y
			
	def on_epoch_end(self):
		# 'Updates indexes after each epoch'
		self.df = self.df.sample(frac=1.0)