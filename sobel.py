import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def sobel(image_name):
    """A sobel filter."""

    # convert image to greyscale
    iname = 'image/' + image_name

    # convert image from jpg to png
    if os.path.isfile(iname + '.jpg'):
        image = Image.open(iname + '.jpg')
        image.save(iname + '.png')

    # test image
    image = np.asarray(Image.open(iname + '.png').convert('L'))
    plt.imshow(image)

    # filter image
    filtered_image = np.zeros(image.shape)
    X_derivative = np.zeros(image.shape)
    Y_derivative = np.zeros(image.shape)
    m, n = image.shape

    # sobel matrices
    G_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    G_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    # the loops
    for i in range(m)[1:-1]:
        for j in range(n)[1:-1]:
            S1 = np.sum(G_x * image[i-1:i+2, j-1:j+2])
            S2 = np.sum(G_y * image[i-1:i+2, j-1:j+2])
            X_derivative[i, j] = S1
            Y_derivative[i, j] = S2
            filtered_image[i, j] = np.sqrt(S1**2 + S2**2)

    # normalize
    filtered_image = (filtered_image / np.max(filtered_image)) * 255

    # show image
    plt.figure(0)
    plt.imshow(X_derivative)
    plt.figure(1)
    plt.imshow(Y_derivative)
    plt.figure(2)
    plt.imshow(filtered_image)

    # save image
    save_image = Image.fromarray(filtered_image)
    save_image = save_image.convert('L')
    save_image.save(iname + '_sobel.png')
    return


if __name__ == '__main__':
    sobel('lamp')
