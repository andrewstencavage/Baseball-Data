import collections
import math
import os
import time

import numpy as np
import pandas as pd
import scipy
import scipy.stats
import matplotlib.pyplot as plt

import tensorflow as tf
import tensorflow_probability as tfp
tfd = tfp.distributions
tfb = tfp.bijectors

# We're assuming 2-D data with a known true mean of (0, 0)
true_mean = np.zeros([2], dtype=np.float32)
# We'll make the 2 coordinates correlated
true_cor = np.array([[1.0, 0.9], [0.9, 1.0]], dtype=np.float32)
# And we'll give the 2 coordinates different variances
true_var = np.array([4.0, 1.0], dtype=np.float32)
# Combine the variances and correlations into a covariance matrix
true_cov = np.expand_dims(np.sqrt(true_var), axis=1).dot(
    np.expand_dims(np.sqrt(true_var), axis=1).T) * true_cor
# We'll be working with precision matrices, so we'll go ahead and compute the
# true precision matrix here
true_precision = np.linalg.inv(true_cov)

# Here's our resulting covariance matrix
print(true_cov)
# Verify that it's positive definite, since np.random.multivariate_normal
# complains about it not being positive definite for some reason.
# (Note that I'll be including a lot of sanity checking code in this notebook -
# it's a *huge* help for debugging)
print('eigenvalues: ', np.linalg.eigvals(true_cov))


# Set the seed so the results are reproducible.
np.random.seed(123)

# Now generate some observations of our random variable.
# (Note that I'm suppressing a bunch of spurious about the covariance matrix
# not being positive semidefinite via check_valid='ignore' because it really is
# positive definite!)
my_data = np.random.multivariate_normal(
    mean=true_mean, cov=true_cov, size=100,
    check_valid='ignore').astype(np.float32)
print(my_data.shape)


# Do a scatter plot of the observations to make sure they look like what we
# expect (higher variance on the x-axis, y values strongly correlated with x)
plt.scatter(my_data[:, 0], my_data[:, 1], alpha=0.75)
# plt.show()

def log_lik_data_numpy(precision, data):
  # np.linalg.inv is a really inefficient way to get the covariance matrix, but
  # remember we don't care about speed here
  cov = np.linalg.inv(precision)
  rv = scipy.stats.multivariate_normal(true_mean, cov)
  return np.sum(rv.logpdf(data))

# test case: compute the log likelihood of the data given the true parameters
ret = log_lik_data_numpy(true_precision, my_data)
print(ret)

with tf.Graph().as_default() as g:
  # case 1: get log probabilities for a vector of iid draws from a single
  # normal distribution
  norm1 = tfd.Normal(loc=0., scale=1.)
  probs1 = norm1.log_prob(tf.constant([1., 0.5, 0.]))

  # case 2: get log probabilities for a vector of independent draws from
  # multiple normal distributions with different parameters.  Note the vector
  # values for loc and scale in the Normal constructor.
  norm2 = tfd.Normal(loc=[0., 2., 4.], scale=[1., 1., 1.])
  probs2 = norm2.log_prob(tf.constant([1., 0.5, 0.]))

  g.finalize()
  
with tf.Session(graph=g) as sess:
  print 'iid draws from a single normal:', sess.run(probs1)

  print 'draws from a batch of normals:', sess.run(probs2)