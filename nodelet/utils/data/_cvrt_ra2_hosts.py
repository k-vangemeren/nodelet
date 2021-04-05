'''

Convert ra2_hosts.yaml into hosts.yaml

Changes -
    - remove anything that isn't a node
    - all hostnames include mp
    - format detailed below...

Nodes: 
- Hostname:
    ip_addr: <ip_addr>
    bmc_addr: <bmc>
    mp: #
    rack: #
    aisle: char
    slot: #
  
'''

from yaml import load, FullLoader, dump

def parse_hostname(hostname):
    name = hostname
    aisle = hostname[0]
    rack = None
    slot = None
    megapod = None

    # aisle a-d,
    # e-f throw away return none    
    if aisle == 'e' or aisle == 'f':
        return None
    else:
        # hostnames ending with l or r are pdus
        # don't want those
        if hostname[-1] == 'l' or hostname[-1] == 'r':
            return None
        else:
            # Get rack number
            hostname = hostname[1:]
            rack = int(hostname[:hostname.find('u')])

            # trim up till after u
            hostname = hostname[hostname.find('u')+1:]

            # We only want the host nodes
            if hostname.find('m') != -1:
                slot = int(hostname[:hostname.find('m')])
                hostname = hostname[hostname.find('m')+1:]
                megapod = int(hostname)
            else:
                return None
    
    return {
        "hostname": name,
        "aisle": aisle,
        "rack": rack,
        "slot": slot,
        "megapod": megapod
    }

def main():
    INPUT_PATH = "ra2_hosts.yaml"
    OUTPUT_PATH = "nodes.yaml"

    with open(INPUT_PATH, "r") as yml_file:
        raw = load(yml_file, Loader=FullLoader)

    # Parse hosts to get rack, aisle, slot, megapod
    hosts = []    
    for host in raw['all']['hosts']:
        out = parse_hostname(host)
        if out != None:
            hosts.append(out)
    
    # Lookup BMC from host and add its IP
    for host in hosts:
        # Get IP addressses
        out = raw['all']['hosts'][host['hostname']]

        host['ip_addr'] = out['ip']

        # Get BMC address
        slot = host['slot']-3
        name = f"{host['aisle']}{host['rack']}u{slot}"

        host["bmc_addr"] = raw['all']['hosts'][name]['ansible_ssh_host']

        print(host)

    output = []
    # Format for output
    for host in hosts:
        output.append({
            host['hostname']:{
                "ip_addr": host['ip_addr'],
                "bmc_addr": host['bmc_addr'],
                "aisle": host['aisle'],
                "rack": host['rack'],
                "slot": host['slot'],
                "megapod": host['megapod']
            }
        })

    with open(OUTPUT_PATH, "w") as yml_file:
        dump(output, yml_file)

if __name__ == "__main__":
    main()
