import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.image as mpimg
from random import randint
import sys
import os
import cv2

sess = tf.InteractiveSession()

x = tf.placeholder(tf.float32, shape=[None, 10000])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

W = tf.Variable(tf.zeros([10000,10]))
b = tf.Variable(tf.zeros([10]))

sess.run(tf.global_variables_initializer())

y = tf.matmul(x,W) + b

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)



correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x, [-1,100,100,1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([40000, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 40000])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

saver = tf.train.Saver()

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())

#try:
saver.restore(sess, "../model.ckpt")
print("Model restored.")
print("Try testing...")
#except:
#  print("Model not found...")
#  sys.exit()
while True:
  try:
    num = randint(1000,3500)
    path = os.path.join("faces",str(num)+".jpg")
    orig_img = mpimg.imread(path)
    img = cv2.resize(orig_img,(100,100))
    img = img.reshape((10000))
    prediction = tf.argmax(y_conv,1)
    classification = prediction.eval(feed_dict={x: [img],keep_prob: 1.0}, session=sess)
    fig = plt.figure()
    a = fig.add_subplot(1,2,1)
    plt.imshow(orig_img,cmap=plt.cm.gray)
    a = fig.add_subplot(1,2,2)
    #print (classification)
    res = mpimg.imread(str(classification[0])+".png")
    plt.imshow(res)
    plt.show()
    #sys.exit()
  except Exception as e:
      print('Exception Caught')
      print(str(e))
      
