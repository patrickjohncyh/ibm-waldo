import os
import numpy as np
import pandas as pd
import keras

from keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from Models import lstm,c3d_model,c3d_sports,fcn,seqlstm
from tqdm import tqdm
from keras.utils import to_categorical

df = pd.read_csv( 'jester-v4-train-five.csv',index_col = None,header=None,sep=';') #v1 for 4 classes, v2 for 6

class DataGenerator(keras.utils.Sequence):

	def __init__(self, df,  batch_size=32, num_frames = 30, dim=2048, n_channels=1, shuffle=True): 
		#dim = 2048 for inception, 1280 for mobilenet
	    # 'Initialization'
		self.transform = None
		self.dim = dim
		self.batch_size = batch_size
		self.n_channels = n_channels
		self.shuffle = shuffle
		self.df = df
		self.num_frames = num_frames
		self.on_epoch_end()
	def __len__(self):
		'''Denotes the number of batches per epoch'''
		return int(np.floor(self.df.shape[0]/self.batch_size))

	def __getitem__(self, index):
		y = []
		df_batch = self.df[index*self.batch_size:(index+1)*self.batch_size]
		X =  np.empty((self.batch_size , self.num_frames , self.dim), dtype=np.uint8)
		for i in range (0,self.batch_size,1):
			v,label,num_frames = df_batch.iloc[i]
			path = 'jester-data/jester-features/'+str(v)
			frame3d = np.load(path+"-"+"features-mobilenet" + ".npy")[:self.num_frames]
			X[i] = frame3d
			y.append(label)
		
		label_encoder = LabelEncoder()
		y = label_encoder.fit_transform(y)	
		return X,to_categorical(y,num_classes=6)
			
	def on_epoch_end(self):
		# 'Updates indexes after each epoch'
		self.df = self.df.sample(frac=1.0)

def get_training_data():
	df = pd.read_csv( 'jester-v4-train-five.csv',index_col = None,header=None,sep=';')
	df.columns = ['Folder','Action','Frames']
	mask = (df['Frames']>=16) & ((df['Action']=='Swiping Left') | (df['Action']=='Swiping Up') |
								 (df['Action']=='Thumb Up')     | (df['Action']=='No gesture') |
								 (df['Action']=='Rolling Hand Backward') | (df['Action']=='Zooming Out With Full Hand'))
	df = df[mask].head(12000)
	df = df.values
	

	X =  np.empty((12000,16,112,112,3),dtype=np.uint8)
	y = []
	pbar = tqdm(total=12000)
	for i in range(0,12000,1):
		v,label,num_frames= df[i]
		path = os.path.join('jester-data','20bn-jester-v1',str(v))
		files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))
		skip = len(files) // 16
		output = [files[i] for i in range(0, len(files), skip)]
		files = output[:16]
		X[i,] = [ image.img_to_array(image.load_img(path+"/"+f+".jpg", target_size=(112, 112))) for f in files]
		pbar.update(1)
	pbar.close()

	label_encoder = LabelEncoder()
	integer_encoded = label_encoder.fit_transform(df[:,1])
	onehot_encoder = OneHotEncoder(sparse=False)
	integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
	y = onehot_encoder.fit_transform(integer_encoded)
	return X,y


df.columns = ['Folder','Action','Frames']
mask = (df['Frames']>=30) & 	((df['Action']=='Swiping Left') | (df['Action']=='Swiping Down') |
								(df['Action']=='Thumb Up')     | (df['Action']=='No gesture') |
								(df['Action']=='Rolling Hand Backward') | (df['Action']=='Zooming Out With Full Hand') )


df = df[mask].head(40000)
dftrain = df.head(int(len(df)*0.8))
dfval = df.tail(int(len(df)*0.2))

model = seqlstm()
model.summary()

model.fit_generator(
	DataGenerator(dftrain,dim=1280),
	validation_data=DataGenerator(dfval,dim=1280),
	verbose=1,
	epochs=100,
)

# model = c3d_sports()

# X,y = get_training_data()
# model.fit(X,
#  		  y,
#  		  verbose=1,
#  		  epochs=100,
#  		  validation_split=0.2)

