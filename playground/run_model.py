import tensorflow as tf
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import numpy as np

import sys
from run_tf import run
from pre_process import pre_process

if __name__ == '__main__':
    img_name = sys.argv[1]
    output_name = "image_numpy_data"
    pre_process(img_name, output_name)
    run(output_name + ".npy", "frozen_graph.pb", "Identity:0")