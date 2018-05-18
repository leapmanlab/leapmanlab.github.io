"""Building, training, and visualizing a convolutional network for MNIST
digit classification using TensorFlow 1.6.

Based on:
(1) TensorFlow 1.7 `tf.layers` tutorial
        (https://www.tensorflow.org/tutorials/layers) - March 31 2018

"""
import genenet as gn
import numpy as np
import tensorflow as tf

from typing import Callable, Dict

# Just because they're so verbose
TRAIN = tf.estimator.ModeKeys.TRAIN
PREDICT = tf.estimator.ModeKeys.PREDICT
EVAL = tf.estimator.ModeKeys.EVAL

tf.logging.set_verbosity(tf.logging.INFO)


def variable_summaries(var):
    """Attach a lot of summaries to a Tensor.

    Returns: None

    """
    with tf.name_scope('summaries'):
        mean = tf.reduce_mean(var)
        tf.summary.scalar('mean', mean)
        with tf.name_scope('stddev'):
            stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
        tf.summary.scalar('stddev', stddev)
        tf.summary.scalar('max', tf.reduce_max(var))
        tf.summary.scalar('min', tf.reduce_min(var))
        tf.summary.histogram('histogram', var)

    pass


def model_fn(features: Dict[str, tf.Tensor],
             labels: Dict[str, tf.Tensor],
             mode: tf.estimator.ModeKeys) -> tf.estimator.EstimatorSpec:
    """Model function for an MNIST-classifying convolutional neural network.

    Args:
        features (Dict[str, tf.Tensor]): Dictionary of input Tensors.
        labels (Dict[str, tf.Tensor]): Dictionary of label Tensors.
        mode (tf.estimator.ModeKeys): Estimator mode.

    Returns:
        (tf.estimator.EstimatorSpec): MNIST CNN EstimatorSpec.

    """
    # Reshape input
    with tf.name_scope('input'):
        input_layer = tf.reshape(features["x"], [-1, 28, 28, 1])

    # First convolution + pooling block
    with tf.name_scope('conv-block1'):
        # Convolve
        with tf.name_scope('conv'):
            conv1 = tf.layers.conv2d(
                inputs=input_layer,
                filters=32,
                kernel_size=[5, 5],
                padding='valid',
                activation=tf.nn.relu,
                name='conv1')
            # variable_summaries(conv1)

        # Pool
        with tf.name_scope('pool'):
            pool1 = tf.layers.max_pooling2d(inputs=conv1,
                                            pool_size=[2, 2],
                                            strides=2,
                                            name='pool1')

    # Second convolution + pooling block
    with tf.name_scope('conv-block2'):
        # Convolve
        with tf.name_scope('conv'):
            conv2 = tf.layers.conv2d(
                inputs=pool1,
                filters=64,
                kernel_size=[5, 5],
                padding='valid',
                activation=tf.nn.relu,
                name='conv2')
            # variable_summaries(conv2)

        # Pool
        with tf.name_scope('pool'):
            pool2 = tf.layers.max_pooling2d(inputs=conv2,
                                            pool_size=[2, 2],
                                            strides=2,
                                            name='pool2')
    # Dense block
    with tf.name_scope('dense-block'):
        # Flatten the second pooling output
        with tf.name_scope('flatten'):
            pool2_flat = tf.contrib.layers.flatten(pool2)

        # Dense layer with 1024 hidden units
        with tf.name_scope('dense'):
            dense = tf.layers.dense(inputs=pool2_flat,
                                    units=1024,
                                    activation=tf.nn.relu,
                                    name='dense')
            # variable_summaries(dense)

        # Apply dropout during training
        with tf.name_scope('dropout'):
            dropout = tf.layers.dropout(inputs=dense,
                                        rate=0.4,
                                        training=mode == TRAIN,
                                        name='dropout')

    # Compute class logits
    with tf.name_scope('logits'):
        logits = tf.layers.dense(inputs=dropout, units=10, name='logits')
        # variable_summaries(logits)

    # Compute class predictions
    with tf.name_scope('classes'):
        classes = tf.argmax(input=logits, axis=1, name='classes')

    # Compute class probabilities
    with tf.name_scope('probabilities'):
        probabilities = tf.nn.softmax(logits, name='probabilities')

    with tf.name_scope('summaries'):
        pass
        # tf.contrib.layers.summarize_weights()  # tf.GraphKeys.WEIGHTS
        # tf.contrib.layers.summarize_biases()  # tf.GraphKeys.BIASES

    # Both predictions (for PREDICT and EVAL modes)
    predictions = {
        'classes': classes,
        'probabilities': probabilities}

    # For a forward pass, no need to build optimization ops
    if mode == PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode,
                                          predictions=predictions)

    # Calculate loss for TRAIN and EVAL modes
    with tf.name_scope('loss'):
        loss = tf.losses.sparse_softmax_cross_entropy(labels=labels,
                                                      logits=logits)

    with tf.name_scope('train'):
        # Configure the training op
        if mode == TRAIN:
            optimizer = tf.train.AdamOptimizer(learning_rate=1e-3)
            train_op = optimizer.minimize(
                loss=loss,
                global_step=tf.train.get_global_step())
            # Return the training op EstimatorSpec
            return tf.estimator.EstimatorSpec(mode=mode,
                                              loss=loss,
                                              train_op=train_op)

    with tf.name_scope('eval'):
        # Add evaluation metrics for EVAL mode
        eval_metric_ops = {
            'accuracy': tf.metrics.accuracy(labels=labels,
                                            predictions=predictions['classes'])}

        return tf.estimator.EstimatorSpec(mode=mode,
                                          loss=loss,
                                          eval_metric_ops=eval_metric_ops)


class MNISTDataHandler:
    def __init__(self):
        mnist = tf.contrib.learn.datasets.load_dataset('mnist')
        self.train_data = mnist.train.images
        self.train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
        self.eval_data = mnist.test.images
        self.eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

    def train_input_fn(self) -> Callable:
        return tf.estimator.inputs.numpy_input_fn(
                x={'x': self.train_data},
                y=self.train_labels,
                batch_size=50,
                num_epochs=None,
                shuffle=True)

    def eval_input_fn(self) -> Callable:
        return tf.estimator.inputs.numpy_input_fn(
                x={'x': self.eval_data},
                y=self.eval_labels,
                num_epochs=1,
                shuffle=False)


def main(_):
    """Main script routine.

    Args:
        _: Unused.

    Returns: None

    """
    # # Load training and eval data. Apparently deprecated but ¯\_(ツ)_/¯
    # mnist = tf.contrib.learn.datasets.load_dataset('mnist')
    # train_data: np.ndarray = mnist.train.images
    # train_labels = np.asarray(mnist.train.labels, dtype=np.int32)
    # eval_data: np.ndarray = mnist.test.images
    # eval_labels = np.asarray(mnist.test.labels, dtype=np.int32)

    data_handler = MNISTDataHandler()

    # Create an Estimator
    mnist_classifier = tf.estimator.Estimator(model_fn=model_fn,
                                              model_dir='output/mnist')

    # print(mnist_classifier.get_variable_names())

    # Set up a metadata hook
    metadata_hook = gn.MetadataHook(save_steps=1000, model_dir='output/mnist')

    # with tf.name_scope('summaries'):
    #     summary_op = tf.summary.merge_all()
    #
    # # Set up a Summary Saver hook
    # summary_hook = tf.train.SummarySaverHook(
    #     save_steps=50,
    #     output_dir='output/mnist',
    #     summary_op=summary_op)

    # # Training input function
    # train_input_fn = tf.estimator.inputs.numpy_input_fn(
    #     x={'x': train_data},
    #     y=train_labels,
    #     batch_size=50,
    #     num_epochs=None,
    #     shuffle=True)

    # Train the model
    mnist_classifier.train(
        input_fn=data_handler.train_input_fn(),
        steps=5000,
        hooks=[metadata_hook])

    # Evaluate the model

    # # Evaluation input function
    # eval_input_fn = tf.estimator.inputs.numpy_input_fn(
    #     x={'x': eval_data},
    #     y=eval_labels,
    #     num_epochs=1,
    #     shuffle=False)

    # Perform evaluation
    eval_results = mnist_classifier.evaluate(
        input_fn=data_handler.eval_input_fn())

    print(f'Evaluation results:\n{eval_results}')


if __name__ == '__main__':
    tf.app.run()
