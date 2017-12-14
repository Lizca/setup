#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from __future__ import print_function

import subprocess
from colors import ColorPrinter
from configuration import *
import os, sys, errno, uuid
import getpass


def print_info(msg):
    cp.cfg('w', None, 'i').out(msg)


def print_step(msg):
    cp.cfg('y', None, 'i').out(msg)


def execute_command(cmd, input=None):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    p.communicate(input=input)
    ret_code = p.poll()

    if ret_code:
        cp.cfg('k', 'r', 'f').out("-> ERROR", ret_code)
        cp.cfg('r', None, 'b').out("An error occurd during the last command! Got error number:", ret_code)
        exit(-1)


if __name__ == "__main__":

    cp = ColorPrinter()
    pyVersion = sys.version_info

    if len(sys.argv) <= 1:
        print("\x1B[91;3m" + "ERROR: YOU HAVE TO DECLARE AN USERNAME!" + "\x1B[0m")
        print_info("\tPlease run \n\t\tsudo ./htb-adduser.py [name of new user] \n\t or \tsudo python2 htb-adduser.py [name of new user]")
        exit(-1)

    hostname = os.uname()[1]
    new_username = sys.argv[1]

    if not hostname == "htb-b1":
        print("\x1B[91m" + "ERROR: CAN ONLY BE EXECUTED ON MASTER PC!" + "\x1B[0m")
        print_info("\tPlease change to htb-b1 (Odroid Master)")
        exit(-1)

    print_step("Create new user " + new_username)
    cmd = ['/usr/sbin/adduser', new_username, '--home', '/home/'+new_username, '--disabled-password', '--ingroup', 'htb', '--gecos', '""']

    execute_command(cmd)

    passwd = getpass.getpass("Enter Password: ")
    print(passwd)

    print_step("Set account password")
    cmd = ['chpasswd']
    input = str(new_username) + ':' + str(passwd) + '\n'
    if pyVersion[0] >= 3:
        execute_command(cmd, input=bytes(input, 'UTF-8'))
    elif pyVersion[0] == 2:
        execute_command(cmd, input=bytes(input))


    print_step("Add new user to groups")
    cmd = ['usermod', '-aG', 'dialout,cdrom,audio,video,plugdev', new_username]
    execute_command(cmd)


    print_step("Syncing passwd file to other htb-pcs")
    for r in range(1, len(htb_config) - 1):  # don't use the external pc
        cmd = ['rsync', '-e', 'ssh',  '-avz', '/etc/passwd', '/etc/shadow', '/etc/group', 'robot-local@' + htb_config[r][1] + ':/etc/']
        execute_command(cmd)
        cmd = ['ping', '-c2', htb_config[r][1]]
        execute_command(cmd)


    print_step("Setup bash and zsh environment")
    print("todo...")


    print_step("Copying ssh-keys to other pcs") #, please enter password of new user")
    print("todo...")

    tempname = "/tmp/file" + str(uuid.uuid4())  # os.tempnam()
    cmd = ['ssh-keygen', '-f', tempname, '-N', '']
    execute_command(cmd)
    try:
        os.makedirs("/home/robot-local/.ssh")
    except OSError as ex:
        if not ex.errno == errno.EEXIST:
            raise
    cmd = ['cp', tempname, '/home/robot-local/.ssh/id_rsa']
    execute_command(cmd)
    cmd = ['cp', tempname + ".pub", '/home/robot-local/.ssh/id_rsa.pub']
    execute_command(cmd)

    # cat ~/.ssh/id_rsa.pub >> ~ /.ssh / authorized_keys
    # cmd = ['ssh-copy-id', htb_config[int(self.robot)][0]]
    # execute_command(cmd)



    print_step("Setup ROS environment")
    if not os.path.exists("/etc/ros/rosdep/"):
        cmd = ['rosdep', 'init', '-r']
        execute_command(cmd)

    cmd = ['sudo', 'su', '-c', 'rosdep update', new_username]
    execute_command(cmd)

    try:
        os.makedirs("/u/" + new_username + "/catkinws")
    except OSError as ex:
        if not ex.errno == errno.EEXIST:
            raise

