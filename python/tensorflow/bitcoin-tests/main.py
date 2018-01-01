import numpy as np
import os
import tensorflow as tf
from tensorflow.contrib import rnn

eth_transaction_fee = tf.constant(0.001)
etc_transaction_fee = tf.constant(0.01)
SEQLEN = 30
BATCHSIZE = 200
INTERNALSIZE = 512
NLAYERS = 3
learning_rate = 0.001
# inputs/outputs
X = tf.placeholder(tf.float32, [None], name="X")
Y_ = tf.placeholder(tf.float32, [None], name="Y_")

# making the multirnn_gru_cell
Hin = tf.placeholder(tf.float32, [None, INTERNALSIZE * NLAYERS], name='Hin')
# [ BATCHSIZE, INTERNALSIZE * NLAYERS]
cells = [rnn.GRUCell(INTERNALSIZE) for _ in range(NLAYERS)]
multicell = rnn.MultiRNNCell(cells, state_is_tuple=False)
Yr, H = tf.nn.dynamic_rnn(multicell, X, dtype=tf.float32, initial_state=Hin)
H = tf.identity(H, name='H')

# checkpoints dir
if not os.path.exists("checkpoints"):
    os.mkdir("checkpoints")
saver = tf.train.Saver(max_to_keep=1000)

# init
# initial zero input state
istate = np.zeros([BATCHSIZE, INTERNALSIZE * NLAYERS])
init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)
step = 0
