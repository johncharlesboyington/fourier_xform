import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
from picture_perfect import img_to_dots


def node_finder(N, points, image_name):
    """This function collapses a series of x,y points (which represent edges
    in the context of this project), and collapses them into a set of nodes
    via k-means clustering, and an array of connecting paths between those
    nodes. The input value 'N' is the number of nodes the user would like
    the data collapsed down to."""

    # honestly, all the clustering magic happens right here
    kmeans = KMeans(n_clusters=N, random_state=0).fit(points)

    # plot the clustered data
    # initialize plotting environment
    fig = plt.figure(0)
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111)

    # create colors
    colors = sns.color_palette("hls", N)

    # plot the centroids, as found via kmeans
    for i in range(N):
        ax.plot(*kmeans.cluster_centers_[i], color=colors[i], marker='*', ms=5)

    # here begins the 'connection finding' portion of the function
    # distance function
    def distance(a, b):
        return np.sqrt(np.sum((a - b)**2))

    # for the following block of code, the final purpose is to find, for
    # each node/centroid, the distance between that node to the furthest
    # point represented (classified) by that node
    # this is necessary for describing the connections between those nodes
    max_dist = np.zeros(N)
    for i in range(len(points)):
        centroid = kmeans.cluster_centers_[kmeans.labels_[i]]
        dist = distance(points[i], centroid)
        if dist > max_dist[kmeans.labels_[i]]:
            max_dist[kmeans.labels_[i]] = dist

    # here, we plot these max distances by using circles to represent
    # these maximum radii from each node. these are placed over the nodes
    # which were added to the figure earlier
    for i in range(N):
        circle = plt.Circle(kmeans.cluster_centers_[i], max_dist[i],
                            fill=False, color=colors[i])
        ax.add_artist(circle)

    # now, this block is dedicated to finding the connections between the
    # nodes. further down the pipeline, this will be used to order the
    # nodes via best first search. the following block takes each node
    # and stores a connection if the nodes radii (as found just above) are
    # overlapping, and in the case that a node doesn't overlap with any
    # other, finds the nearest node and connects it with only that one
    connections = []
    for i in range(N):
        connection = []
        min_dist = np.inf
        for j in range(N):

            # skip if self
            if i == j:
                continue

            # compute distance between two points
            node_dist = distance(kmeans.cluster_centers_[i],
                                 kmeans.cluster_centers_[j])

            # compute relevent distance
            # this is the sum of the radii calculated earlier
            relevent_dist = max_dist[i] + max_dist[j]

            # this continually updates the node closest to the current
            # node in consideration, for use in the event that the node
            # doesn't have any overlapping neighbors
            if min_dist > node_dist:
                min_dist = node_dist
                min_node = j

            # this is somewhat arbitrary, but it was necessary (for maths
            # sake) to add a fudge factor when determining these connecting
            # nodes. basically, in reality, we're not checking if the radii
            # overlap, but that the sum of the radii PLUS 20% overlaps.
            # this will lead to more connections, as opposed to less,
            # and in the future, should be a user-determined value,
            # but for now, I've found that 20% works well for a lot of
            # cases
            if (relevent_dist * 1.2) > node_dist:
                connection.append(j)

        # here's where we store the closed node as a connection in the case
        # that the node doesn't overlap with any others
        if not connection:
            connection = [min_node]
        connections.append(connection)

    # this block plots and saves the connection on top of the
    # already-plotted nodes and radii
    for i in range(N):
        a = kmeans.cluster_centers_[i]
        for j in connections[i]:
            b = kmeans.cluster_centers_[j]
            ax.plot([a[0], b[0]], [a[1], b[1]], color='k', lw=0.8)
    fig.savefig('image/' + image_name + '_nodes.png')
    fig.clf()

    # we're going to return both the nodes and their connections
    return kmeans.cluster_centers_, connections


if __name__ == '__main__':
    """You can run this script by itself for debugging."""
    points = img_to_dots('peace')
    node_finder(points, 'peace')
