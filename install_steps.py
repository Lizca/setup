
from __future__ import print_function
from htb_install import *
from colors import ColorPrinter
import uuid, os, errno

class InstallSteps:

    robot = None
    actingType = ActingType.UNDEFINED
    robotIP = None

    cp = ColorPrinter()

    def step_01(self):
        """Step 1: Setup language and time settings"""
        self.cp.cfg('y', None, 'ib').out(self.step_01.__doc__)
        self.cp.out(len(self.step_01.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Set system language and keyboard layout")
        cmd = ['cp', 'templates/locale', '/etc/default/locale']
        execute_command(cmd)
        print_info("Your language has been set to 'LANG=de_DE.UTF-8' and keyboard layout to 'KEYMAP=de-latin1-nodeadkeys'")

        self.cp.cfg('y', None, 'i').out("Set time zone")
        try:
            cmd = ['unlink', '/etc/localtime']
            execute_command(cmd)
        except:
            pass
        cmd = ['ln', '-s', '/usr/share/zoneinfo/Europe/Berlin', '/etc/localtime']
        execute_command(cmd)
        print_info("Your timezone has been set to Europe/Berlin")

        self.cp.cfg('y', None, 'i').out("Set hardware clock")
        cmd = ['timedatectl', 'set-local-rtc', '0']
        execute_command(cmd)
        execute_command(['date'])

        self.cp.cfg('y', None, 'i').out("Generate locales")
        cmd = ['cp', 'templates/locale.gen', '/etc/locale.gen']
        #subprocess.call(["locale-gen"])
        cp.cfg('k', 'g', 'f').out("-> Successful")
        print()



    def step_02(self):
        """Step 2: Set hostname"""
        self.cp.cfg('y', None, 'ib').out(self.step_02.__doc__)
        self.cp.out(len(self.step_02.__doc__) * '"')

        cmd = ['hostnamectl', 'set-hostname', htb_config[int(self.robot)]][0]
        #execute_command(cmd)
        print_info("The hostname has been set to " + htb_config[int(self.robot)][0] + ' ('+htb_config[int(self.robot)][3]+')')

        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_03(self):
        """Step 3: Setup user account robot-local"""
        self.cp.cfg('y', None, 'ib').out(self.step_03.__doc__)
        self.cp.out(len(self.step_03.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Check if the user robot-local exists")
        if 'robot-local' in open('/etc/passwd').read():
            self.cp.cfg('k', 'g', 'f').out("-> Found!")
        else:
            self.cp.cfg('k', 'y', 'bf').out("-> No user 'robot-local' found!")
            self.cp.cfg('y', None, 'i').out("Create new user 'robot-local'")
            cmd = ['adduser', '--disabled-password', '--gecos', '""', 'robot-local', '--home', '/home/robot-local']
            execute_command(cmd)

        self.cp.cfg('y', None, 'i').out("Add user to groups")
        cmd = ['adduser', 'robot-local', 'sudo']
        execute_command(cmd)

        self.cp.cfg('y', None, 'i').out("Set account password")
        cmd = ['chpasswd', '-e']
        execute_command(cmd, input=b'robot-local:$6$q4PV2O6Zww/wqTzx$v4Fg21NOOovlSkkhIx/sRLGJSvt9FhSkUjNAkfW6OtenDp/DdI4EAHhLT.1KXhB6SNWL0xTgIx7ECXW60Yjzv1\n')

        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_04(self):
        """Step 4: Setup network connection"""
        self.cp.cfg('y', None, 'ib').out(self.step_04.__doc__)
        self.cp.out(len(self.step_04.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Create file /etc/network/interfaces")
        if False:
            cmd = ['rm', '/etc/network/interfaces_foo']
            execute_command(cmd)

        tempfile = open("templates/interfaces")
        interfaces = open("/etc/network/interfaces_foo", 'w+')
        for line in tempfile:
            if line.startswith("address"):
                interfaces.write("address " + htb_config[int(self.robot)][1] + '\n')
            else:
                interfaces.write(str(line))
        tempfile.close()
        interfaces.close()

        self.cp.cfg('y', None, 'i').out("Start ethernet connection")
        cmd = ['ifdown', 'eth0']
        # execute_command(cmd)
        cmd = ['ifup', '-v', 'eth0']
        # execute_command(cmd)
        self.cp.cfg('y', None, 'i').out("Test connection")
        cmd = ['ping', '-c2', 'www.github.com']
        execute_command(cmd)
        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_05(self):
        """Step 5: Add htb-packages to APT-Sources"""
        self.cp.cfg('y', None, 'ib').out(self.step_05.__doc__)
        self.cp.out(len(self.step_05.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Install depended Package")
        cmd = ['apt-get', 'install', 'apt-transport-https', '-y']
        execute_command(cmd)

        self.cp.cfg('y', None, 'i').out("Add htb-repository to APT-Sources")
        cmd = ['sh', '-c',
               'echo "deb https://raw.githubusercontent.com/hhntb/htb_aptrepo/master $(lsb_release -sc) main" > /etc/apt/sources.list.d/github-htb-aptrepo.list']
        execute_command(cmd)
        print_info("https://raw.githubusercontent.com/hhntb/htb_aptrepo/master")

        self.cp.cfg('y', None, 'i').out("Update APT-Sources")
        cmd = ['apt-get', 'update']
        execute_command(cmd)
        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_06(self):
        """Step 6: Upgrade System"""
        self.cp.cfg('y', None, 'ib').out(self.step_06.__doc__)
        self.cp.out(len(self.step_06.__doc__) * '"')

        cmd = ['apt-get', 'upgrade', '-y']
        execute_command(cmd)
        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_07(self):
        """Step 7: Install base packages"""
        self.cp.cfg('y', None, 'ib').out(self.step_07.__doc__)
        self.cp.out(len(self.step_07.__doc__) * '"')

        for p in packages_to_install:
            execute_command(["apt-get", "install", "-y", p])
            self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_08(self):
        """Step 8: Setup additional system configuration"""
        self.cp.cfg('y', None, 'ib').out(self.step_08.__doc__)
        self.cp.out(len(self.step_08.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Allow shutdown when powerbutton has been pressed")
        cmd = ['cp', 'templates/powerbtn.sh', '/etc/acpi/powerbtn.sh']
        print_info("Edit file /etc/acpi/powerbtn.sh")
        execute_command(cmd)

        self.cp.cfg('y', None, 'i').out("Let ssh server send alive signal")
        rewrite_file("/etc/ssh/sshd_config", "ClientAliveInterval", "ClientAliveInterval 60\n")
        print_info("Edit file /etc/ssh/sshd_config")

        self.cp.cfg('y', None, 'i').out("Disable root account")
        cmd = ['chpasswd', '-e']
        execute_command(cmd, input=b'root:!\n')
        print_info("Root account is now no longer usable")

        self.cp.cfg('y', None, 'i').out("Create new group htb")
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

        self.cp.cfg('y', None, 'i').out("Add name resolution to /etc/hosts")
        for r in range(0, len(htb_config)):
            if not r == int(self.robot):
                file = open("/etc/hosts_foo", 'r')
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
                    file = open("/etc/hosts_foo", 'r+')
                    lines = file.readlines()
                    file.write(htb_config[r][1] + " " + htb_config[r][0] + '\n')
                    file.close()


                elif host_exist and not ip_correct:
                    file = open("/etc/hosts_foo", 'w')
                    file.write("\n" + htb_config[r][1] + " " + htb_config[r][0] + '\n')
                    for line in lines:
                        file.write(line)

                    file.close()


        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()



    def step_09(self):
        """Step 9: Setup NFS"""
        self.cp.cfg('y', None, 'ib').out(self.step_09.__doc__)
        self.cp.out(len(self.step_09.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Install needed packages")
        cmd = ['apt-get', 'install', 'nfs-kernel-server', '-y']
        #execute_command(cmd)

        self.cp.cfg('y', None, 'i').out("Create directory '/u'")
        cmd = ['mkdir', '/ u']
        #execute_command(cmd)

        self.cp.cfg('y', None, 'i').out("Activate STATD")
        rewrite_file("/etc/default/nfs-common", "NEED_STATD", "NEED_STATD=yes\n")

        if self.actingType.value == ActingType.MASTER.value:
            self.cp.cfg('y', None, 'i').out("Editing '/etc/fstab'")
            rewrite_file("/etc/fstab_foo", "[uuid]", "[uuid] /u ext4 rw,suid,dev,auto,nouser,sync,noatime,nofail 0 0\n")

            self.cp.cfg('y', None, 'i').out("Mount external device")
            cmd = ['mount', '/u']
            #execute_command(cmd)
            self.cp.cfg('y', None, 'i').out("Edit /etc/exports")
            rewrite_file("/etc/exports", "/u", "/u *(rw,fsid=0,sync,no_subtree_check)\n")

        elif self.actingType.value == ActingType.SLAVE.value:
            self.cp.cfg('y', None, 'i').out("Install needed packages")
            cmd = ['apt-get', 'install', 'autofs', '-y']
            execute_command(cmd)

            self.cp.cfg('y', None, 'i').out("Edit /etc/auto.master")
            rewrite_file("/etc/auto.master", "/-", "/- /etc/auto.direct\n")

            self.cp.cfg('y', None, 'i').out("Create /etc/auto.direct")
            file = open("/etc/auto.direct", 'w+')
            file.write("/u -fstype=nfs4 " + htb_config[0][1] + ":/\n")

            self.cp.cfg('y', None, 'i').out("Activate NFS")
            cmd = ['update-rc.d', 'autofs', 'defaults']
            #execute_command(cmd)
            cmd = ['service', 'autofs', 'restart']
            #execute_command(cmd)
            cmd = ['modprobe', 'nfs']
            #execute_command(cmd)

        #cp.cfg('y', None, 'i').out("foo")
        #cmd = ['systemctl', 'daemon-reload']
        #execute_command(cmd)

        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()

        #cp.cfg('y', None, 'ib').out("Initiate Reboot")
        #cp.out('""""""""""""""""')
        #print()


    def step_10(self):
        """Step 10: ssh key exchange"""
        self.cp.cfg('y', None, 'ib').out(self.step_10.__doc__)
        self.cp.out(len(self.step_10.__doc__) * '"')

        tempname = "/tmp/file" + str(uuid.uuid4()) #os.tempnam()
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
        cmd = ['ssh-copy-id', htb_config[int(self.robot)][0]]
        #execute_command(cmd)

        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_11(self):
        """Step 11: Setup NTP"""
        self.cp.cfg('y', None, 'ib').out(self.step_11.__doc__)
        self.cp.out(len(self.step_11.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Install needed package")
        cmd = ['apt-get', 'install', 'ntp', '-y']
        execute_command(cmd)
        if self.actingType.value == ActingType.MASTER.value:
            self.cp.cfg('y', None, 'i').out("Edit /etc/ntp.conf")
            #rewrite_file("/etc/ntp.conf", "pool 0.ubuntu", "server 0.pool.ntp.org\n")
            #rewrite_file("/etc/ntp.conf", "restrict " + htb_config[0][1], "restrict " + htb_config[0][1] + " mask 255.255.255.0 nomodify notrap\n")
        elif self.actingType.value == ActingType.SLAVE.value:
            self.cp.cfg('y', None, 'i').out("Edit /etc/ntp.conf")
            #rewrite_file("/etc/ntp.conf", "pool 0.ubuntu", "server " + htb_config[0][1] + "\n")

        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_12(self):
        """Step 12: Install ROS"""
        self.cp.cfg('y', None, 'ib').out(self.step_12.__doc__)
        self.cp.out(len(self.step_12.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Setup source.list and keys")
        cmd = ['sh', '-c',
               'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list']
        execute_command(cmd)
        cmd = ['apt-key', 'adv', '--keyserver', 'hkp://ha.pool.sks-keyservers.net:80', '--recv-key',
               '421C365BD9FF1F717815A3895523BAEEB01FA116']
        execute_command(cmd)

        self.cp.cfg('y', None, 'i').out("Update ATP-sources")
        execute_command(['apt-get', 'update'])

        self.cp.cfg('y', None, 'i').out("Install ROS packages")
        execute_command(['apt-get', 'install', 'ros-kinetic-ros-base'])

        self.cp.cfg('y', None, 'i').out("Install ros-turtlebot packages")
        for p in turtlebot_packages:
            execute_command(['apt-get', 'install', p])

        self.cp.cfg('y', None, 'i').out("Initialize rosdep")
        # execute_command(['rosdep', 'init'])
        # execute_command(['rosdep', 'update'])
        self.cp.cfg('k', 'g', 'f').out("-> Successfull")
        print()


    def step_13(self):
        """Step 14: Create user robot"""
        self.cp.cfg('y', None, 'ib').out(self.step_14.__doc__)
        self.cp.out(len(self.step_14.__doc__) * '"')

        self.cp.cfg('y', None, 'i').out("Create new user 'robot'")
        self.cp.cfg('y', None, 'i').out("Create catkin workspace of robot")
        print_info("/u/robot/git/catkinws")
        print("todo...")
        print()


    def step_14(self):
        """Step 15: Get own htb-packages from git"""
        self.cp.cfg('y', None, 'ib').out(self.step_15.__doc__)
        self.cp.out(len(self.step_15.__doc__) * '"')
        cmd = ['apt-get', 'install', 'libfreenect2']
        print("todo...")
        print()
