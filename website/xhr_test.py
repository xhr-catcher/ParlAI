import torch
import tensorflow as tf
x = torch.rand(5, 3)
print(x)
print(torch.cuda.is_available())

hello = tf.constant("Hello!TensorFlow")
sess = tf.Session()
print(sess.run(hello))
