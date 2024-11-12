import matplotlib.pylab as plt
from pylab import *
import numpy as np
import glob
import skimage as ski
import skimage.morphology as mp
from skimage.morphology import disk
from skimage import io, filters
from skimage.filters import rank
from skimage.filters.edges import convolve
from skimage.util import img_as_float, img_as_ubyte
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
from ipywidgets import interact, fixed
from matplotlib_inline.backend_inline import flush_figures

columns = 6
rows = 4 

# dimensions of images
images_dim = []


# read every image from file_path
def read_data(file_path):
    images = []
    for filename in glob.glob(file_path + '/*.jpg'):
        image = io.imread(filename)
        images.append(img_as_float(image)) # img_as_float converts from 0-255 to 0-1

        h, w = image.shape[:2]
        images_dim.append([h, w]) 
    return images

# most common value, working for grayscaled images
# probably not that useful
def get_commmon_value(image):
    image = (image * 255).astype(np.uint8) # convert to 0-255 for bincount()
    flattened_image = image.flatten() # flatten to 1 dimensional array
    counts = np.bincount(flattened_image) # count every value
    most_common_value = np.argmax(counts) # get back to 0-1
    return most_common_value / 255

# show collection of images
def show_images(data):
    fig = plt.figure(figsize=(13, 8))

    for i in range(len(data)):
        fig.add_subplot(rows, columns, i + 1)
        plt.imshow(data[i], cmap='gray') # delete gray if not showing gray images
        plt.axis('off')
    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    plt.show()

# convolution with changing to grayscale
def convolve_images(image, k_array):
    k_array = k_array / k_array[k_array > 0].sum()

    if image.ndim == 3:
        image = rgb2gray(image)
    image = convolve(image, k_array)
    
    return image

def contrast(image, perc):
    MIN = np.percentile(image, perc)
    MAX = np.percentile(image, 100-perc)
    norm = (image - MIN) / (MAX - MIN)
    norm[norm[:,:] > 1] = 1
    norm[norm[:,:] < 0] = 0

    return norm

# image binarization
def thresh(image, value):
    binary = (image > value)
    binary = np.uint8(binary)
    
    return binary


if __name__ == '__main__':
    plane_images = read_data("./images/planes")
    fixed_planes = []
    
    for image in plane_images:
        new_image = image

        new_image = convolve_images(new_image, ones([11,11]))
        new_image = new_image ** 0.4
        new_image = contrast(new_image, 0.2)

        noisy_image = img_as_ubyte(new_image)
        new_image =  rank.mean(noisy_image, disk(8)) #filters.median(new_image, disk(4))

        # new_image = thresh(new_image)
        # new_image = filters.sobel(new_image)

        fixed_planes.append(new_image)

    show_images(fixed_planes)