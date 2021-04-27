import numpy as np
import matplotlib.pyplot as plt
from numpy.random import randint
from picture_perfect import img_to_dots
from node_finder import node_finder
from spin_to_win import spin


def distance(a, b):
    return np.sqrt(np.sum((a - b)**2))


def order_nodes(nodes, connections, image_name):
    """order_nodes"""

    # containers
    node_indices = list(range(len(nodes)))
    final_path = []
    node_list = list(np.array(node_indices))
    current_node = node_list[0]
    node_list.remove(current_node)
    final_path.append(current_node)

    # main loop
    for i in range(1000):

        if not node_list:
            break
        
        # select next
        options = connections[current_node]

        # if at least one option is in node list
        # this next code is super dope my guy
        if True in [v in node_list for v in options]:

            for option in options:
                if option in node_list:

                    # update
                    current_node = option
                    node_list.remove(current_node)
                    final_path.append(current_node)
                    break
                else:
                    continue

        # else pick a random node
        else:
            current_node = options[randint(0, len(options))]
            final_path.append(current_node)

    # final ordinates
    final_ordinates = []
    for node_index in final_path:
        final_ordinates.append(nodes[node_index])
    
    # plotting
    fig = plt.figure(0)
    ax = fig.add_subplot(111)
    ax.plot(*np.array(final_ordinates).T)
    
    fig.savefig('image/' + image_name + '_path.png')
    fig.clf()
    return final_ordinates


if __name__ == '__main__':
    img_name = 'czechia'
    points = img_to_dots(img_name)
    nodes, connections = node_finder(80, points, img_name)
    ordered_nodes = order_nodes(nodes, connections, img_name)
    spin(len(ordered_nodes), ordered_nodes, img_name)
