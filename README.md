# nodelet
Python library to aid in distributed node operations

## Changes

Added lookup function for nodes supports input types; "x.x.x.x", "c7u4m10", "c7u4"

```python

> from nodelet.utils.lookup_node import lookup_node
> lookup_node("10.15.1.1")

{'c7u4m10': {
       'aisle': 'c', 
       'bmc_addr': '10.0.131.10', 
       'ip_addr': '10.15.1.1',
       'megapod': 10,
       'rack': 7, 
       'slot': 4
       }
}

```

Added by_megapod function which outputs the IP addresses of the mp input.

```python

> from nodelet.utils.list_targets import by_megapod
> by_megapod(0)

['10.10.1.1', '10.10.2.1', '10.10.3.1', '10.10.4.1', 
'10.10.5.1', '10.10.6.1', '10.10.7.1', '10.10.8.1', 
'10.10.9.1', '10.10.10.1', '10.10.11.1', '10.10.12.1', 
'10.10.13.1', '10.10.14.1', '10.10.15.1', '10.10.16.1']

```

## Requirements

### Running from within RA2

- The file `id_rsa_switch` must be present in the users `~/.ssh/` directory, with the correct permissions.

- To setup on the RA2 jumpbox:
```
   virtualenv nodelet_env --python=/usr/bin/python3.6
   source nodelet_env/bin/activate
   python3 -m pip install -r requirements.txt
```

- To execute:
```
   python node-logs.py -n <hostname> 
```
Example:
```
   python node-logs.py -n c1u4m8 
```

### Running outside RA2

- The file `id_rsa_switch` must be present in the users `~/.ssh/` directory, with the correct permissions.
- An `id_rsa` key whose public key is in the Jumpbox's `~/.ssh/authorized_keys` file must be present in the users `~/.ssh/` directory.
- An entry for host `jumpbox-ra` must be included in the users `~/.ssh/config` file.

## Setup

```bash
# Install as python package
$ python3 -m pip install dist/nodelet-0.1.0-py3-none-any.whl

# or install dependencies with
$ python3 -m pip install -r requirements.txt
```



## Basic Usage

Creating the connection

```
with Node(ip_address) as n:
    n.send_command("foo")

# or with

foo = Node(ip_address)
foo.send_command("bar")
foo.close()
```
Utilities
```
with Node(ip_address) as n:
    # Send cmd to node, execute, return result
    n.send_command(cmd)

    # Send a file or directory to the node
    n.send_file(local_path, remote_path)

    # Get a file or directory from the node
    n.get_file(remote_path, local_path)

```

See the examples folder for more!


## Appendix - SSH Config Example

```
Host jumpbox-ra2
	User <your user>
	Port 22
	HostName 192.55.65.201
	IdentityFile ~/.ssh/id_rsa
	ProxyCommand /usr/bin/nc -X 5 -x proxy-us.intel.com:1080 %h %p
```
