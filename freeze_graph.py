import tensorflow as tf
import keras.backend as K
from tensorflow.python.framework import graph_io
from keras.models import load_model,Model
from keras.layers import Input


import tensorflow.contrib.tensorrt as trt

from Models import lstm,c3d,fcn

# Clear any previous session.
tf.keras.backend.clear_session()


save_pb_dir = 'frozen_models'
model_fname = 'erkl.h5'


def freeze_graph(graph, session, output, save_pb_dir='.', save_pb_name='frozen_model.pb', save_pb_as_text=False):
    with graph.as_default():
        graphdef_inf = tf.graph_util.remove_training_nodes(graph.as_graph_def())
        graphdef_frozen = tf.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
        graph_io.write_graph(graphdef_frozen, save_pb_dir, save_pb_name, as_text=save_pb_as_text)
        return graphdef_frozen

def get_frozen_graph(graph_file):
    """Read Frozen Graph file from disk."""
    with tf.gfile.FastGFile(graph_file, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    return graph_def        


def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
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
        frozen_graph = tf.graph_util.convert_variables_to_constants(session, input_graph_def,
                                                      output_names, freeze_var_names)
        frozen_graph = tf.graph_util.remove_training_nodes(frozen_graph)
        return frozen_graph


# This line must be executed before loading Keras model.
tf.keras.backend.set_learning_phase(0) 

# model = load_model("erkl.h5",custom_objects={'tf':tf,'K':K,"GlorotUniform": tf.keras.initializers.glorot_uniform})
model = fcn()
model.save('temp.h5')
model = load_model("temp.h5")
model.summary()

session = tf.keras.backend.get_session()
tf.global_variables_initializer()

input_names = [t.op.name for t in model.inputs]
output_names = [t.op.name for t in model.outputs]

# Prints input and output nodes names, take notes of them.
print(input_names, output_names)

frozen_graph = freeze_graph(session.graph, session, [out.op.name for out in model.outputs], save_pb_dir=save_pb_dir)
# frozen_graph = freeze_graph(session.graph, session, output_names, save_pb_dir=save_pb_dir)
# frozen_graph = get_frozen_graph('tf_model.pb')

for node in frozen_graph.node:
	print(node.name)


trt_graph = trt.create_inference_graph(
    input_graph_def=frozen_graph,
    outputs=output_names,
    max_batch_size=1,
    max_workspace_size_bytes=1 << 25,
    precision_mode='FP16',
    minimum_segment_size=50
)

graph_io.write_graph(trt_graph, "./frozen_models/",
                     "trt_graph.pb", as_text=False)