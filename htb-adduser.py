#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from __future__ import print_function

import subprocess
import os, sys, errno, uuid
from shutil import copyfile
import getpass

from configuration import *


def print_info(msg):
    print("\x1b[37;3m" + msg + "\x1b[0m")


def print_step(msg):
    print("\x1b[33;3m" + msg + "\x1b[0m")


def execute_command(cmd, input=None):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    p.communicate(input=input)
    ret_code = p.poll()

    if ret_code:
        print("\x1b[91;3m" + "-> ERROR" + str(ret_code) + "\x1b[0m")
        print("\x1b[91;3m An error occurd during the last command! Got error number:" + str(ret_code) + "\x1b[0m")
        exit(-1)


if __name__ == "__main__":

    pyVersion = sys.version_info

    if len(sys.argv) <= 1:
        print("\x1B[91;3m" + "ERROR: YOU HAVE TO DECLARE AN USERNAME!" + "\x1B[0m")
        print_info("\tPlease run \n\t\tsudo ./htb-adduser.py [name of new user] \n\t or \tsudo python2 htb-adduser.py [name of new user]")
        exit(-1)

    execution_path = os.path.realpath(os.path.dirname(sys.argv[0]))
    hostname = os.uname()[1]
    new_username = sys.argv[1]
    user_home_dir = "/u/" + new_username


    if not hostname == "htb-b1":
        print("\x1B[91m" + "ERROR: CAN ONLY BE EXECUTED ON MASTER PC!" + "\x1B[0m")
        print_info("\tPlease change to htb-b1 (Odroid Master)")
        exit(-1)

    print_step("Create new user " + new_username)
    cmd = ['/usr/sbin/adduser', new_username, '--home', user_home_dir, '--disabled-password', '--ingroup', 'htb', '--gecos', '""']

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



    print_step("Setup bash environment")
    copyfile(execution_path + "/templates/htb_ros_env.sh", user_home_dir + "/.htb_ros_env.sh")

    file = open(str(user_home_dir + "/.bashrc"), 'r')
    lines = file.readlines()
    file.close()

    inputStr_exist = False
    for line in lines:
        if line.startswith(str("source ~/.htb_ros_env.sh")):
            inputStr_exist = True

    if not inputStr_exist:
        file = open(str(user_home_dir + "/.bashrc"), 'a')
        file.write("\n source ~/.htb_ros_env.sh")
        file.close()


    print_step("Copying ssh-keys to other pcs")
    tempname = "/tmp/file" + str(uuid.uuid4())  # os.tempnam()
    cmd = ['sudo', '-u', new_username, 'ssh-keygen', '-f', tempname, '-N', '']
    execute_command(cmd)
    try:
        os.makedirs("/u/" + new_username + "/.ssh")
    except OSError as ex:
        if not ex.errno == errno.EEXIST:
            raise
    cmd = ['cp', tempname, user_home_dir + '/.ssh/id_rsa']
    execute_command(cmd)
    cmd = ['cp', tempname + ".pub", user_home_dir + '/.ssh/id_rsa.pub']
    execute_command(cmd)

    key_file = open(user_home_dir + "/.ssh/id_rsa.pub", 'r')
    key_file_lines = key_file.readlines()
    key_file.close()

    auth_keys_file = open(user_home_dir + "/.ssh/authorized_keys", 'a')
    for line in key_file_lines:
        auth_keys_file.write("\n")
        auth_keys_file.write(line)

    auth_keys_file.close()

    print_step("Setup ROS environment")
    if not os.path.exists("/etc/ros/rosdep/"):
        cmd = ['rosdep', 'init', '-r']
        execute_command(cmd)

    cmd = ['sudo', 'su', '-c', 'rosdep update', new_username]
    execute_command(cmd)

    print_step("Create catkin workspace 'catkinws'")
    try:
        os.makedirs(user_home_dir + "/catkinws")
        os.makedirs(user_home_dir + "/catkinws/src")
        execute_command(cmd)
    except OSError as ex:
        if not ex.errno == errno.EEXIST:
            raise

