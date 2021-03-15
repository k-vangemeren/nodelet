#!/usr/bin/env python3

"""
Node abstracts of the connection to a node and provides the
following some basic utilities once connected

Usage:

foo = Node(ip_address)
foo.send_command("foo")
foo.close()

            OR

with Node(ip_address) as n:
    n.send_command("foo")

"""

import os
import sys
import time

import paramiko
import scp

class Node:
    def __init__(self, IP, jumpbox=False):
        self.KEY_FILE = os.getenv('HOME')+'/.ssh/id_rsa'
        self.PATH_SSH_CONFIG = os.getenv('HOME')+"/.ssh/config"
        self.PATH_ID_RSA_SWITCH = os.getenv('HOME')+"/.ssh/id_rsa_switch"
        self.JBOX_PRIVATE = "10.18.1.1"

        self._get_config()
        self._connect(IP)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def progress(self, filename, size, sent):
        sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

    @property
    def connection(self):
        return self._conn

    def close(self):
        self._conn.close
        self.jbox.close

    def _get_config(self):
        config = paramiko.SSHConfig()
        config.parse(open(self.PATH_SSH_CONFIG))
        self.conf = config.lookup("jumpbox-ra2")

    def _open_channel(self, target_ip):
        self.jbox = paramiko.SSHClient()
        self.jbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.jbox.connect(
            self.conf.get('hostname'),
            username=self.conf.get('user'),
            key_filename=self.KEY_FILE,
            sock=paramiko.ProxyCommand(self.conf.get('proxycommand'))
        )
        jbox_transport = self.jbox.get_transport()
        
        src = (self.JBOX_PRIVATE, self.conf.as_int('port'))
        dst = (target_ip, self.conf.as_int('port'))
        chnl = jbox_transport.open_channel("direct-tcpip", dst, src)
        return chnl

    def _connect(self, target_ip):
        self._conn = paramiko.SSHClient()
        self._conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._conn.connect(
            target_ip,
            username='ubuntu',
            key_filename=self.PATH_ID_RSA_SWITCH,
            sock=self._open_channel(target_ip)
        )

    def send_command(self, cmd, cmd_timeout=None, splitlines=0):
        """Send command to node and return the result.
    
        Required:
            cmd (str) - command for the node to execute.
    
        Optional:
            timeout (int) - forces the channel closed after n seconds
            splitlines (bool) - split the lines of the nodes response
                                (default) False

        Returns:
            utf-8 decoded node response.
        """

        s_time = time.time()
        _stdin, stdout, _stderr = self._conn.exec_command(
            cmd, get_pty=True
        )

        if cmd_timeout is not None:
            while not stdout.channel.exit_status_ready():
                e_time = time.time() - s_time
                if e_time >= cmd_timeout:
                    stdout.channel.close()
                    print("Closed Channel")
                    break

        if splitlines:
            return stdout.read().decode("utf-8").splitlines()
        else:
            return stdout.read().decode("utf-8")

    def send_file(self, local_path, dest_path):
        """Send local file (or directory) to the node.

        Required:
            local_path (str) - absolute path or relative to the working directory
            dest_path (str) - absolute remote path
        """

        _scp = scp.SCPClient(self._conn.get_transport())
        _scp.put(
            local_path,
            recursive=True,
            remote_path=dest_path
        )
        _scp.close()
    
    def get_file(self, remote_path, local_path):
        """Get file (or directory) at remote_path and save to local_path

        Required:
            remote_path (str) - absolute remote path
            local_path (str) - absolute local path or relative to the working directory
        """
        _scp = scp.SCPClient(self._conn.get_transport())
        _scp.get(
            remote_path,
            local_path, 
            recursive=True
        )
        _scp.close()


if __name__ == "__main__":

    # Test...should respond with the hostname a0u4m0
    # VPN on...
    with Node("10.10.1.1") as conn:
        print("Test: send_command")
        print(conn.send_command("hostname"))