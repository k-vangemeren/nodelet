# nodelet
Python library to aid in distributed node operations

## Requirements

### Running from within RA2

- The file `id_rsa_switch` must be present in the users `~/.ssh/` directory, with the correct permissions.

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


## To-Do

- Cleanup
- Usage documentation
- Examples folder

## Appendix - SSH Config Example

```
Host jumpbox-ra2
	User <your user>
	Port 22
	HostName 192.55.65.201
	IdentityFile ~/.ssh/id_rsa
	ProxyCommand /usr/bin/nc -X 5 -x proxy-us.intel.com:1080 %h %p
```