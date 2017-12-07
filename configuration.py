

############
# WARNING: #
############
# The value of SLAVE has to be the number of existing client pcs.
# The value of EXTERN has to be the value of SLAVE +1
########################################################################
UNDEFINED = -1
MASTER = 0
SLAVE = 2
EXTERN = 3


htb_config = [
    ['htb-b1', '10.0.0.10', MASTER, 'Odroid Master'],
    ['htb-n1', '10.0.0.20', SLAVE, 'NUC Slave'],
    ['htb-o1', '10.0.0.30', SLAVE, 'Ordoid Slave'],
    ['extern', None, EXTERN, 'External pc']
]

packages_to_install = [
    ["vim"], # editors
    ["zsh"], # shells
    ["ipython", "ipython3"],
    ["htop"], # process viewer
    ["ranger"], # file manager
    ["tmux", "terminator"], # terminal multiplexer
    ["gitg", "openssh-server", "tree", "meld"]
]

turtlebot_packages = [
    "ros-kinetic-turtlebot",
    "ros-kinetic-turtlebot-stage",
    "ros-kinetic-turtlebot-apps",
    "ros-kinetic-turtlebot-interactions",
    "ros-kinetic-turtlebot-simulator",
    "ros-kinetic-ar-track-alvar-msgs"
]

external_install_steps = [
    1, 5, 6, 7, 12
]
