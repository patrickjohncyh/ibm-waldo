from tensorflow.keras.models import load_model
from keras import backend as K

import tensorflow as tf
from tensorflow.contrib import tensorrt as tftrt
from tensorflow.python.framework import graph_io

import copy
import numpy as np
import sys
import time

class FrozenGraph(object):
  def __init__(self, model, shape):
    shape = (None,) + shape
    x_name = 'image_tensor_x'
    with K.get_session() as sess:
        x_tensor = tf.placeholder(tf.float32, shape, x_name)
        K.set_learning_phase(0)
        y_tensor = model(x_tensor)
        y_name = y_tensor.name[:-2]
        graph = sess.graph.as_graph_def()
        graph0 = tf.graph_util.convert_variables_to_constants(sess, graph, [y_name])
        graph1 = tf.graph_util.remove_training_nodes(graph0)

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

    graph_io.write_graph(tftrt_graph, "./frozen_models/",
                     "trt_graph.pb", as_text=False)

    opt_graph = copy.deepcopy(graph)
    opt_graph.frozen = tftrt_graph
    super(TftrtEngine, self).__init__(opt_graph)
    self.batch_size = batch_size

  def infer(self, x):
    num_tests = x.shape[0]
    y = np.empty((num_tests, self.y_tensor.shape[1]), np.float32)
    batch_size = self.batch_size

    for i in range(0, num_tests, batch_size):
      x_part = x[i : i + batch_size]
      y_part = self.sess.run(self.y_tensor,
        feed_dict={self.x_tensor: x_part})
      y[i : i + batch_size] = y_part
    return y

def verify(result, ans):
  num_tests = ans.shape[0]
  error = 0
  for i in range(0, num_tests):
    a = np.argmax(ans[i])
    r = np.argmax(result[i])
    if (a != r) : error += 1

  if (error == 0) : print('PASSED')
  else            : print('FAILURE')

def freeze_graph(graph, session, output, save_pb_dir='.', save_pb_name='frozen_model.pb', save_pb_as_text=False):
    with graph.as_default():
        graphdef_inf = tf.graph_util.remove_training_nodes(graph.as_graph_def())
        graphdef_frozen = tf.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
        graph_io.write_graph(graphdef_frozen, save_pb_dir, save_pb_name, as_text=save_pb_as_text)

from Models import lstm,c3d,c3d_only

# model = load_model("checkpoint_models/C3DLSTM12_2.h5")
model = c3d()
model.summary()
tf.global_variables_initializer()



frozen_graph = FrozenGraph(model, (30,112,112,3))
for node in frozen_graph.frozen.node:
  print(node.name)

print("Done Freezing...")

tftrt_engine = TftrtEngine(frozen_graph, 1, 'FP32')

