"""

Utility function for host lookup

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

def lookup_node(address):
    """ Lookup info for address info. Accepts strings of forms
        'x.x.x.x', 'a1u18', 'a1u18m0'. 
    Args:
        address (str): address of host (hostname or ip)
    Returns:
        node_info (dict): info for address, or None if not found
    """
    host_map = _load_host_map()

    # Case searching by IP
    if address[0].isdigit():
        for host in host_map:
            for node in host:
                if host[node]['ip_addr'] == address:
                    return host
    
    # Case searching by hostname_w/_MP
    elif address.find('m') != -1:
        for host in host_map:
            for node in host:
                if node == address:
                    return host

    # Case searching by hostname_w/o_MP
    else:
        for host in host_map:
            for node in host:
                if node[:node.find('m')] == address:
                    return host

    # No match found
    return None

if __name__ == "__main__":
    
    # TESTS should all return
    # {'c7u4m10': {
    #   'aisle': 'c', 
    #   'bmc_addr': '10.0.131.10', 
    #   'ip_addr': '10.15.1.1',
    #   'megapod': 10,
    #   'rack': 7, 
    #   'slot': 4
    #   }
    # }
    
    # Test ip lookup
    print(lookup_node("10.15.1.1"))

    # Test hostname w/ mp lookup
    print(lookup_node("c7u4m10"))

    # Test hostname w/o mp lookup
    print(lookup_node("c7u4"))