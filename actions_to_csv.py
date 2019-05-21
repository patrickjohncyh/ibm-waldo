import os
import pandas as pd
import numpy as np
from tqdm import tqdm

# Training Data
path = os.path.join('jester-data','labels','jester-v1-train.csv') #CSV containing full list of all actions vids used for training
df = pd.read_csv( path,index_col = None,header=None,sep=';')
df.columns = ['Folder','Action']

mask = ((df['Action']=='Swiping Left') | 
	    (df['Action']=='Swiping Right')| 
	    (df['Action']=='Swiping Down') | 
	    (df['Action']=='Swiping Up')   |
		(df['Action']=='Thumb Up')     |
		(df['Action']=='No gesture') |
		(df['Action']=='Rolling Hand Backward') |
		(df['Action']=='Turning Hand Counterclockwise') |
		(df['Action']=='Sliding Two Fingers Left') | 
		(df['Action']=='Sliding Two Fingers Right') |
		(df['Action']=='Stop Sign') |
		(df['Action']=='Drumming Fingers'))



df = df[mask]
df['Frames'] = 0

pbar = tqdm(total=df.shape[0])
for idx,row in df.iterrows():
	v = row[0]
	path = os.path.join('jester-data','20bn-jester-v1',str(v))
	num_files = len(os.listdir(path))
	df.at[idx,'Frames'] = num_files
	pbar.update(1)
pbar.close()

df[mask].to_csv("jester-train-12.csv",index=False,header=False,sep=';')
