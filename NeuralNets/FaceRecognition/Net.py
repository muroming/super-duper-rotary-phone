import os

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import BatchNormalization, Dropout, Input
from tensorflow.keras.models import Model

np.random.seed(10)
tf.set_random_seed(10)


class BayesianModel(object):
    def __init__(self, input_shape, output_shape, n_persons, predict_threshold, batch_size=32, n_iter_train=70,
                 n_iter_predict=200, test_size=.3, label_names=None, model_path=None, input_dtype=tf.float32, output_dtype=tf.int32):
        tf.reset_default_graph()

        self.session = tf.Session()
        self.model = self.__build_model(n_persons)
        self.x = tf.placeholder(shape=input_shape, dtype=input_dtype)
        self.y = tf.placeholder(shape=output_shape, dtype=output_dtype)
        self.n = tf.placeholder(shape=[], dtype=tf.float32)
        self.n_iter_train = n_iter_train
        self.batch_size = batch_size
        self.n_iter_predict = n_iter_predict
        self.label_names = label_names
        self.test_size = test_size
        self.predict_threshold = predict_threshold

        # if model_path is not None and os.path.exists(model_path):
        #     saver = tf.train.Saver()
        #     saver.restore(self.session, model_path)
        #     print("Model loaded")

    def predict(self, X):
        res = []
        for _ in range(self.n_iter_predict):
            res.append(self.__predict_once(X))

        res_means = np.mean(res, axis=0)
        max_ind = np.argmax(res_means)
        print(np.array(res).shape, res_means.shape)
        print(res_means)

        if np.max(res_means) < self.predict_threshold:
            return ""

        if self.label_names is not None:
            return self.label_names[max_ind]

        return max_ind

    def __predict_once(self, X):
        return self.session.run(self.probs, feed_dict={self.x: X})

    def fit(self, X, y):
        logits = self.model(self.x)
        self.probs = tf.nn.softmax(logits, axis=1)
        labels_distribution = tfp.distributions.Categorical(logits=logits)
        log_probs = labels_distribution.log_prob(self.y)

        neg_log_likelihood = -tf.reduce_mean(log_probs)
        kl = sum(self.model.losses) / self.n
        elbo_loss = neg_log_likelihood + kl

        correct_preds = tf.equal(tf.cast(self.y, dtype=tf.int64), tf.argmax(self.probs, axis=1))
        accuracy = tf.reduce_mean(tf.cast(correct_preds, tf.float32))

        optimizer = tf.train.AdamOptimizer(0.001)
        train_op = optimizer.minimize(elbo_loss)

        init = tf.global_variables_initializer()

        sess = self.session
        sess.run(init)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size)

        for i in range(self.n_iter_train):
            batch_indices = np.random.choice(len(X_train), self.batch_size, replace=False)
            batch_x = X_train[batch_indices]
            batch_y = y_train[batch_indices]

            feed_dict = {self.x: batch_x, self.y: batch_y, self.n: self.batch_size}
            sess.run(train_op, feed_dict=feed_dict)

            temp_loss, temp_acc = sess.run([elbo_loss, accuracy], feed_dict=feed_dict)

            batch_indices = np.random.choice(len(X_test), self.batch_size, replace=False)
            batch_x = X_test[batch_indices]
            batch_y = y_test[batch_indices]

            feed_dict = {self.x: batch_x, self.y: batch_y, self.n: self.batch_size}
            sess.run(train_op, feed_dict=feed_dict)

            temp_loss, temp_acc = sess.run([elbo_loss, accuracy], feed_dict=feed_dict)

            print("Val accuracy:", temp_acc)

    def __build_model(self, number_persons):
        inputs = Input(shape=(128,))

        x = tfp.layers.DenseFlipout(64, activation='relu')(inputs)
        x = Dropout(0.5)(x)
        x = tfp.layers.DenseFlipout(32, activation='relu')(inputs)
        x = BatchNormalization()(x)
        outputs = tfp.layers.DenseFlipout(number_persons, activation=None)(x)

        model = Model(inputs, outputs)
        model.summary()

        return model
