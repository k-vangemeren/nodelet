'''
Perform docker-login on a megapod

Usage:
$ python3 docker-login.py -f barcelona-targets/<mp#> -u <username> -p <password>

'''

from nodelet import node

import argparse
import os

# Get ips per file
def get_targets(target_file):
    ips = []
    with open(target_file, "r") as f:
        for line in f:
            ips.append(line.strip())
    return ips

def main(ips, username, password):
    with open("passwrd", "w+") as tmpFile:
        tmpFile.write(password)
    
    counter = 0
    total = len(ips)

    for ip in ips:
        try:
            # Set flag to True if executing from your laptop
            # Setup required see README
            with node.Node(ip) as target:
                target.send_file("passwrd", "~/")
                target.send_command(f"cat ~/passwrd | docker login --username {username}--password-stdin")
                target.send_command("rm ~/passwrd")
                counter+=1

            print(f"{counter}/{total}: {ip} - Done")
        except Exception:
            print(f"{counter}/{total}: {ip} - Fail")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-f", dest="filepath", required=True
        )
        parser.add_argument(
            "-u", dest="username", required=True
        )
        parser.add_argument(
            "-p", dest="password", required=True
        )
        args = parser.parse_args()

        # pass parse list of IPs to main
        main(get_targets(args.filepath), args.username, args.password)