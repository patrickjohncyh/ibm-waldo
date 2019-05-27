import pandas as pd
import numpy as np
import os
from Extractor import ExtractorMobileNet,ExtractorXception,ExtractorInception,ExtractorC3D
from tqdm import tqdm


model = ExtractorMobileNet() #change this based on model used?

df = pd.read_csv('vids_csv.csv', index_col = None, header = None, sep = ',')
df.columns = ['Folder', 'Action']
mask = ((df['Action']=='D') |
		(df['Action']=='G') |
		(df['Action']=='H') |
		(df['Action']=='N') |
		(df['Action']=='S') |
		(df['Action']=='NN'))

df = df[mask]


video_folders = df['Folder']
video_folders = video_folders[4500:]

pbar = tqdm(total=video_folders.size)
for idx,f in video_folders.iteritems():
	path = os.path.join('makaton-data','makaton_vids',str(f))
	files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))
	save_path = os.path.join('makaton-data','makaton_features',str(f)+'-'+'features-mobilenet')
	seq = []
	for frame in files:
		frame_path = os.path.join(path,frame+'.jpg')
		feature = model.extract(frame_path)
		seq.append(feature)
	
	np.save(save_path,seq)

	pbar.update(1)
pbar.close()

