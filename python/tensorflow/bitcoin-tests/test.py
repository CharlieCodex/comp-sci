import tensorflow as tf
import json
from data_utils import minibatch_sequencer


BATCHSIZE = 200
SEQUENCE_LENGTH = 20

raw_data = []
with open("example_data.txt") as file:
    raw_data = json.load(file)


layer_size = [200, 200, 10, 1]

X = tf.placeholder(tf.float32, (BATCHSIZE, SEQUENCE_LENGTH))

weights = [tf.Variable(tf.random_normal((SEQUENCE_LENGTH, layer_size[0]),
                                        dtype=tf.float32),
                       dtype=tf.float32, name="w0")] + \
          [tf.Variable(tf.random_normal((layer_size[x], layer_size[x + 1]),
                                        dtype=tf.float32),
                       dtype=tf.float32, name=("w" + str(x + 1)))
           for x in range(len(layer_size) - 1)]

biases = [tf.Variable(tf.ones(layer_size[x]),
                      dtype=tf.float32, name=("b" + str(x)))
          for x in range(len(layer_size))]
