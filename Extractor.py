from keras.preprocessing import image

from keras.applications.xception import Xception, preprocess_input as prepreocess_input_x
from keras.applications.mobilenet_v2 import MobileNetV2,preprocess_input  
from keras.applications.inception_v3 import InceptionV3,preprocess_input as preprocess_input_i

from keras.models import Model, load_model
from keras.layers import Input
import numpy as np
import os

from Models import c3d_sports

class ExtractorMobileNet():
    def __init__(self):
        """Either load pretrained from imagenet, or load our saved
        weights from our own training."""

        # Get model with pretrained weights.
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=True
        )

        # We'll extract features at the final pool layer.
        self.model = Model(
            inputs=base_model.input,
            outputs=base_model.get_layer('global_average_pooling2d_1').output
        )

    def extract(self, image_path):
        img = image.load_img(image_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Get the prediction.
        features = self.model.predict(x)

        # For imagenet/default network:
        features = features[0]

        return features

class ExtractorXception():
    def __init__(self):
        """Either load pretrained from imagenet, or load our saved
        weights from our own training."""

        # Get model with pretrained weights.
        base_model = Xception(
            weights='imagenet',
            include_top=True
        )

        # We'll extract features at the final pool layer.
        self.model = Model(
            inputs=base_model.input,
            outputs=base_model.get_layer('avg_pool').output
        )

    def extract(self, image_path):
        img = image.load_img(image_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input_x(x)

        # Get the prediction.
        features = self.model.predict(x)

        # For imagenet/default network:
        features = features[0]

        return features      

class ExtractorInception():
    def __init__(self):
        """Either load pretrained from imagenet, or load our saved
        weights from our own training."""

        # Get model with pretrained weights.
        base_model = InceptionV3(
            weights='imagenet',
            include_top=True
        )

        # We'll extract features at the final pool layer.
        self.model = Model(
            inputs=base_model.input,
            outputs=base_model.get_layer('avg_pool').output
        )

    def extract(self, image_path):
        img = image.load_img(image_path, target_size=(299, 299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input_i(x)

        # Get the prediction.
        features = self.model.predict(x)

        # For imagenet/default network:
        features = features[0]

        return features   

class ExtractorC3D():
    def __init__(self):
        base_model = c3d_sports()
        
        self.model = Model(
            inputs = base_model.input,
            outputs = (base_model.get_layer('fc6').output , base_model.get_layer('fc7').output )
        )
    def extract(self, video_path):
        x =  np.empty((16,112,112,3),dtype=np.uint8)
        files = np.sort(np.array([os.path.splitext(filename)[0] for filename in os.listdir(video_path)]))
        skip = len(files) // 16
        output = [files[i] for i in range(0, len(files), skip)]
        files = output[:16]
        x = [ image.img_to_array(image.load_img(video_path+"/"+f+".jpg", target_size=(112, 112))) for f in files]
        x = np.expand_dims(x, axis=0)

        # Get the prediction.
        features = self.model.predict(x)

        fc6,fc7 = features[0],features[1]

        return fc6,fc7
