import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def sobel(image_name):
    """A homemade sobel filter. Used to approximate the derivate
    of an image, which acts as an edge detector. I encourage the
    reader to review how a sobel filter works to help understand
    how this function operates."""

    # adds a path to the image name
    iname = 'image/' + image_name

    # convert image from jpg to png if it's not already
    if os.path.isfile(iname + '.jpg'):
        image = Image.open(iname + '.jpg')
        image.save(iname + '.png')

    # this opens the image as a greyscale numpy array
    image = np.asarray(Image.open(iname + '.png').convert('L'))
    plt.imshow(image)

    # open containers used for the algorithm
    filtered_image = np.zeros(image.shape)
    X_derivative = np.zeros(image.shape)
    Y_derivative = np.zeros(image.shape)

    # grab the shape of the image
    m, n = image.shape

    # sobel matrices, used in approximating the derivative
    G_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    G_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    # loop through everything but the outer edge
    for i in range(m)[1:-1]:
        for j in range(n)[1:-1]:

            # calculate the S1 and S2 (sums)
            S1 = np.sum(G_x * image[i-1:i+2, j-1:j+2])
            S2 = np.sum(G_y * image[i-1:i+2, j-1:j+2])

            # store these, which are the derivative approximates
            # at those particular points
            X_derivative[i, j] = S1
            Y_derivative[i, j] = S2

            # euclidean norm is used to combine the two derivatives
            filtered_image[i, j] = np.sqrt(S1**2 + S2**2)

    # due to the greyscale format used when importing the image,
    # the following normalizes the image (max value = 1)
    filtered_image = (filtered_image / np.max(filtered_image)) * 255

    # show images of the derivatives
    plt.figure(0)
    plt.imshow(X_derivative)
    plt.figure(1)
    plt.imshow(Y_derivative)
    plt.figure(2)
    plt.imshow(filtered_image)

    # save the sobel image
    save_image = Image.fromarray(filtered_image)
    save_image = save_image.convert('L')
    save_image.save(iname + '_sobel.png')
    return


if __name__ == '__main__':
    """You can run this script by itself for debugging."""
    sobel('lamp')
