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

import tensorflow as tf


K.set_learning_phase(0)


model = load_model('./checkpoint_models/C3DLSTM12.h5')
print(model.outputs)
# [<tf.Tensor 'dense_2/Softmax:0' shape=(?, 10) dtype=float32>]
print(model.inputs)
# [<tf.Tensor 'conv2d_1_input:0' shape=(?, 28, 28, 1) dtype=float32>]


def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.
    @param session The TensorFlow session to be frozen.
    @param keep_var_names A list of variable names that should not be frozen,
                          or None to freeze all the variables in the graph.
    @param output_names Names of the relevant graph outputs.
    @param clear_devices Remove the device directives from the graph for better portability.
    @return The frozen graph definition.
    """
    from tensorflow.python.framework.graph_util import convert_variables_to_constants
    graph = session.graph
    with graph.as_default():
        freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
        output_names = output_names or []
        output_names += [v.op.name for v in tf.global_variables()]
        # Graph -> GraphDef ProtoBuf
        input_graph_def = graph.as_graph_def()
        if clear_devices:
            for node in input_graph_def.node:
                node.device = ""
        frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        return frozen_graph


frozen_graph = freeze_session(K.get_session(),
                              output_names=[out.op.name for out in model.outputs])

# Save to ./model/tf_model.pb
tf.train.write_graph(frozen_graph, "model", "tf_model.pb", as_text=False)

