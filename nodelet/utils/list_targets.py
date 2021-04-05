"""

Utility function to get a list of ip_addresses to connect to
from a various inputs types

See bottom for example usage.

"""

import yaml
import os

def _load_host_map():
    cd = os.path.dirname(os.path.abspath(__file__))
    PATH_TO_HOST_MAP = cd + "/data/nodes.yaml"

    with open(PATH_TO_HOST_MAP, "r") as file:
        host_map = yaml.load(file, Loader=yaml.FullLoader)
    return host_map

def by_megapod(megapod):
    """ Get list of nodes by by MP.
    Args:
        mp (int): The MP whose nodes to list
    Returns:
        nodes (list): List of IP addresses
    """
    host_map = _load_host_map()

    nodes = []

    for host in host_map:
        for node in host:
            if host[node]['megapod'] == megapod:
                nodes.append(host[node]['ip_addr'])
    
    return nodes

if __name__ == "__main__":
    # Tests

    # should print ip_addr for 
    # nodes a1u4 - a3u39
    print(by_megapod(0))