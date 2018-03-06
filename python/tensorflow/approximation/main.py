import tensorflow as tf
import numpy as np

INTERNAL_SIZE = 200
DEGREE = 2

def main():
    y = tf.placeholder(shape=(2), dtype=tf.float32)
    w_1 = tf.Variable(tf.random_normal((2 + INTERNAL_SIZE, INTERNAL_SIZE)),
                      dtype=tf.float32)
    b_1 = tf.Variable(tf.random_normal((INTERNAL_SIZE)),
                      dtype=tf.float32)
    w_2 = tf.Variable(tf.random_normal((INTERNAL_SIZE, DEGREE + 1)),
                      dtype=tf.float32)
    b_2 = tf.Variable(tf.random_normal((DEGREE + 1)),
                      dtype=tf.float32)
    w_f = tf.Variable(tf.random_normal((INTERNAL_SIZE, INTERNAL_SIZE)),
                      dtype=tf.float32)
    b_f = tf.Variable(tf.random_normal((INTERNAL_SIZE, INTERNAL_SIZE)),
                      dtype=tf.float32)
    istate = tf.placeholder(shape=(INTERNAL_SIZE),
                            dtype=tf.float32)
    state = tf.matmul(w_1, tf.concat(y + istate)) + b_1
    ostate = tf.nn.relu(tf.matmul(w_f, state) + b_f)
    _y = state


if __name__ == '__main__':
    main()
