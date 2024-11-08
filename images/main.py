from __future__ import division
from pylab import *
import skimage as ski
from skimage import data, io, filters, exposure
from skimage.filters import rank
from skimage import img_as_float, img_as_ubyte
from skimage.morphology import disk
import skimage.morphology as mp
from skimage import util
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from skimage.filters.edges import convolve
from matplotlib import pylab as plt
import numpy as np
from numpy import array
from IPython.display import display
from ipywidgets import interact, interactive, fixed
from ipywidgets import *
from matplotlib_inline.backend_inline import flush_figures
import glob

columns = 6
rows = 4

# dimensions of images
images_dim = []

def read_data(file_path):
    images = []
    for filename in glob.glob(file_path + '/*.jpg'):
        image = io.imread(filename)
        images.append(img_as_float(image)) # img_as_float converts from 0-255 to 0-1

        h, w = image.shape[:2]
        images_dim.append([h, w]) 
    return images

def show_images(data):
    fig = plt.figure(figsize=(13, 8))

    for i in range(len(data)):
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(data[i], cmap='gray') # delete gray if not showing gray images
        plt.axis('off')
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.show()

def convolve_images(data):
    SIZE=5
    K = ones([SIZE,SIZE])
    K = K / sum(K)

    new_data = []
    for image in data:
        if image.ndim == 3:
            image = rgb2gray(image)
        new_data.append(convolve(image, K))
    
    return new_data


if __name__ == '__main__':
    plane_images = read_data("./images/planes")

    fixed_planes = convolve_images(plane_images)
    show_images(fixed_planes)