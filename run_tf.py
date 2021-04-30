import tensorflow as tf
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import numpy as np

import sys

def load_pb(path_to_pb):
  with tf.io.gfile.GFile(path_to_pb, 'rb') as f:
    graph_def = tf.compat.v1.GraphDef()
    graph_def.ParseFromString(f.read())
  with tf.Graph().as_default() as graph:
    tf.import_graph_def(graph_def, name="")
    return graph


def run(inp_name, graph_name, output_name):
  inp = np.load(inp_name, allow_pickle=True)
  # inp = np.reshape(inp, (1,320,320,3))
  g = load_pb(graph_name)
  i = g.get_operation_by_name("x")
  with g.as_default():
    with tf.compat.v1.Session() as sess:
      output_tensor = g.get_tensor_by_name(output_name)
      #g.get_operation_by_name(output_name).outputs[0]
      out = sess.run(output_tensor, feed_dict={i.outputs[0]:inp})
      np.save("tensorflow_output", out)
      print("\n"*5)
      print("Output dumped in tensorflow_output.npy")
      print("Output = ", out)

if __name__ == '__main__':
  run(sys.argv[1], "frozen_graph.pb", "Identity:0")