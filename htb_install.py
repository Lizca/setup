# !/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import subprocess
from enum import Enum
from colors import ColorPrinter
import install_steps
import sys



class ActingType(Enum):
    UNDEFINED = 0
    MASTER = 1
    SLAVE = 2
    EXTERN = 4

cp = ColorPrinter()


htb_config = [
    ['htb-b1', '10.0.0.10', ActingType.MASTER, 'Odroid Master'],
    ['htb-n1', '10.0.0.20', ActingType.SLAVE, 'NUC Slave'],
    ['htb-o1', '10.0.0.30', ActingType.SLAVE, 'Ordoid Slave']
]

packages_to_install = [
   # "vim", # editors
   # "zsh", # shells
   # "ipython", "ipython3",
   # "htop", # process viewer
   # "ranger", # file manager
   # "tmux", "terminator", # terminal multiplexer
    "gitg", "openssh-server", "tree", "meld"
]

turtlebot_packages = [
   # "ros-kinetic-turtlebot",
   # "ros-kinetic-turtlebot-apps",
   # "ros-kinetic-turtlebot-interactions",
   # "ros-kinetic-turtlebot-simulator",
   # "ros-kinetic-ar-track-alvar-msgs"
]

def execute_command(cmd, input=None):
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    p.communicate(input=input)
    ret_code = p.poll()

    if ret_code:
        cp.cfg('k', 'r', 'f').out("-> ERROR", ret_code)
        cp.cfg('r', None, 'b').out("An error occurd during the last command! Got error number", ret_code)
        exit(-1)


def print_info(msg):
    print("\x1B[3m"+msg+"\x1B[23m")


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


    fnc_list = []
    installSteps = install_steps.InstallSteps()
    pyVersion = sys.version_info

    cp.cfg('g', None, 'b').out('===================')
    cp.out('= START EXECUTION =')
    cp.out('===================')
    print()

    ###################################
    # CONFIGURATION OF INSTALL SCRIPT #
    ###################################

    while True:
        cp.cfg('y', None, 'ib').out("Configuration")
        cp.out(len("Configuration") * '"')

        cp.cfg('y', None, 'i').out("Choose TurtleBot pc")
        print("Which TurtleBot pc do you want to setup? Choose one of the following numbers.")
        #print("")
        print(" 0:", htb_config[0][0], '('+htb_config[0][3]+")")
        print(" 1:", htb_config[1][0], '('+htb_config[1][3]+")")
        print(" 2:", htb_config[2][0], '('+htb_config[2][3]+")")

        robot = input("->: ")
        print()

        if 0 <= int(robot) <= 2:
            print('You have chosen the pc:', '"' + htb_config[int(robot)][0] + '" (' + htb_config[int(robot)][3] + ")", 'with the IP address:', htb_config[int(robot)][1] + '.')
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
            print("This pc doesn't exist! Try again!")
    print()

    while True:
        while True:
            print()
            cp.cfg('y', None, 'i').out("Choose install step")
            print("Which install step do you want to execute?")
            print("Type the number of step. Type 'a' or press 'Enter' to execute all steps.")
            print("Type q to quit!")

            numFnc = 0
            for fnc_str in [x for x in dir(install_steps.InstallSteps)
                if x.startswith('step_')]:
                    numFnc += 1
                    fnc_list.append(fnc_str)
                    fnc = getattr(install_steps.InstallSteps, fnc_str)
                    print(" " + fnc_str + ":", fnc.__doc__)
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
                    break
                else:
                    print()
                    print("This step doesn't exist! Try again!")
                    continue
            except:
                print()
                print("This step doesn't exist! Try again!")
                continue

        print()
        cp.cfg('k', 'g', 'f').out("-> Configuration Successful")
        print()


        cp.cfg('g', None, 'b').out('=========================')
        cp.out('= STARTING INSTALLATION =')
        cp.out('=========================')
        print()


        if step > 0:
            fnc = getattr(install_steps.InstallSteps, fnc_list[step-1])
            fnc(installSteps)
        else:
            for fnc_str in range(0, len(fnc_list)):
                fnc = getattr(install_steps.InstallSteps, fnc_list[fnc_str])
                fnc(installSteps)

            cp.cfg('g', None, 'b').out('=================================')
            cp.out('= INSTALLATION ENDED SUCCESSFUL =')
            cp.out('=================================')
            print()

            exit()


        cp.cfg('g', None, 'b').out('=================================')
        cp.out('= INSTALLATION ENDED SUCCESSFUL =')
        cp.out('=================================')
        print()

