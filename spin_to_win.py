import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from picture_perfect import img_to_dots
from node_finder import node_finder


def compute_coefficients(ns, data):
    """Used by the spin function, this computes the coefficients for
    the fourrier transform. The math here is fairly straightforward,
    but for a demonstration for how one arrives at the equation used,
    I recommend visiting https://www.youtube.com/watch?v=r6sGWTCMz2k&vl=en
    to see it worked out."""
    cs = []
    for n in ns:
        s = complex(0, 0)
        for i, datum in enumerate(data):
            t = i / len(data)
            dt = 1 / len(data)
            d = complex(*datum)
            s += d * np.exp(-n * 2 * np.pi * complex(0, 1) * t) * dt
        cs.append(s)
    return(cs)


def spin(N, f, ani_name):
    """Produces a .gif of a fourier approximation of a given set of points,
    using N, a number of fourier terms, as well as f, a list of points to
    be approximated. ani_name is the desired name of the animation. The
    docstring for compute_coefficients contains the youtube video which
    demonstrates the maths used in this approximation."""
    # the time ordinates used in the animation
    # this produces 3 full rotations
    times = np.linspace(0, 2, 500)

    # function for selecting the terms given the desired order
    # ex. if N=5, terms are (0, 1, -1, 2, -2)
    ns = []
    for nnn in range(N):
        ns.append(-nnn // 2 if not nnn % 2 else nnn // 2 + 1)

    # computes the coefficients given the list of points
    cs = compute_coefficients(ns, f)

    # function for computing the individual terms now that we've got the
    # coefficients
    def term(c_n, n, t):
        """Returns the nth term for the series, given coefficients and the
        timestep."""
        return c_n * np.exp(n * 2 * np.pi * t * complex(0, 1))

    # initialize a container for storing the data for each timestep and loop
    # through times
    data = []
    for t in times:

        # the first x, y coordinates of any line in the animation will be
        # at the origin (0, 0)
        step = [[0], [0]]

        # now we'll look at each term individually
        for i in range(len(ns)):

            # pull the order & coefficient for the term
            n = ns[i]
            c_n = cs[i]

            # first, compute the term,
            # then, add the term to the endpoint of the previous term
            step[0].append(step[0][-1] + term(c_n, n, t).real)
            step[1].append(step[1][-1] + term(c_n, n, t).imag)

        # append the data to the master container
        data.append(step)

    # setup the plotting environment
    fig = plt.figure(0, figsize=(30, 30))
    ax = fig.add_subplot(111)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    # the following few lines initialize the figure
    # this plots the spaghetti segment
    seg = ax.plot(data[0][0], data[0][1], c='seagreen')[0]

    # this is the endpoint
    point = ax.plot(data[0][0][-1], data[0][1][-1],
                    c='mediumspringgreen', marker='o', ms=2)[0]

    # because we store every point, this is plotted separately, not just
    # updated like the line
    line_x = []
    line_y = []
    line_x.append(data[0][0][-1])
    line_y.append(data[0][1][-1])
    line = ax.plot(data[0][0][-1], data[0][1][-1], c='mediumspringgreen')[0]

    # a function used in mpl animation
    def animate(i):
        """This function is necessary to do an mpl animation. The variable
        i is used to update the image."""
        # this updates the spaghetti arms
        seg.set_xdata(data[i][0])
        seg.set_ydata(data[i][1])

        # this updates the endpoints on the spaghetti (fourier arms)
        point.set_xdata(data[i][0][-1])
        point.set_ydata(data[i][1][-1])

        # this updates the actual line of the image
        # this includes storing the previous lines, so
        # we continuously update the image or 'draw' it
        line_x.append(data[i][0][-1])
        line_y.append(data[i][1][-1])
        line.set_xdata(line_x)
        line.set_ydata(line_y)
        return

    # initialize the animation environment
    fig.set_size_inches(10, 10)

    # this controls the animation
    # all integers are in ms (I believe)
    ani = animation.FuncAnimation(fig, animate, frames=len(times),
                                  interval=50, repeat_delay=2000)

    # and finally, save the animation as a .gif
    ani.save('image/' + ani_name + '.gif')
    return


def test_circle_function():
    """This function produces points in a circle, for use in
    debugging the spin function."""
    r = 5
    theta = np.linspace(0, 2 * np.pi, 7)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    sf = np.max(x + y)
    x /= sf
    y /= sf
    return list(zip(x, y))


if __name__ == '__main__':
    """You can run this script by itself for debugging, though
    this requires running the other functions, too, to produce
    inputs for this one."""
    N = 50
    points = img_to_dots('peace')
    nodes, _ = node_finder(points, 'peace')
    spin(N, nodes, 'peace')
