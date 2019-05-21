import tensorflow as tf
import keras.backend as K
from tensorflow.python.framework import graph_io
from tensorflow.keras.models import load_model,Model
from tensorflow.keras.layers import Input


import tensorflow.contrib.tensorrt as trt

# Clear any previous session.
tf.keras.backend.clear_session()


save_pb_dir = 'frozen_models'
model_fname = 'checkpoint_models/C3DLSTM12.h5'


def freeze_graph(graph, session, output, save_pb_dir='.', save_pb_name='frozen_model.pb', save_pb_as_text=False):
    with graph.as_default():
        graphdef_inf = tf.graph_util.remove_training_nodes(graph.as_graph_def())
        graphdef_frozen = tf.graph_util.convert_variables_to_constants(session, graphdef_inf, output)
        graph_io.write_graph(graphdef_frozen, save_pb_dir, save_pb_name, as_text=save_pb_as_text)

def get_frozen_graph(graph_file):
    """Read Frozen Graph file from disk."""
    with tf.gfile.FastGFile(graph_file, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    return graph_def        

# # This line must be executed before loading Keras model.
# tf.keras.backend.set_learning_phase(0) 

# model = load_model(model_fname,custom_objects={'tf':tf,'K':K})
# model.summary()
# input_layer = Input((30,112,112,3))
# output_layer = model(input_layer)
# model = Model(input_layer,output_layer)
# model.summary()

session = tf.keras.backend.get_session()


input_names = ['input_1']  #[t.op.name for t in model.inputs]
output_names = [' sequential_2/dense_2/Softmax'] #[t.op.name for t in model.outputs]

# Prints input and output nodes names, take notes of them.
print(input_names, output_names)

# frozen_graph = freeze_graph(session.graph, session, [out.op.name for out in model.outputs], save_pb_dir=save_pb_dir)
# frozen_graph = freeze_graph(session.graph, session, output_names, save_pb_dir=save_pb_dir)
frozen_graph = get_frozen_graph('tf_model.pb')

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