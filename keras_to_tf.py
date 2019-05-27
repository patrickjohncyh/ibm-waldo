from keras.models import load_model
from keras import backend as K

import tensorflow as tf
from tensorflow.contrib import tensorrt as tftrt
import tensorrt as trt
from tensorflow.python.framework import graph_io

import copy
import numpy as np
import sys
import time
import os
from keras.preprocessing import image

# import utils.ascii as helper
# import utils.dataset as data

class FrozenGraph(object):
  def __init__(self, model, shape):
    shape = (None,) + shape
    x_name = 'image_tensor_x'
    with K.get_session() as sess:
        model.summary()
        x_tensor = tf.placeholder(tf.float32, shape, x_name)
        K.set_learning_phase(0)
        y_tensor = model(x_tensor)
        y_name = y_tensor.name[:-2]
        graph = sess.graph.as_graph_def()
        graph0 = tf.graph_util.convert_variables_to_constants(sess, graph, [y_name])
        graph1 = tf.graph_util.remove_training_nodes(graph0)
        graph_io.write_graph(graph1, '.', 'lenet.pb', as_text=False)

    self.x_name = [x_name]
    self.y_name = [y_name]
    self.frozen = graph1

class TfEngine(object):
  def __init__(self, graph):
    g = tf.Graph()
    with g.as_default():
      x_op, y_op = tf.import_graph_def(
          graph_def=graph.frozen, return_elements=graph.x_name + graph.y_name)
      self.x_tensor = x_op.outputs[0]
      self.y_tensor = y_op.outputs[0]

    config = tf.ConfigProto(gpu_options=
      tf.GPUOptions(per_process_gpu_memory_fraction=0.5,
      allow_growth=True))

    self.sess = tf.Session(graph=g, config=config)

  def infer(self, x):
    y = self.sess.run(self.y_tensor,
      feed_dict={self.x_tensor: x})
    return y

class TftrtEngine(TfEngine):
  def __init__(self, graph, batch_size, precision):
    tftrt_graph = tftrt.create_inference_graph(
      graph.frozen,
      outputs=graph.y_name,
      max_batch_size=batch_size,
      max_workspace_size_bytes=1 << 30,
      precision_mode=precision,
      minimum_segment_size=2)

    opt_graph = copy.deepcopy(graph)
    opt_graph.frozen = tftrt_graph
    super(TftrtEngine, self).__init__(opt_graph)
    self.batch_size = batch_size

  def infer(self, x):
    y = self.sess.run(self.y_tensor,
      feed_dict={self.x_tensor: x})
    return y

from Models import fcn,c3d,c3d_lite,lenet

model = lenet() #load_model("c3donly.h5")
model.summary()

frozen_graph = FrozenGraph(model, (28,28,1))
# frozen_graph = FrozenGraph(model, (30,112,112,3))
print(type(frozen_graph.frozen))

print("Done Freezing...")
