
# Dense cellular segmentation using 2D-3D neural network ensembles for electron microscopy

> Modern biological electron microscopy produces nanoscale images from biological samples of unprecedented volume, and researchers now face the problem of making use of the data. Image segmentation has played a fundamental role in EM image analysis for decades, but challenges from biological EM have spurred interest and rapid advances in computer vision for automating the segmentation process. In this paper, we demonstrate dense cellular segmentation as a method for generating rich, 3D models of tissues and their constituent cells and organelles from scanning electron microscopy images. We describe how to use ensembles of 2D-3D neural networks to compute dense cellular segmentations of cells and organelles inside two human platelet tissue samples. We conclude by discussing ongoing challenges for realizing practical dense cellular segmentation algorithms.

## Full text

[Read on Biorxiv](https://www.biorxiv.org/content/addactuallinkhere)

## Data

[Download ZIP](https://www.dropbox.com/s/68yclbraqq1diza/platelet_data_1219.zip) (180 MB)

## Examples

Examples of training and using neural nets for segmenting 3D biomedical SEM images

### Setup

#### Requirements

This setup was tested on Ubuntu 18.04 with an NVIDIA GTX 1080, using Python 3.6 and TensorFlow 1.15. Information for installing TensorFlow 1.15 with GPU support can be found at [https://www.tensorflow.org/install/gpu](https://www.tensorflow.org/install/gpu).

#### Clone repo

To get all examples, we recommend using `git` to clone our example repo. Zipped source code for each example can also be found in the example descriptions below.

```bash
git clone https://github.com/leapmanlab/examples
cd examples
```

#### Python setup

We recommend using a Python virtual environment. Install packages from _examples/requirements.txt_.

```bash
python3 -m venv leapmanlab
source leapmanlab/bin/activate
pip3 install -r requirements.txt
# Add a jupyter kernel for the venv
ipython kernel install --user --name=leapmanlab
```

You should now be able to run example notebooks! Each folder within _examples_ contains a separate, self-contained example.


### Example 1: Training a U-Net

Training a U-Net from (Ronneberger et al., 2015) [PDF](https://arxiv.org/pdf/1505.04597.pdf) for platelet segmentation.

If you cloned the repo above, have the venv active, and are in the _examples_ root directory, you can view the Example 1 notebook locally with

```bash
cd unet
jupyter notebook example1_train_unet.ipynb
```

[View Notebook](example1_train_unet.html)

[Download Source](path/to/src.zip)

