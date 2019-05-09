import os
import numpy as np
import pandas as pd
import keras

from keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from Models import lstm,c3d_model,c3d_sports,fcn
from tqdm import tqdm
from keras.utils import to_categorical
# from keras.models import load_

def get_training_data():
	df = pd.read_csv( 'jester-v1-train-five.csv',index_col = None,header=None,sep=';')
	df.columns = ['Folder','Action','Frames']
	mask = (df['Frames']>=30) #& ( (df['Action'] == 'Swiping Right') | (df['Action'] == 'Swiping Down') )
	df = df[mask].head(14700)
	X = []
	y = []

	pbar = tqdm(total=14700)
	for idx,row in df.iterrows():
		v,label,num_frames = row
		feature_path = os.path.join('jester-data','jester-features',str(v)+'-'+'features-inception'+'.npy')
		X.append(np.load(feature_path)[:30])
		y.append(label)
		pbar.update(1)
	pbar.close()

	label_encoder = LabelEncoder()
	integer_encoded = label_encoder.fit_transform(y)
	onehot_encoder = OneHotEncoder(sparse=False)
	integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
	y = onehot_encoder.fit_transform(integer_encoded)
	X = np.array(X,ndmin=3)
	return X,y

def get_training_data_imgs():
	df = pd.read_csv( 'jester-v1-train-five.csv',index_col = None,header=None,sep=';')
	df.columns = ['Folder','Action','Frames']
	mask = (df['Frames']>=16) & ( (df['Action'] == 'Swiping Right') | (df['Action'] == 'Swiping Down') )
	df = df[mask].head(8000)
	df = df.values

	X =  np.empty((8000,16,112,112,3),dtype=np.uint8)
	y = []
	pbar = tqdm(total=8000)
	for i in range(0,8000,1):
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

# class DataGenerator(keras.utils.Sequence):

# 	def __init__(self, df,  batch_size=8,  dim=(16,128,128), n_channels=3, shuffle=True):
# 	    # 'Initialization'
# 		self.transform = None
# 		self.dim = dim
# 		self.batch_size = batch_size
# 		self.n_channels = n_channels
# 		self.shuffle = shuffle
# 		self.df = df
# 		self.on_epoch_end()


# 	# def get_image(self, t):
# 	#     def transform_img(img):
# 	#         if self.transform is not None:
# 	#             img = transform(img.numpy())
# 	#         return img
# 	#     a, p = self.data[t[0]], self.data[t[1]]

# 	#     return img_a, img_p

# 	def __len__(self):
# 		'''Denotes the number of batches per epoch'''
# 		return int(np.floor(self.df.shape[0]/self.batch_size))

# 	def __getitem__(self, index):
# 		y = []
# 		df_batch = self.df[index*self.batch_size:(index+1)*self.batch_size]
# 		X =  np.empty((self.batch_size,) + self.dim + (self.n_channels,))
# 		size = self.dim[0]
# 		for i in range (0,self.batch_size,1):
# 			v,label,num_frames = df.iloc[i]
# 			path = 'jester-data/20bn-jester-v1/'+str(v)
# 			files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))
# 			skip = len(files) // size
# 			output = [files[i] for i in range(0, len(files), skip)]
# 			files = output[:size]
# 			frame3d = [ image.img_to_array(image.load_img(path+"/"+f+".jpg", target_size=(128, 128))) for f in files]
# 			X[i] = frame3d
# 			y.append(label)

# 		label_encoder = LabelEncoder()
# 		integer_encoded = label_encoder.fit_transform(y)
# 		onehot_encoder = OneHotEncoder(sparse=False,categories='auto')
# 		integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
# 		y = onehot_encoder.fit_transform(integer_encoded)	
# 		return X,np.array(y)


# 	def on_epoch_end(self):
# 		# 'Updates indexes after each epoch'
# 		self.df = self.df.sample(frac=1.0)



model = lstm()
# model = c3d_sports()
#model = fcn()




X,y = get_training_data()
model.fit(X,
 		  y,
 		  verbose=1,
 		  epochs=100,
 		  validation_split=0.2)



# model.fit_generator(
# 	DataGenerator(df),
# 	verbose=1,
# 	epochs=100
# )

# X,y = get_training_data()
# model.fit(X,
# 		  y,
# 		  verbose=1,
# 		  epochs=100,
# 		  validation_split=0.2)


