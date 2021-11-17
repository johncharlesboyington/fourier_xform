import numpy as np
import matplotlib.pyplot as plt
from picture_perfect import img_to_dots
from node_finder import node_finder
from spin_to_win import spin


def distance(a, b):
    """Given two points (len 2 np.arrays), returns the euclidean distance
    between the two."""
    return np.sqrt(np.sum((a - b)**2))


def best_first_search(nodes, connections, image_name):
    """Given a set of nodes, and a set of connecting paths between those
    points, returns an optimal path (a short path) which connects all of
    the nodes in the list using best first searching. The image_name is
    used for storing plots."""

    # used to print debugging info to study the algorithm!
    debug = False

    # initialize some containers for use in our algorithm
    node_indices = list(range(len(nodes)))
    final_path = []
    node_list = list(np.array(node_indices))

    # starting point is fairly arbitrary, the first point in our node list
    # technically, it's the point with the lowest theta, due to sorting
    # in the node_finder
    current_node = node_list[0]

    # whenever we have touched a new node, it'll be appended to our path
    # and removed from the list of nodes we still need to travel to
    node_list.remove(current_node)
    final_path.append(current_node)

    # a flag telling us whether our path has brought us home, yet
    # this is necessary to complete an image, drawing the final curve
    # to get us from the last point in our path back to the first point
    #  in the path
    home_flag = False

    # we're going to loop as still as there's open nodes in our list
    while node_list:

        # for debugging purposes, this shows the existing list of
        # remaining nodes at each step
        if debug:
            print('\n\n\n --------------------------------------------------')
            print('Node List:', node_list)

        # for this step of the iteration, define the starting point for
        # our search algorithm.
        start_node = final_path[-1]
        if debug:
            print('Start:', start_node)

        # define the goal to be the node which is the CLOSEST node to
        # the current node which hasn't been removed from the open
        # node list and remove it from the open node list
        goal_node = node_list[np.argmin([distance(nodes[start_node], nodes[g])
                                         for g in node_list])]
        node_list.remove(goal_node)
        if debug:
            print('Goal:', goal_node)

        # this is to make sure the algorithm gets back to the beginning!
        # this avoids some weird lines being drawn back to the start
        if not home_flag and len(node_list) == 0:
            home_flag = True
            node_list.append(final_path[0])

        # if the reader is unfamiliar with best first search,
        # it may be good to review how that works to better understand
        # the following block of code
        # initialize the algorithm
        start_distance = distance(nodes[start_node], nodes[goal_node])
        open_list = [(start_node, start_distance)]
        closed_list = []

        # loop for searching
        while True:

            # get the adjacent nodes
            adjacent_nodes = connections[open_list[0][0]]
            if debug:
                print('\nCurrent Node:', open_list[0][0])
                print('Adjacent Nodes:', adjacent_nodes)

            # move the current search node to the closed list
            closed_list.append(open_list.pop(0)[0])
            if debug:
                print('Closed List:', closed_list)

            # add the adjacent nodes and their heuristics to the open list
            # in this case, the heuristic is the euclidean distance to
            # the goal node
            for node in adjacent_nodes:
                if node not in closed_list:
                    open_list.append((node,
                                      distance(nodes[node], nodes[goal_node])))

            # order the open list by distance
            open_list.sort(key=lambda x: x[1])
            if debug:
                print('Sorted Open List:', open_list)

            # if we find the goal, great
            # if not, the following block is skipped and the algorithm
            # reiterates
            if goal_node == open_list[0][0]:

                # calculate and store the path back to the start
                path_home = [goal_node]
                while path_home[-1] != start_node:
                    if debug:
                        print('Path Home:', path_home)
                    for node in connections[path_home[-1]]:
                        if node in closed_list:
                            path_home.append(node)
                            closed_list.remove(node)
                            break

                # appends the searched path from the start node to the
                # goal node to our final path, but removes the start node,
                # because it's already in the final path, then
                # exits the loop
                for node in path_home[::-1][1:]:
                    final_path.append(node)
                break

    # this converts the path from a list of node labels to a list of
    # node ordinates (x,y)
    final_ordinates = []
    for node_index in final_path:
        final_ordinates.append(nodes[node_index])

    # plot and save the final path as determined by the search
    fig = plt.figure(0)
    fig.set_size_inches(10, 10)
    ax = fig.add_subplot(111)
    ax.plot(*np.array(final_ordinates).T)
    fig.savefig('image/' + image_name + '_path.png')
    fig.clf()

    # we want to return the ordered set of nodes to give to the
    # fourier xform algorithm
    return final_ordinates


if __name__ == '__main__':
    """You can run this script by itself for debugging, though
    this requires running the other functions, too, to produce
    inputs for this one."""
    img_name = 'czechia'
    points = img_to_dots(img_name)
    nodes, connections = node_finder(100, points, img_name)
    ordered_nodes = best_first_search(nodes, connections, img_name)
    spin(len(ordered_nodes), ordered_nodes, img_name)
