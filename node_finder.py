import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
from picture_perfect import img_to_dots


def node_finder(N, points, image_name):
    """node_finder"""

    # cluster
    kmeans = KMeans(n_clusters=N, random_state=0).fit(points)

    # plot the clustered data
    # initialize plotting environment
    fig = plt.figure(0)
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111)

    # create colors
    colors = sns.color_palette("hls", N)

    # plot the clusters
    # for i in range(len(points)):
    #     ax.plot(*points[i], color=colors[kmeans.labels_[i]], marker='o',
    #             ms=0.2)

    # plot the centroids
    for i in range(N):
        ax.plot(*kmeans.cluster_centers_[i], color=colors[i], marker='*', ms=5)

    # ------------------------------------------------------------------------
    # new stuff

    # distance function
    def distance(a, b):
        return np.sqrt(np.sum((a - b)**2))
    
    max_dist = np.zeros(N)
    
    for i in range(len(points)):
        centroid = kmeans.cluster_centers_[kmeans.labels_[i]]
        dist = distance(points[i], centroid)
        if dist > max_dist[kmeans.labels_[i]]:
            max_dist[kmeans.labels_[i]] = dist
    
    # plot the circles
    for i in range(N):
        circle = plt.Circle(kmeans.cluster_centers_[i], max_dist[i],
                            fill=False, color=colors[i])
        ax.add_artist(circle)
        

    # connections
    connections = []
    for i in range(N):
        connection = []
        min_dist = np.inf
        for j in range(N):
            
            # skip if selfe
            if i == j:
                continue
            
            # compute distance between two points
            node_dist = distance(kmeans.cluster_centers_[i],
                                 kmeans.cluster_centers_[j])

            # compute relevent distance
            relevent_dist = max_dist[i] + max_dist[j]
            
            # min dist
            if min_dist > node_dist:
                min_dist = node_dist
                min_node = j
            

            # if it's less, it's a connection
            if (relevent_dist * 1.2) > node_dist:
                connection.append(j)
                
        if not connection:
            connection = [min_node]
        connections.append(connection)
        
    
    # plot the connections
    for i in range(N):
        a = kmeans.cluster_centers_[i]
        for j in connections[i]:
            b = kmeans.cluster_centers_[j]
            
            ax.plot([a[0], b[0]], [a[1], b[1]], color='k', lw=0.8)
        
        
    
        
    
    
    
    
    
    # save
    fig.savefig('image/' + image_name + '_nodes.png')
    fig.clf()

    return kmeans.cluster_centers_, connections


if __name__ == '__main__':
    points = img_to_dots('peace')
    node_finder(points, 'peace')
