import tensorflow as tf
import numpy as np
import json
import data_utils as data_utils
import os
import math
import time

if not os.path.exists("checkpoints"):
    os.mkdir("checkpoints")

data = []
with open("example_data.txt") as file:
    data = json.load(file)

BATCHSIZE = 200
INTERNALSIZE = 200
SEQ_LEN = 1

X = tf.placeholder(tf.float32, [BATCHSIZE,1], name="X")
Y_ = tf.placeholder(tf.float32, [BATCHSIZE,1], name="Y_")

w1 = tf.Variable(tf.truncated_normal([1,40]),dtype=tf.float32)
b1 = tf.Variable(tf.ones([40]),dtype=tf.float32)
#in 1 number, out 40
w2 = tf.Variable(tf.truncated_normal([40,40]),dtype=tf.float32)
b2 = tf.Variable(tf.ones([40]),dtype=tf.float32)
#in 40 , out 20
w3 = tf.Variable(tf.truncated_normal([40,20]),dtype=tf.float32)
b3 = tf.Variable(tf.ones([20]),dtype=tf.float32)
#in 20 , out 40
w4 = tf.Variable(tf.truncated_normal([INTERNALSIZE+20,INTERNALSIZE]),dtype=tf.float32)
b4 = tf.Variable(tf.ones([INTERNALSIZE]),dtype=tf.float32)
#interal_size+40 in, 100 out

mem_gate_w = tf.Variable(tf.truncated_normal([INTERNALSIZE,INTERNALSIZE]),dtype=tf.float32)
mem_gate_b = tf.Variable(tf.ones([INTERNALSIZE]),dtype=tf.float32)

#final output neuron
out_w = tf.Variable(tf.truncated_normal([INTERNALSIZE,1]),dtype=tf.float32)
out_b = tf.Variable(tf.ones([INTERNALSIZE]),dtype=tf.float32)

istate = np.zeros([BATCHSIZE, INTERNALSIZE])

Y1 = tf.nn.relu(tf.matmul(X,w1)+b1)
Y2 = tf.nn.relu(tf.matmul(Y1,w2)+b2)
Y3 = tf.nn.relu(tf.matmul(Y1,w3)+b3)

Hin = tf.placeholder(tf.float32,[BATCHSIZE,INTERNALSIZE],"Hin")

H = tf.nn.sigmoid(tf.matmul(tf.concat([Hin,Y3],1),w4)+b4)

ostate = tf.nn.relu(tf.matmul(H,mem_gate_w)+mem_gate_b)

Y = tf.matmul(H,out_w)+out_b;
loss = tf.squared_difference(Y,Y_);
train_step = tf.train.AdamOptimizer().minimize(loss);

saver = tf.train.Saver(max_to_keep=1000)
sess = tf.Session()
init = tf.global_variables_initializer();
sess.run(init)
timestamp = str(math.trunc(time.time()))
saver.restore(sess,'checkpoints/rnn_train_final')
step = 0

for x, y_, epoch in data_utils.minibatch_sequencer(data, BATCHSIZE, SEQ_LEN, nb_epochs=100):

    # train on one minibatch
    feed_dict = {X: x, Y_: y_, Hin: istate}
    _, y, o,l = sess.run([train_step, Y, ostate, loss], feed_dict=feed_dict)
    if step // 10 % BATCHSIZE*10 == 0:
        for i in range(0,BATCHSIZE):
            print(str(x[i][0])+"|"+str(y_[i][0])+": "+str(y[i][0]))
    # loop state around
    istate = o
    step += BATCHSIZE * SEQ_LEN


saved_file = saver.save(sess, 'checkpoints/rnn_train_final_'+timestamp)
