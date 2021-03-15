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

def main(ips, password):
    with open("passwrd", "w+") as tmpFile:
        tmpFile.write(password)
    
    counter = 0
    total = len(ips)-1

    for ip in ips:
        try:
            # Set flag to False if executing from the jumpbox
            with node.Node(ip, jumpbox=True) as target:
                target.send_file("passwrd", "~/")
                target.send_command("cat ~/passwrd | docker login --username kvangemeren --password-stdin")
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
            "-p", dest="password", required=True
        )
        args = parser.parse_args()

        # pass parse list of IPs to main
        main(get_targets(args.filepath), args.password)