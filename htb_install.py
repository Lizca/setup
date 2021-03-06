#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from __future__ import print_function

import subprocess
from colors import ColorPrinter
from configuration import *
import install_steps
import sys, getpass, os


cp = ColorPrinter()

def execute_command(cmd, input=None):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    p.communicate(input=input)
    ret_code = p.poll()

    if ret_code:
        cp.cfg('k', 'r', 'f').out("-> ERROR", ret_code)
        cp.cfg('r', None, 'b').out("An error occurd during the last command! Got error number:", ret_code)
        exit(-1)


def print_info(msg):
    cp.cfg('w', None, 'i').out(msg)


def print_step(msg):
    cp.cfg('y', None, 'ib').out(msg)
    cp.out(len(msg) * '"')


def print_subStep(msg):
    cp.cfg('y', None, 'i').out(msg)


def print_section(msg):
    cp.cfg('b', None, 'b').out((len(msg)+4) *'=')
    cp.out('= ' + msg + ' =')
    cp.cfg('b', None, 'b').out((len(msg)+4) *'=')


def print_success():
    cp.cfg('g', None, 'bu').out("-> Successful")
    print()


def rewrite_file(fileStr, searchStr, inputStr):
    file = open(str(fileStr), 'r')
    lines = file.readlines()
    file.close()

    file = open(str(fileStr), 'w')
    inputStr_exist = False
    for line in lines:
        if line.startswith(str(searchStr)):
            inputStr_exist = True
            file.write(str(inputStr))
        else:
            file.write(line)
    if not inputStr_exist:
        file.write(str(inputStr))


if __name__ == "__main__":

    # check if user has executed with sudo
    if not getpass.getuser() == "root":
        print("\x1B[91;3m" + "ERROR: YOU HAVE TO EXECUTE THIS INSTALL SCRIPT WITH SUDO RIGHTS!" + "\x1B[0m")
        print_info("\tPlease run \n\t\tsudo ./htb_install.py \n\t or \tsudo python2 htb_install.py")
        exit(-1)

    fnc_list, ext_fnc_list = [], []
    installSteps = install_steps.InstallSteps()
    pyVersion = sys.version_info
    installSteps.execution_path = os.path.realpath(os.path.dirname(sys.argv[0]))

    # Get all existing install step functions
    numFnc = 0
    for fnc_str in [x for x in dir(install_steps.InstallSteps) if x.startswith('step_')]:
        fnc_list.append(fnc_str)
        numFnc += 1

    # Get the existing install step functions for external pc
    for fnc_num in external_install_steps:
        if fnc_num <= 9:
            fnc_str = 'step_0' + str(fnc_num)
        else:
            fnc_str = 'step_' + str(fnc_num)
        ext_fnc_list.append(fnc_str)



    print_section("START EXECUTION")
    print()

    ###################################
    # CONFIGURATION OF INSTALL SCRIPT #
    ###################################

    while True:
        print_step("Configuration")

        print_subStep("Choose TurtleBot pc")
        print("Which TurtleBot pc do you want to setup? Choose one of the following numbers.")
        print(" 0:", htb_config[0][0], '('+htb_config[0][3]+")")
        print(" 1:", htb_config[1][0], '('+htb_config[1][3]+")")
        print(" 2:", htb_config[2][0], '('+htb_config[2][3]+")")
        print(" 3:", "external pc")

        robot = input("->: ")
        print()

        if MASTER <= int(robot) <= EXTERN:
            if int(robot) <= SLAVE:
                print('You have chosen the pc:', '"' + htb_config[int(robot)][0] + '" (' + htb_config[int(robot)][3] + ")", 'with the IP address:', htb_config[int(robot)][1] + '.')
            else:
                print('You have chosen the external pc.')

            print("Is this correct?")

            if pyVersion[0] == 2 and pyVersion[1] >= 5:
                userInput = raw_input("type 'Y' or 'n': ") # python 2
            elif pyVersion[0] >= 3 :
                userInput = input("type 'Y' or 'n': ") # python 3
            else:
                print("The currenty used python version is not compatible. Please use Python 2.5 or higher.")
                exit(-1)

            if userInput == "" or userInput == 'Y' or userInput == 'y':
                installSteps.robot = robot
                installSteps.actingType = htb_config[int(robot)][2]
                installSteps.robotIp = htb_config[int(robot)][1]
                break
            else:
                print()
                continue
        else:
            print("This pc doesn't exist! Please try again!")
    print()

    while True:
        while True:
            print()
            print_subStep("Choose install step")
            print("Which install step do you want to execute?")
            print("Type the number of step. Type 'a' or press 'Enter' to execute all steps.")
            print("Type q to quit!")

            if int(robot) <= SLAVE:
                for fnc_str in fnc_list:
                    fnc = getattr(install_steps.InstallSteps, fnc_str)
                    print(" ", fnc_str + ":", fnc.__doc__)
            else:
                for fnc_str in ext_fnc_list:
                    fnc = getattr(install_steps.InstallSteps, fnc_str)
                    print(" ", fnc_str + ":", fnc.__doc__)

            print("       a: Execute all steps")
            print("       q: Quit")

            if pyVersion[0] == 2 and pyVersion[1] >= 5:
                step = raw_input("-> : ")  # python 2
            elif pyVersion[0] >= 3:
                step = input("-> : ")  # python 3
            else:
                print("The currenty used python version is not compatible. Please use Python 2.5 or higher.")
                exit(-1)

            if step == 'q':
                exit()

            try:
                if step == 'a' or step == "":
                    step = 0
                    break
                elif 1 <= int(step) <= (numFnc+1):
                    step = int(step)
                    if int(robot) == EXTERN and step not in external_install_steps:
                        raise RuntimeError
                    break
                else:
                    raise RuntimeError
            except:
                print()
                print("This step doesn't exist! Please try again!")
                continue

        print()
        print_success()


        print_section('STARTING INSTALLATION')
        print()

        if step > 0:
            fnc = getattr(install_steps.InstallSteps, fnc_list[step-1])
            fnc(installSteps)
        else:
            if int(robot) <= SLAVE:
                for fnc_num in range(0, len(fnc_list)):
                    fnc = getattr(install_steps.InstallSteps, fnc_list[fnc_num])
                    fnc(installSteps)
            else:
                for fnc_num in range(0, len(ext_fnc_list)):
                    fnc = getattr(install_steps.InstallSteps, ext_fnc_list[fnc_num])
                    fnc(installSteps)


            print_section('INSTALLATION ENDED SUCCESSFULLLY')
            print()

            print_section('INSTALLATION ENDED SUCCESSFULLY')
            print()

            print("     \x1B[91;3m#\x1B[0m      | ")
            print("    \x1B[91;3m# #\x1B[0m     | ")
            print("   \x1B[91;3m#\x1B[0m | \x1B[91;3m#\x1B[0m    |  Please reboot now!  ")
            print("  \x1B[91;3m#\x1B[0m  .  \x1B[91;3m#\x1B[0m   | ")
            print(" \x1B[91;3m#########\x1B[0m  | ")
            print()

            exit()

