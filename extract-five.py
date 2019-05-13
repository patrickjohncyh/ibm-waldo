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
		(df['Action']=='Zooming Out With Full Hand'))
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

df[mask].to_csv("jester-v4-train-five.csv",index=False,header=False,sep=';')
#v1 is csv processed to only have 4 actions(Swipe left,right,up,down)
#v2 is csv to have 6 actions(4 from v1 + thumb up and Shaking Hand)
#v3 is csv to have 10 actions
#v4 is csv with 8 actions(swipe left,right,up,down, thumb up , no gesture, rolling hand backward and zooming out with full hand)






# # Validation Data
# df = pd.read_csv( 'jester-v1-validation.csv',index_col = None,header=None,sep=';')
# df.columns = ['Folder','Action']

# mask = ((df['Action']=='Swiping Left') | 
# 	    (df['Action']=='Swiping Right')| 
# 	    (df['Action']=='Swiping Down') | 
# 	    (df['Action']=='Swiping Up'))

# df[mask].to_csv("jester-v1-validation-five.csv",index=False,header=False,sep=';')