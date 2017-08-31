import tensorflow as tf
import json
import os
from os import listdir
from pprint import pprint

#load data

raw_data = []

for filename in listdir('data'):
    if filename.endswith('.json'):
        with open('data/'+filename) as data_file:
            raw_data.insert(len(raw_data), json.load(data_file)['values'])

CTX_LENGTH = 10
#length of W and b tensors

PREDICT_DEGREES = 11
#range of % change to predict (execess will be cliped in)
PREDICT_RANGE = 5

if not os.path.exists("tmp"):
    os.makedirs("tmp")

#data management, x as input, y as desired output
X = tf.placeholder(tf.float32, [None, CTX_LENGTH])
Y_ = tf.placeholder(tf.float32, [PREDICT_DEGREES])


#predict next price in points, ranging from -5pts to + 5pts
W = tf.Variable(tf.zeros([CTX_LENGTH, PREDICT_DEGREES]),
                      name="weights")
b = tf.Variable(tf.zeros([CTX_LENGTH, PREDICT_DEGREES]),
                      name="baises")

#model softmax function
Y = tf.nn.softmax(tf.matmul(X, W) + b);

#error function
cross_entropy = -tf.reduce_mean(Y_ * tf.log(Y + 1e-10))

#training step definition
train_step = tf.train.GradientDescentOptimizer(0.003).minimize(cross_entropy)

def extractBatch(batch_i, data):
    batch_data = data[batch_i:batch_i+CTX_LENGTH+1]
    batch_X = []
    for i in range(len(batch_data)-1):
        batch_X.append(batch_data[i]['y'])

    batch_Y = [0.0] * PREDICT_DEGREES
    #calculated percent error = difference / sum
    if batch_data[CTX_LENGTH]['y'] + batch_data[CTX_LENGTH-1]['y'] == 0:
        cpe = 0
    else:
        cpe = (batch_data[CTX_LENGTH]['y'] - batch_data[CTX_LENGTH-1]['y'])/(batch_data[CTX_LENGTH]['y'] + batch_data[CTX_LENGTH-1]['y'])

    #make sure the cpe is within our tensor
    if cpe > PREDICT_RANGE:
        cpe = PREDICT_RANGE
    elif cpe < -PREDICT_RANGE:
        cpe = -PREDICT_RANGE

    if PREDICT_DEGREES % 2 == 0:
        cpe /= PREDICT_RANGE * (PREDICT_DEGREES) / 2 - 1
    else:
        cpe /= PREDICT_RANGE * (PREDICT_DEGREES - 1) / 2

    cpe += (PREDICT_DEGREES - 1) / 2;

    #get index on tmp tensor
    batch_Y[round(cpe)] = 1.0

    yield [batch_X]
    yield batch_Y
#last vars for our training loop!!!

#init vars
init = tf.global_variables_initializer()
sess = tf.Session()

sess.run(init);

saver = tf.train.Saver(max_to_keep=1)

#saver.restore(sess, "tmp/model1450.ckpt")

depth = 0

for i, data in enumerate(raw_data):
    print("STARTING DATASET "+str(i+1)+" OF " + str(len(raw_data)))
    nb_batches = len(data)-(CTX_LENGTH+1)
    for batch_i in range(nb_batches):

        #define our batch values
        batch_X, batch_Y = extractBatch(batch_i, data)

        #train it

        #save every 50 batches just in case
        if (batch_i + depth) % 50 == 0:
            save_path = saver.save(sess, "tmp/model-"+str(depth + batch_i)+".ckpt")
            print("Model saved in file: %s" % save_path)


        sess.run(train_step, feed_dict={X: batch_X, Y_: batch_Y})

    depth += nb_batches

