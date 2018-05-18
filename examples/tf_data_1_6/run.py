"""Experimenting with the TensorFlow 1.6 Dataset API.

"""
import math
import time
import os

import numpy as np
import tifffile as tif


from typing import Optional, Sequence, Tuple


def generate_windows(window_shape: Sequence[int],
                     data_dir: str,
                     window_spacing: Sequence[int]=None,
                     jitter_seed: int=None,
                     normalize: bool=True,
                     train_file: Optional[str]='train-volume.tif',
                     label_file: Optional[str]='label-volume.tif',
                     weight_file: Optional[str]='weight-volume.tif') \
        -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """TODO

    Args:
        window_shape (Sequence[int]): A sequence of 2 or 3 ints specifying
            the shape of each window to be generated.
        data_dir (str): String specifying the location of the source
            training data, training labels, and training error weight files.
        window_spacing (Sequence[int]): Spacing between the corners of
            consecutive windows along each spatial axis. Should be in
            (dx, dy) format for 2D windows, and (dz, dx, dy) format for 3D
            windows.
        jitter_seed (int): Window corners are chosen randomly from a small
            interval for added variability. This seed controls the random
            number generator used to produce the corner locations.
        normalize (bool): If True, normalize training data to have mean 0 and
            variance 1 before creating windows
        train_file (Optional[str]): Name of the training data image volume
            within the data_dir.
        label_file (Optional[str]): Name of the training label image volume
            within the data_dir.
        weight_file (Optional[str]): Name of the error weighting image volume
            within the data_dir.

    Returns:

    """
    train_volume: Optional[np.ndarray] = None
    label_volume: Optional[np.ndarray] = None
    weight_volume: Optional[np.ndarray] = None

    # Make 2D stuff 3D
    if len(window_shape) == 2:
        window_shape = [1] + list(window_shape)
    if len(window_spacing) == 2:
        window_spacing = [1] + list(window_spacing)

    # Default window spacing: 20 window corner points along each axis
    if window_spacing is None:
        window_spacing = [max(1, int(s / 20)) for s in window_shape]

    if train_file is not None:
        train_volume = \
            tif.imread(os.path.join(data_dir, train_file)).astype(np.float32)
        if normalize:
            train_volume -= np.mean(train_volume)
            train_volume /= np.std(train_volume)

    if label_file is not None:
        label_volume = \
            tif.imread(os.path.join(data_dir, label_file)).astype(np.uint16)

    if weight_file is not None:
        weight_volume = \
            tif.imread(os.path.join(data_dir, label_file)).astype(np.float32)

    # Choose window corners. Given N corner points along an axis, divide the
    # usable axis length L into N bins such that bin i is the interval
    # [ L*i/(N+1), L*(i+1)/(N+1) ). Corner point i is chosen at random from bin
    # i. The usable axis length L along a given axis is equal to the total axis
    # length minus the window size along the axis.
    vol_shape = train_volume.shape
    grid_points = []

    np.random.seed(jitter_seed)

    for i in range(len(window_shape)):
        v = vol_shape[i]
        w = window_shape[i]
        d = window_spacing[i]

        usable_length = v - w

        num_bins = int(math.ceil(usable_length / d))

        bins = [min(d * i, usable_length) for i in range(num_bins + 1)]

        gridi = [np.random.randint(bins[i], bins[i + 1])
                 for i in range(num_bins)]

        grid_points.append(gridi)

    # Create windows

    n_windows = 1
    for el in grid_points:
        n_windows *= len(el)

    array_shape = [n_windows] + list(window_shape)

    train_array = np.zeros(array_shape, dtype=np.int16)
    label_array = np.zeros(array_shape, dtype=np.uint16)
    weight_array = np.zeros(array_shape, dtype=np.float32)

    dz = window_shape[0]
    dx = window_shape[1]
    dy = window_shape[2]

    window_idx = 0
    for z in grid_points[0]:
        for x in grid_points[1]:
            for y in grid_points[2]:
                train_array[window_idx, ...] = train_volume[z:(z + dz),
                                                            x:(x + dx),
                                                            y:(y + dy)]

                label_array[window_idx, ...] = label_volume[z:(z + dz),
                                                            x:(x + dx),
                                                            y:(y + dy)]
                weight_array[window_idx, ...] = weight_volume[z:(z + dz),
                                                              x:(x + dx),
                                                              y:(y + dy)]
                window_idx += 1

    return train_array, label_array, weight_array


nibib_dir = '../../../../..'
platelet_dir = os.path.join(nibib_dir, 'data/platelet')

t0 = time.time()
t, l, w = generate_windows((1, 200, 200),
                           platelet_dir,
                           [1, 40, 40],
                           0)
t1 = time.time()

print(f'Elapsed time is {t1 - t0}')
print(f'{t.shape}')

time.sleep(10)
