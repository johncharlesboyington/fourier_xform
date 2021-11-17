from img_to_dots import img_to_dots
from node_finder import node_finder
from spin import spin
from best_first_search import best_first_search


def fxform(img_name, N=100, debug=False):
    """Produces a fourier approximation of a particular image. img_name
    is the filename (sans path, sans extension) that the user has placed
    in the local 'image/' folder. This image must be a .jpg or a .png.
    N is the order of the approximation. The argument for debugging output
    is included but not currently implemented."""
    points = img_to_dots(img_name)
    nodes, connections = node_finder(N, points, img_name)
    ordered_nodes = best_first_search(nodes, connections, img_name)
    spin(len(ordered_nodes), ordered_nodes, img_name)
    return
