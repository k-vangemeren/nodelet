from nodelet.Node import Node

test_ip = "10.16.12.1" # Magic IP address

if __name__ == '__main__':
    with Node(test_ip) as node:
        print(node.send_command("hostname"))