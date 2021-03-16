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

# HELPERS -----

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

def main(ips, logpath, save_log):
    counter = 0
    total = len(ips)

    # For each input IP
    for ip in ips:
        try:
            # Create node
            host = node.Node(ip)

            # Get device info
            devices = get_device_info(host)

            # Check for number of detected devices
            if len(devices) != 4:
                print(f"{ip}: {len(devices)}/4 Gaudi detected")

            # for each device reported
            for device in devices:
                # Get local rank by passing pci bus_id
                rank = get_local_rank(host, device[2])

                # Check if the device at that rank has had any failures
                failures = check_for_error_rank(host, logpath, rank)
                
                # Append results to devices
                device.append(int(failures))

            if save_log:
                # Create log folder if it doesn't exist
                if not os.path.exists('logs'):
                    os.makedirs('logs')
                
                # download file
                host.get_file(logpath, f"logs/{ip}.log")

            # Close connection
            host.close()

            # Print results
            counter +=1 
            print(f"{counter}/{total}: {ip} - Pass") 
            print(f"{ip}: Results --")
            for result in devices:
                print(f"{result}")

        except Exception as e:
            print(f"{counter}/{total}: {ip} - Fail")
            print(e)

        except KeyboardInterrupt:
            break


if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-f", dest="filepath", required=True
        )
        parser.add_argument(
            "-l", dest="logpath", required=True
        )
        parser.add_argument(
            "-d", dest="save_log", action="store_true"
        )
        args = parser.parse_args()

        main(get_targets(args.filepath), args.logpath, args.save_log)