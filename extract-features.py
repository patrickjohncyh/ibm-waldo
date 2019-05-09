import pandas as pd
import numpy as np
import os
from Extractor import Extractor,ExtractorXception,ExtractorInception,ExtractorC3D
from tqdm import tqdm


"""model = ExtractorInception()

df = pd.read_csv( 'jester-v1-train-five.csv',index_col = None,header=None,sep=';')
df.columns = ['Folder','Action','Frames']
video_folders = df['Folder']
video_folders = video_folders[:15000]

pbar = tqdm(total=video_folders.size)
for idx,f in video_folders.iteritems():
	path = os.path.join('jester-data','20bn-jester-v1',str(f))
	files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(path)]))

	save_path = os.path.join('jester-data','jester-features',str(f)+'-'+'features-inception')
	seq = []
	for frame in files:
		frame_path = os.path.join(path,frame+'.jpg')
		feature = model.extract(frame_path)
		seq.append(feature)
	
	np.save(save_path,seq)
	pbar.update(1)
pbar.close()
"""

model = ExtractorC3D()

df = pd.read_csv( 'jester-v1-train-five.csv',index_col = None,header=None,sep=';')
df.columns = ['Folder','Action','Frames']
mask = (df['Frames']>=16)
df = df[mask]

video_folders = df['Folder']
video_folders = video_folders[:15000]

pbar = tqdm(total=video_folders.size)
for idx,f in video_folders.iteritems():
	path = os.path.join('jester-data','20bn-jester-v1',str(f))

	save_pathfc6 = os.path.join('jester-data','jester-features',str(f)+'-'+'features-fc6')
	save_pathfc7 = os.path.join('jester-data','jester-features',str(f)+'-'+'features-fc7')
	fc6,fc7 = model.extract(path)
	
	np.save(save_pathfc6,fc6)
	np.save(save_pathfc7,fc7)
	pbar.update(1)
pbar.close()