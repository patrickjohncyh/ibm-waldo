import os
import pandas as pd
import numpy as np
from tqdm import tqdm

'''
Generates CSV from provided Labels
Filters based on deisired actions
Adds new field for number of Frames 
'''

# CSV containing full list of all actions vids used for training
path = os.path.join('jester-data','labels','jester-v1-train.csv') 
df = pd.read_csv( path,index_col = None,header=None,sep=';')
df.columns = ['Folder','Action']

# Mask to select desired Actions
mask = ((df['Action']=='Swiping Left') 				| 
	    (df['Action']=='Swiping Down') 				|
		(df['Action']=='Thumbs Up') 				|
		(df['Action']=='Drumming Fingers')			|
		(df['Action']=='Sliding Two Fingers Left') 	| 
		(df['Action']=='No gesture'))
df = df[mask]

# Add new column for number of Frames
df['Frames'] = 0

# Loop through Dataset and check number of frames
pbar = tqdm(total=df.shape[0])
for idx,row in df.iterrows():
	v = row[0]
	path = os.path.join('jester-data','20bn-jester-v1',str(v))
	num_files = len(os.listdir(path))
	df.at[idx,'Frames'] = num_files
	pbar.update(1)
pbar.close()

# Generate CSV
df.to_csv('jester-train-six-actions.csv',index=False,header=False,sep=';')
