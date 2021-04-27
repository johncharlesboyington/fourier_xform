import numpy as np
import matplotlib.pyplot as plt
from numpy.random import randint
from picture_perfect import img_to_dots
from node_finder import node_finder
from spin_to_win import spin


def distance(a, b):
    return np.sqrt(np.sum((a - b)**2))


def best_first_search(nodes, connections, image_name):
    """best_first_search"""

    # containers
    node_indices = list(range(len(nodes)))
    final_path = []
    node_list = list(np.array(node_indices))
    current_node = node_list[0]
    node_list.remove(current_node)
    final_path.append(current_node)

    # start the loop
    while node_list:
        print('\n\n\n -------------------------------------------------------')
        print('Node List:', node_list)

        # define the start
        start_node = final_path[-1]
        print('Start:', start_node)

        # define the goal
        goal_node = node_list[np.argmin([distance(nodes[start_node], nodes[g]) for g in node_list])]
        node_list.remove(goal_node)
        print('Goal:', goal_node)

        # best first search
        start_distance = distance(nodes[start_node], nodes[goal_node])
        open_list = [(start_node, start_distance)]
        closed_list = []

        while True:

            # get the adjacent nodes
            adjacent_nodes = connections[open_list[0][0]]
            print('\nCurrent Node:', open_list[0][0])
            print('Adjacent Nodes:', adjacent_nodes)

            # move the current search node to the closed list
            closed_list.append(open_list.pop(0)[0])
            print('Closed List:', closed_list)

            # add the adjacent nodes and their heuristics to the open list
            for node in adjacent_nodes:
                if node not in closed_list:
                    open_list.append((node, distance(nodes[node], nodes[goal_node])))

            # order by distance
            open_list.sort(key=lambda x: x[1])
            print('Sorted Open List:', open_list)

            # if we find the goal, great
            if goal_node == open_list[0][0]:

                # calculate and return the path back to the start
                path_home = [goal_node]
                while path_home[-1] != start_node:
                    print('Path Home:', path_home)
                    for node in connections[path_home[-1]]:
                        if node in closed_list:
                            path_home.append(node)
                            closed_list.remove(node)
                            break
                for node in path_home[::-1][1:]:
                    final_path.append(node)
                break

    # final ordinates
    final_ordinates = []
    for node_index in final_path:
        final_ordinates.append(nodes[node_index])

    # plotting
    fig = plt.figure(0)
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111)
    ax.plot(*np.array(final_ordinates).T)

    fig.savefig('image/' + image_name + '_path.png')
    fig.clf()
    return final_ordinates


if __name__ == '__main__':
    img_name = 'maple'
    points = img_to_dots(img_name)
    nodes, connections = node_finder(200, points, img_name)
    ordered_nodes = best_first_search(nodes, connections, img_name)
    spin(len(ordered_nodes), ordered_nodes, img_name)
