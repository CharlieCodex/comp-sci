import numpy as np
import tensorflow as tf

#consts
INTERNAL_SIZE = 256

#state machine
hstate = tf.placeholder(dtype=tf.float32, shape=(INTERNAL_SIZE))
istate = np.zeros(INTERNAL_SIZE)
