# nodelet
Python library to aid in distributed node operations

## To-Do

- Cleanup
- Usage documentation
- Examples folder

## Requirements

### Running from within RA2

- The file `id_rsa_switch` must be present in the users `~/.ssh/` directory, with the correct permissions.

### Running outside RA2

- The file `id_rsa_switch` must be present in the users `~/.ssh/` directory, with the correct permissions.
- An `id_rsa` key whose public key is in the Jumpbox's `~/.ssh/authorized_keys` file must be present in the users `~/.ssh/` directory.
- An entry for host `jumpbox-ra` must be included in the users `~/.ssh/config` file.

