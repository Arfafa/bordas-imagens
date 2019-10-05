import os

import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

PATH = 'images'
IMAGES_LIST = os.listdir(PATH)
SIGMA = np.linspace(2, 10, 9)
# SIGMA = [5.0]

DOG_IMAGES_DIR = 'dog_images'
LOG_IMAGES_DIR = 'log_images'
LIM_IMAGES_DIR = 'lim_images'
BIN_IMAGES_DIR = 'borders'


def gaussian2D(sigma):
    x, y = np.meshgrid(np.linspace(-128, 128, 256),
                       np.linspace(-128, 128, 256))

    z = x**2 + y**2
    z = z/(2*sigma**2)
    z = np.exp(-z)

    return z


def laplacian2D():
    x, y = np.meshgrid(np.linspace(-128, 128, 256),
                       np.linspace(-128, 128, 256))

    z = -(x**2 + y**2)

    return z


def find_boards(img):
    img_copy = np.copy(img)

    for i in range(256):
        for j in range(256):

            if(img[i, j]):
                up = i-1
                down = i+1
                left = j-1
                right = j+1

                aux = True if(up < 0 or
                              down > 255 or
                              left < 0 or
                              right > 255) else False

                if(up > -1 and not aux):
                    aux = True if(img[up, j] == 0) else False

                if(down < 256 and not aux):
                    aux = True if(img[down, j] == 0) else False

                if(left > -1 and not aux):
                    aux = True if(img[i, left] == 0) else False

                if(right < 256 and not aux):
                    aux = True if(img[i, right] == 0) else False

                if(not aux):
                    img_copy[i, j] = 0

    return img_copy


def main():

    if(DOG_IMAGES_DIR not in os.listdir()):
        os.mkdir(DOG_IMAGES_DIR)

    if(LOG_IMAGES_DIR not in os.listdir()):
        os.mkdir(LOG_IMAGES_DIR)

    if(LIM_IMAGES_DIR not in os.listdir()):
        os.mkdir(LIM_IMAGES_DIR)

    if(BIN_IMAGES_DIR not in os.listdir()):
        os.mkdir(BIN_IMAGES_DIR)

    z = laplacian2D()
    shifted_laplacian = np.fft.ifftshift(z)

    for sig in SIGMA:

        z = gaussian2D(sig)
        shifted_gaussian = np.fft.ifftshift(z)

        for image in IMAGES_LIST:
            image_path = '{}/{}'.format(PATH, image)

            img = mpimg.imread(image_path)

            freq = np.fft.fft2(img)

            dog_freq = freq*shifted_gaussian

            log_freq = dog_freq*shifted_laplacian

            dog_img = np.fft.ifft2(dog_freq)

            log_img = np.fft.ifft2(log_freq)

            lim_img = np.where(np.real(log_img) > 0, 1, 0)

            bin_img = find_boards(lim_img)

            dic = {DOG_IMAGES_DIR: dog_img,
                   LOG_IMAGES_DIR: log_img,
                   LIM_IMAGES_DIR: lim_img,
                   BIN_IMAGES_DIR: bin_img}

            for k, v in dic.items():
                fig = plt.imshow(np.real(v), cmap='gray')
                plt.axis('off')

                fig.axes.get_xaxis().set_visible(False)
                fig.axes.get_yaxis().set_visible(False)

                name = '{}/sigma={}_{}'.format(k, sig, image)

                plt.savefig(name, bbox_inches='tight', pad_inches=0)


if(__name__ == '__main__'):
    main()
