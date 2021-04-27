import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.filters import sobel
import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose


def plot(data, name, cmap='gray'):
    fig = plt.figure(0)
    ax = fig.add_subplot(111)
    ax.imshow(data, cmap=cmap)
    fig.savefig(name + '.png')
    fig.clf()


def img_to_dots(image_name):
    iname = 'image/' + image_name

    # convert image from jpg to png
    if os.path.isfile(iname + '.jpg'):
        image = Image.open(iname + '.jpg')
        image.save(iname + '.png')

    # test image
    image = np.asarray(Image.open(iname + '.png').convert('L'))
    elevation_map = sobel(image)
    elevation_map /= np.max(elevation_map)
    elevation_map[elevation_map < 0.5] = 0
    elevation_map[elevation_map > 0.5] = 1
    plot(elevation_map, iname + '_elevation')

    # calculate the midpoints
    xmid = image.shape[1] // 2
    ymid = image.shape[0] // 2

    # loop through each pixel
    points = []
    for i in range(image.shape[1]):
        for j in range(image.shape[0]):

            # store the ones
            if elevation_map[j, i]:
                points.append((i - xmid, ymid - j))
    points = np.array(points).astype(float)

    # plot the dots
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(points[:, 0], points[:, 1], lw=0.3, marker='o', ms=0.4)
    fig.savefig(iname + '_dots.png')
    fig.clf()

    points /= np.max(points)
    #points = points[::len(points) // 500]
    points = [(x, y) for x, y in points]

    # sort by theta
    points = sorted(points, key=lambda x: np.arctan2(x[1], x[0]))

    points = np.array(points).astype(float)
    # plot the dots
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(points[:, 0], points[:, 1], lw=0.3, marker='o', ms=0.4)
    fig.savefig(iname + '_dots.png')
    fig.clf()
    return points


if __name__ == '__main__':
    img_to_dots('peace')
