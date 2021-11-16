import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.filters import sobel
import six
import sys
sys.modules['sklearn.externals.six'] = six


def plot(data, name, cmap='gray'):
    """Simple plotting function. This creates and saves a colormap of a given
    two dimensional dataset, with option to specify color scheme."""
    fig = plt.figure(0)
    ax = fig.add_subplot(111)
    ax.imshow(data, cmap=cmap)
    fig.savefig(name + '.png')
    fig.clf()
    return


def img_to_dots(image_name):
    """This function takes the name of an image (no path, no extension,
    assuming you've got an image of that name in the included image/ folder),
    and converts it into an array of (x,y) coordinates representing the
    pixels which comprise the edges of the image."""

    # adds path to image folder
    iname = 'image/' + image_name

    # convert image from jpg to png, if it's not already a png
    # the png format is necessary for doing certain operations on the data
    if os.path.isfile(iname + '.jpg'):
        image = Image.open(iname + '.jpg')
        image.save(iname + '.png')

    # load the image
    image = np.asarray(Image.open(iname + '.png').convert('L'))

    # produce an elevation map using a sobel filter
    elevation_map = sobel(image)

    # normalize the elevation map
    elevation_map /= np.max(elevation_map)

    # these 2 lines convert the continuous data of the elevation map into
    # a set of discreet points. this is necessary for the node generation
    # in the future, because the k-clustering requires specific points to
    # group, as opposed to regions
    # everything with a value above 0.5 IS an edge, everything else is not
    elevation_map[elevation_map < 0.5] = 0
    elevation_map[elevation_map > 0.5] = 1

    # plot the elevation map
    plot(elevation_map, iname + '_elevation')

    # calculate the midpoint of the image
    # this is necessary to translate the coordinates of the image to be
    # centered around the midpoint, as opposed to 0,0. the reason for this
    # will be more obvious when seeing the fourier xform in action
    xmid = image.shape[1] // 2
    ymid = image.shape[0] // 2

    # loop through each pixel
    points = []
    for i in range(image.shape[1]):
        for j in range(image.shape[0]):

            # store the x, y of the edge points (all the values equal to 1)
            if elevation_map[j, i]:
                points.append((i - xmid, ymid - j))

    # convert these from a list to an np array so we can do maths and plot
    points = np.array(points).astype(float)

    # plot the dots (which are really the edges)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(points[:, 0], points[:, 1], lw=0.3, marker='o', ms=0.4)
    fig.savefig(iname + '_dots.png')
    fig.clf()

    # the reason we normalize here is to scale the dots onto a 2x2 image
    # or, an image that goes from -1 to 1.
    # doing this earlier prevents downstream issues with scaling the
    # fourrier xform
    points /= np.max(points)

    # now tuples will be our preferred way of storing these points
    points = [(x, y) for x, y in points]

    # after some future changes to the code, this step is likely not
    # necessary but I don't want to break anything by removing it.
    # so, the reason I sorted the points by theta is that, for the
    # fourrier xform, it is necessary to have not only a set of points,
    # but to have those points ordered. since or algorithm works by
    # 'spinning', sorting them by theta gave us a nice first approximation
    # to how we should order our points. this created a few issues
    # with certain types of images, but those have been solved by
    # more complex algorithms. the order of the points should no
    # longer matter, but there's should be no issue with keeping this
    # line
    points = sorted(points, key=lambda x: np.arctan2(x[1], x[0]))

    # back to np.array for plotting
    points = np.array(points).astype(float)

    # plot the dots
    # the difference in THIS plotting function is that the points are
    # now ordered via theta
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.plot(points[:, 0], points[:, 1], lw=0.3, marker='o', ms=0.4)
    fig.savefig(iname + '_dots.png')
    fig.clf()

    # the punchline of this function is to return the set of points
    # to be used in the kmeans classifier
    return points


if __name__ == '__main__':
    """You can run this script by itself for debugging."""
    img_to_dots('peace')
