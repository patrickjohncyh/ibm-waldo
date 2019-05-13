import os
import numpy as np
import pandas as pd
import keras

import PIL.Image as Image
from keras.preprocessing import image
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from Models import lstm,convlstm,autoencoder
from tqdm import tqdm
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ModelCheckpoint

def get_training_data_imgs():
	df = pd.read_csv( 'jester-v1-train-five.csv',index_col = None,header=None,sep=';')
	df.columns = ['Folder','Action','Frames']
	mask = (df['Frames']>=30) #& ( (df['Action'] == 'Swiping Right') | (df['Action'] == 'Swiping Down') )
	df = df[mask].head(9999)
	df = df.values
	num_samples = df.shape[0]
	X =  np.empty((num_samples,30,112,112,3),dtype=np.uint8)
	y = []
	pbar = tqdm(total=num_samples)
	for i in range(0,num_samples,1):
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

class DataGeneratorAE(keras.utils.Sequence):

	def __init__(self, df,  batch_size=32, num_frames = 30, dim=(128,128), n_channels=3, shuffle=True):
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
		X =  np.empty((self.batch_size,self.num_frames) + self.dim + (self.n_channels,),dtype=np.uint8)
		for i in range (0,self.batch_size,1):
			v,label,num_frames = df_batch.iloc[i]
			path = '../jester-data/20bn-jester-v1/'+str(v)
			files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))
			files = files[:self.num_frames]
			frame3d = [image.img_to_array(image.load_img(path+"/"+f+".jpg", target_size=self.dim)) for f in files]
			X[i] = frame3d
			# y.append(label)
		X = X.reshape((self.batch_size*self.num_frames,) + self.dim + (self.n_channels,))
		return X,X

	def on_epoch_end(self):
		# 'Updates indexes after each epoch'
		self.df = self.df.sample(frac=1.0)

model = autoencoder()
model.summary()

df = pd.read_csv( '../jester-v1-train-five.csv',index_col = None,header=None,sep=';')
df.columns = ['Folder','Action','Frames']
mask = (df['Frames']>=30)
df = df[mask]

label_encoder = LabelEncoder()
integer_encoded = label_encoder.fit_transform(df['Action'])
df['Action'] = integer_encoded

df_train = df.head(int(len(df)*0.4))
df_valid = df.tail(int(len(df)*0.1))
# df_pred  = df.tail(int(len(df)*0.2)).sample(10)

print(df_train.shape)
print(df_valid.shape)

model.fit_generator(
	generator = DataGeneratorAE(df_train),
	validation_data= DataGeneratorAE(df_valid),
	verbose=1,
	epochs=100,
	use_multiprocessing=True,
	workers=8,
	callbacks=[ModelCheckpoint('checkpoint_models/Autoencoder.h5',
                                monitor='val_loss',
                                verbose=1,
                                save_best_only=True,
                                mode='min',
                                period=1)]
)

# def predict(x):
# 	v,label,num_frames = x.values
# 	path  = '../jester-data/20bn-jester-v1/'+str(v)
# 	files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))
# 	file  = files[np.random.randint(6,27)]
# 	img   = image.load_img(path+"/"+file+".jpg", target_size=(128,128))
# 	out   = model.predict(np.expand_dims(image.img_to_array(img),0),verbose=1)

# 	out_img = Image.fromarray(np.squeeze(out,0).astype(np.uint8))
# 	out_img.save("out_img/"+file+"-out.jpg")
# 	img.save("out_img/"+file+"-in.jpg")



# df_pred.apply(predict,axis=1)












