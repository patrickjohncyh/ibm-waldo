import os
import numpy as np
import imgaug as ia
import imageio
from imgaug import augmenters as iaa

from keras.preprocessing import image


class FramesAugmentation():
	def __init__(self):
		# self.sometimes = lambda aug: iaa.Sometimes(0.7, aug)
		self.seq = iaa.Sequential(
			[
			    iaa.Affine( translate_percent={"x": (-0.20, 0.20), "y": (-0.2, 0.2)}, # translate by -20 to +20 percent (per axis)),
			    			scale={"x": (0.8, 1.2), "y": (0.8, 1.2)}, # scale images to 80-120% of their size, individually per axis
			    			rotate=(-5, 5),
			    			shear=(-5, 5),
			    			mode='edge'),
			    iaa.ContrastNormalization((0.75, 1.5)),
				iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
		],random_order=True)

	def augment_batch(self,X):
		seq_det = self.seq.to_deterministic()
		d = X.shape[1]
		for i in range(0,d,1):
			X[:,i,:,:] = seq_det.augment_images(X[:,i,:,:])
		return X