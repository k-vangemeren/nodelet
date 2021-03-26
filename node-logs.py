#!/bin/env python3
'''
Parse logfile at location for dma errors

Usage:
$ python3 dma-logs.py -f barcelona-targets/<mp#> -l <location-of-log> [Optional -d ]

Example:
# Search for errors in syslog across mp10. Don't save the log
$ python3 dma-logs.py -f barcelona-targets/mp10 -l /var/log/syslog

# Same. But this time save the logs
$ python3 dma-logs.py -f barcelona-targets/mp10 -l /var/log/syslog -d

'''

from nodelet import node
import argparse
import re
import os
import sys
import yaml
# HELPERS -----

def get_hlsip(hostName):
    rackUName = hostName.split('m')[0]
    rackName = rackUName.split('u')[0]
    rackNum = rackUName.split('u')[1]
    #Subr 3 to get the HLS U num
    rackNumInt = list(map(int, rackNum))
    rackNumInt[:] = [number - 3 for number in rackNumInt]
    rackNumStr = list(map(str, rackNumInt))
    hlsname=rackName+'u'+rackNumStr[0]
    return hlsname

# Get ips per file
def get_targets(target_file):
    ips = []
    with open(target_file, "r") as f:
        for line in f:
            ips.append(line.strip())
    return ips

# Get serial number, driver_version, and pci bus_id
def get_device_info(node):
    out = []
    resp = node.send_command("hl-smi -f csv,noheader -Q serial,driver_version,bus_id", splitlines=1)
    for line in resp:
        line = line.split(', ')
        line[0] = line[0][5:]
        line[2] = line[2][:-3]
        out.append(line)
    return out

# check `location` for errors by module
def check_for_error_rank(node, location, rank):
    resp = node.send_command(f"grep 'hl{rank}' {location} | grep 'SERR=1' | wc -l")
    return int(resp)

# with bus_id get AIP number of the device
def get_local_rank(node, bus_id):
    resp = node.send_command(f"hl-smi -q | grep -iE 'Serial Number|AIP \(hl|Module ID' | grep {bus_id}")
    regex = re.compile(r"AIP \(hl(.+?)\)")
    match = regex.search(resp)
    return match.group(1)

# MAIN ----

def main(ip, logpath, save_log=True):
    counter = 0
    total = len(ip)
    print(logpath)
    try:
        with open("nodelet/targets/ra2_hosts.yaml", 'r') as stream:
          try:
            ra2_hls = (yaml.safe_load(stream))
          except yaml.YAMLError as exc:
            print(exc)

        hls_name = get_hlsip(ip) 
        hls_ip = ra2_hls['all']['hosts'][hls_name]['ansible_ssh_host'] 
        print ("hls: "hls_name+": "+hls_ip)
        # Create node
        host = node.Node(ip, 'ubuntu')
        hls = node.Node(hls_ip, 'root')

        if save_log:
            # Create log folder if it doesn't exist
            if not os.path.exists(os.path.join(logpath,ip)):
                os.makedirs(str(os.path.join(logpath,ip, "server")))
                os.makedirs(str(os.path.join(logpath,ip, "hls")))
            
            # download files
            host.get_file('/var/log/syslog', f"{logpath}/{ip}/server/{ip}.log")
            hls.get_file('/var/run/log/journal', f"{logpath}/{ip}/hls/")
            print("Saved files at "+logpath)

        # Close connection
        host.close()
        hls.close()

    except Exception as e:
        print(e)

    #except KeyboardInterrupt:
    #    break


if __name__ == "__main__":
        sys.path.append(r'/bin')
        parser = argparse.ArgumentParser()
#       parser.add_argument(
#            "-f", dest="filepath", required=False, help='User specified file or dir path to copy'
#        )
        parser.add_argument(
            "-n", dest="nodename", required=True
        )
        parser.add_argument(
            "-l", dest="logpath", required=False, default='/mnt/weka/weka-csi/aramacha/logs/'
        )
        args = parser.parse_args()

        main(args.nodename, args.logpath)
