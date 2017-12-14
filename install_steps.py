
from __future__ import print_function
from htb_install import *
from configuration import *
from colors import ColorPrinter
import os, errno
from shutil import copyfile


class InstallSteps:

    robot = None
    actingType = UNDEFINED
    robotIP = None

    cp = ColorPrinter()

    def step_01(self):
        """Setup language and time settings"""
        print_step("Step 1: " + str(self.step_01.__doc__))

        print_subStep("Set system language and keyboard layout")
        cmd = ['cp', 'templates/locale', '/etc/default/locale']
        execute_command(cmd)
        cmd = ['cp', 'templates/keyboard', '/etc/default/keyboard']
        execute_command(cmd)
        print_info("Your language has been set to 'LANG=de_DE.UTF-8' and keyboard layout to 'KEYMAP=de-latin1-nodeadkeys'")

        print_subStep("Set time zone")
        try:
            cmd = ['unlink', '/etc/localtime']
            execute_command(cmd)
        except:
            pass
        cmd = ['ln', '-s', '/usr/share/zoneinfo/Europe/Berlin', '/etc/localtime']
        execute_command(cmd)
        print_info("Your timezone has been set to Europe/Berlin")

        print_subStep("Set hardware clock")
        cmd = ['timedatectl', 'set-local-rtc', '0']
        execute_command(cmd)
        execute_command(['date'])

        print_subStep("Generate locales")
        cmd = ['cp', 'templates/locale.gen', '/etc/locale.gen']
        execute_command(cmd)
        cmd = (["locale-gen"])
        execute_command(cmd)

        print_success()


    def step_02(self):
        """Set hostname"""
        print_step("Step 2: " + str(self.step_02.__doc__))

        cmd = ['hostnamectl', 'set-hostname', htb_config[int(self.robot)]][0]
        execute_command(cmd)
        print_info("The hostname has been set to " + htb_config[int(self.robot)][0] + ' ('+htb_config[int(self.robot)][3]+')')

        print_success()


    def step_03(self):
        """Setup user account robot-local"""
        print_step("Step 3: " + str(self.step_03.__doc__))

        print_subStep("Check if the user robot-local exists")
        if 'robot-local' in open('/etc/passwd').read():
            self.cp.cfg('k', 'g', 'f').out("-> Found!")
        else:
            self.cp.cfg('k', 'y', 'bf').out("-> No user 'robot-local' found!")
            self.cp.cfg('y', None, 'i').out("Create new user 'robot-local'")
            cmd = ['adduser', '--disabled-password', '--gecos', '""', 'robot-local', '--home', '/home/robot-local']
            execute_command(cmd)

        print_subStep("Add user to groups")
        cmd = ['adduser', 'robot-local', 'sudo']
        execute_command(cmd)

        print_subStep("Set account password")
        cmd = ['chpasswd', '-e']
        execute_command(cmd, input=b'robot-local:$6$q4PV2O6Zww/wqTzx$v4Fg21NOOovlSkkhIx/sRLGJSvt9FhSkUjNAkfW6OtenDp/DdI4EAHhLT.1KXhB6SNWL0xTgIx7ECXW60Yjzv1\n')

        print_success()


    def step_04(self):
        """Setup network connection"""
        print_step("Step 4: " + str(self.step_04.__doc__))

        networks = os.listdir('/sys/class/net')
        for n in networks:
            if n.startswith("eth") or n.startswith("enp"):
                network = n
                break

        print_subStep("Create file /etc/network/interfaces")

        tempfile = open("templates/interfaces")
        interfaces = open("/etc/network/interfaces", 'w+')
        for line in tempfile:
            if line.startswith("auto $(iface)"):
                interfaces.write("auto " + network + '\n')
            elif line.startswith("iface $(iface)"):
                interfaces.write("iface " + network + ' inet static\n')
            elif line.startswith("address $(ip_address)"):
                interfaces.write("address " + htb_config[int(self.robot)][1] + '\n')
            else:
                interfaces.write(str(line))
        tempfile.close()
        interfaces.close()

        print_subStep("Start ethernet connection")
        cmd = ['ifdown', network]
        execute_command(cmd)
        cmd = ['ifup', '-v', network]
        execute_command(cmd)

        print_subStep("Test connection")
        cmd = ['ping', '-c2', 'www.google.com']
        execute_command(cmd)

        print_success()


    def step_05(self):
        """Add htb-packages to APT-Sources"""
        print_step("Step 5: " + str(self.step_05.__doc__))

        print_subStep("Install depended Package")
        cmd = ['apt-get', 'install', 'apt-transport-https', '-y']
        execute_command(cmd)

        print_subStep("Add htb-repository to APT-Sources")
        cmd = ['sh', '-c',
               'echo "deb https://raw.githubusercontent.com/hhntb/htb_aptrepo/master $(lsb_release -sc) main" > /etc/apt/sources.list.d/github-htb-aptrepo.list']
        execute_command(cmd)
        print_info("https://raw.githubusercontent.com/hhntb/htb_aptrepo/master")

        print_subStep("Update APT-Sources")
        cmd = ['apt-get', 'update', '-y']
        execute_command(cmd)

        print_success()


    def step_06(self):
        """Upgrade System"""
        print_step("Step 6: " + str(self.step_06.__doc__))

        cmd = ['apt-get', 'update', '-y']
        execute_command(cmd)
        cmd = ['apt-get', 'upgrade', '-y']
        execute_command(cmd)

        print_success()


    def step_07(self):
        """Install base packages"""
        print_step("Step 7: " + str(self.step_07.__doc__))

        for p in packages_to_install:
            cmd = ["apt-get", "install", "-y"]
            cmd.extend(p)
            execute_command(cmd)

        print_success()


    def step_08(self):
        """Setup additional system configuration"""
        print_step("Step 8: " + str(self.step_08.__doc__))

        '''
            print_subStep("Allow shutdown when powerbutton has been pressed")
            cmd = ['cp', 'templates/powerbtn.sh', '/etc/acpi/powerbtn.sh']
            print_info("Edit file /etc/acpi/powerbtn.sh")
            execute_command(cmd)
        '''

        print_subStep("Let ssh server send alive signal")
        rewrite_file("/etc/ssh/sshd_config", "ClientAliveInterval", "ClientAliveInterval 60\n")
        print_info("Edit file /etc/ssh/sshd_config")

        print_subStep("Disable root account")
        cmd = ['chpasswd', '-e']
        execute_command(cmd, input=b'root:!\n')
        print_info("Root account is now no longer usable")

        print_subStep("Create new group htb")
        groups = open("/etc/group", 'r')
        group_exist = False
        for line in groups:
            if line.startswith("htb:"):
                group_exist = True
                print_info("Group htb already exist.")
                break
        if not group_exist:
            cmd = ['groupadd', 'htb']
            execute_command(cmd)
            print_info("Add group htb")
        groups.close()

        print_subStep("Add name resolution to /etc/hosts")
        for r in range(0, len(htb_config)-1): # don't add the external pc
            if not r == int(self.robot):
                file = open("/etc/hosts", 'r')
                lines = file.readlines()
                file.close()

                host_exist, ip_correct = False, False
                for line in lines:
                    if htb_config[r][0] in line:
                        host_exist = True

                        if line.startswith(htb_config[r][1]):
                            ip_correct = True

                        break

                if not host_exist:
                    file = open("/etc/hosts", 'a')
                    file.write(htb_config[r][1] + " " + htb_config[r][0] + '\n')
                    file.close()

                elif host_exist and not ip_correct:
                    file = open("/etc/hosts", 'w')
                    file.write("\n" + htb_config[r][1] + " " + htb_config[r][0] + '\n')
                    for line in lines:
                        file.write(line)

                    file.close()

        print_success()


    def step_09(self):
        """Setup NFS"""
        print_step("Step 9: " + str(self.step_09.__doc__))

        print_subStep("Install needed packages")
        cmd = ['apt-get', 'install', 'nfs-kernel-server', '-y']
        execute_command(cmd)

        print_subStep("Create directory '/u'")
        try:
            os.makedirs("/ u")
        except OSError as ex:
            #print_info("Directory already exist.")
            if not ex.errno == errno.EEXIST:
                raise

        print_subStep("Activate STATD")
        rewrite_file("/etc/default/nfs-common", "NEED_STATD", "NEED_STATD=yes\n")

        if self.actingType == MASTER:
            print_subStep("Editing '/etc/fstab'")
            rewrite_file("/etc/fstab", "[uuid]", "[uuid] /u ext4 rw,suid,dev,auto,nouser,sync,noatime,nofail 0 0\n")

            print_subStep("Mount external device")
            cmd = ['mount', '/u']
            execute_command(cmd)
            print_subStep("Edit /etc/exports")
            rewrite_file("/etc/exports", "/u", "/u *(rw,fsid=0,sync,no_subtree_check)\n")

        elif self.actingType == SLAVE:
            print_subStep("Install needed packages")
            cmd = ['apt-get', 'install', 'autofs', '-y']
            execute_command(cmd)

            print_subStep("Edit /etc/auto.master")
            rewrite_file("/etc/auto.master", "/-", "/- /etc/auto.direct\n")

            print_subStep("Create /etc/auto.direct")
            file = open("/etc/auto.direct", 'w+')
            file.write("/u -fstype=nfs4 " + htb_config[0][1] + ":/\n")

            print_subStep("Activate NFS")
            cmd = ['update-rc.d', 'autofs', 'defaults']
            execute_command(cmd)
            cmd = ['service', 'autofs', 'restart']
            execute_command(cmd)
            cmd = ['modprobe', 'nfs']
            execute_command(cmd)

        print_subStep("Reload /etc/fstab")
        cmd = ['systemctl', 'daemon-reload']
        execute_command(cmd)

        print_success()


    def step_10(self):
        """Setup NTP"""
        print_step("Step 10: " + str(self.step_10.__doc__))

        print_subStep("Install needed package")
        cmd = ['apt-get', 'install', 'ntp', '-y']
        execute_command(cmd)
        print_subStep("Edit /etc/ntp.conf")
        if self.actingType == MASTER:
            rewrite_file("/etc/ntp.conf", "pool 0.ubuntu", "server 0.pool.ntp.org\n")
            rewrite_file("/etc/ntp.conf", "restrict " + htb_config[0][1], "restrict " + htb_config[0][1] + " mask 255.255.255.0 nomodify notrap\n")
        elif self.actingType == SLAVE:
            rewrite_file("/etc/ntp.conf", "pool 0.ubuntu", "server " + htb_config[0][1] + "\n")

        print_success()


    def step_11(self):
        """Install ROS"""
        print_step("Step 11: " + str(self.step_11.__doc__))

        print_subStep("Setup source.list and keys")
        cmd = ['sh', '-c',
               'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list']
        execute_command(cmd)
        cmd = ['apt-key', 'adv', '--keyserver', 'hkp://ha.pool.sks-keyservers.net:80', '--recv-key',
               '421C365BD9FF1F717815A3895523BAEEB01FA116']
        execute_command(cmd)

        print_subStep("Update ATP-sources")
        cmd = ['apt-get', 'update', '-y']
        execute_command(cmd)

        print_subStep("Install ROS packages")
        if self.actingType <= SLAVE:
            execute_command(['apt-get', 'install', 'ros-kinetic-ros-base', '-y'])
        else:
            execute_command(['apt-get', 'install', 'ros-kinetic-desktop-full', '-y'])

        print_subStep("Install ros-turtlebot packages")
        for p in turtlebot_packages:
            execute_command(['apt-get', 'install', '-y', p])

        if self.actingType == EXTERN:
            self.cp.cfg('y', None, 'i').out("Setup rosdep")

            if not os.path.exists("/etc/ros/rosdep/"):
                cmd = ['rosdep', 'init', '-r']
                execute_command(cmd)

            user_name = os.environ.get('SUDO_USER')
            if not user_name:
                user_name = os.environ.get('LOGNAME')

            cmd = ['sudo', 'su', '-c', 'rosdep update', user_name]
            execute_command(cmd)

        print_success()


    def step_12(self):
        """Copy scripts and configuration to /opt"""
        print_step("Step 12: " + str(self.step_12.__doc__))

        try:
            os.makedirs("/opt/htb")
        except OSError as ex:
           if not ex.errno == errno.EEXIST:
               raise

        copyfile("configuration.py", "/opt/htb/configuration.py")
        copyfile("htb-adduser.py", "/opt/htb/htb-adduser.py")
        cmd = ['chmod', '+x', '/opt/htb/htb-adduser.py']
        execute_command(cmd)

        cmd = ['ln', '-sf', '/opt/htb/htb-adduser.py', '/usr/bin/htb-adduser']
        execute_command(cmd)

        print_success()


    def step_13(self):
        """Create user robot"""
        print_step("Step 13: " + str(self.step_13.__doc__))

        print_subStep("Create new user 'robot'")
        print_subStep("Create catkin workspace of robot")
        print_info("/u/robot/git/catkinws")
        print("todo...")
        print()


    def step_14(self):
        """Get own htb-packages from git"""
        print_step("Step 14: " + str(self.step_14.__doc__))

        cmd = ['apt-get', 'install', 'libfreenect2', '--allow-unauthenticated']
        print("todo...")
        print()
