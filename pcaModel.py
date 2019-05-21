from keras.models import load_model,Model
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import keras
import os
import pandas as pd
import numpy as np
from keras.preprocessing import image
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder,OneHotEncoder


saved_model = "checkpoint_models/C3DLSTM12_2.h5"
model = load_model(saved_model)
model.summary()
layer_name = "dense_1"

intermediate_layer_model = Model(inputs=model.input, outputs=model.get_layer(layer_name).output)

df = pd.read_csv( 'jester-train-12.csv',
					index_col = None,
					header=None,
					sep=';',
					names=['Folder','Action','Frames'])
mask = (df['Frames']>=30) 
df = df[mask]
gesturelist = ['Swiping Left', 'Swiping Down' , 'Thumb Up' , 'Drumming Fingers' , 'Sliding Two Fingers Left' , 'No gesture']
df = df[df['Action'].isin(gesturelist)]

df = df[:200]
df = df[['Folder', 'Action']]



path = os.path.join('jester-data','20bn-jester-v1')
X =  np.empty((200,30,112,112,3,) , dtype=np.uint8)
y=[]

print("Loading Images ....")
for i in range (0,200,1):
	v,label= df.iloc[i]
	folder_path = path+"/"+str(v)	
	files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(folder_path)]))
	files = files[:30]
	X[i] = np.array([image.img_to_array(image.load_img(folder_path+"/"+str(f)+".jpg", target_size=(112,112))) for f in files])
	y.append(label)

print("Predicting final dense layer to obtain feature embeddings ... ")
embeds = intermediate_layer_model.predict(X) #Embeddings after passing through Network before the final Softmax layer	
y = np.array(y)


print("Performing PCA on embeddings ...")
pca = PCA(n_components=2)
X_P = pca.fit_transform(embeds)
print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))

plt.figure()
colors = ['navy', 'red' , 'turquoise', 'yellow', 'magenta' , 'black']

for color,i in zip(colors,gesturelist):
    plt.scatter(X_P[y==i,0], X_P[y==i,1], color=color, alpha=.5)
  
plt.title('PCA of 200 512-Dimensional Feature Vectors')
plt.legend(labels=gesturelist, loc = 'best')

plt.savefig("pca_embeddings/200.png", dpi=200)