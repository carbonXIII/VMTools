"""
Modify the settings below for your particular config.

The xml files mouse.xml, keyboard.xml must also be updated.
"""

import os

path = os.path.dirname(os.path.realpath(__file__))
def get_file(name):
    return '{}/{}'.format(path, name)

# VM config
vm_name_hint = 'win10'

devices = {}

devices['keyboard'] = """
<hostdev mode="subsystem" type="usb" managed="yes">
  <source>
    <vendor id="0x1532"/>
    <product id="0x0203"/>
  </source>
  <address type="usb" bus="0" port="5"/>
</hostdev>
"""

devices['mouse'] = """
<hostdev mode="subsystem" type="usb" managed="yes">
  <source>
    <vendor id="0x1532"/>
    <product id="0x0085"/>
  </source>
  <address type="usb" bus="0" port="6"/>
</hostdev>
"""

INPUT_DVI = 3
INPUT_DP = 15
INPUT_HDMI = 17

monitors = {
    0: [INPUT_DP,INPUT_DVI,INPUT_HDMI],
    1: [INPUT_DP,INPUT_DVI,INPUT_HDMI],
}

# Service hostname
hostname = '192.168.122.1'

# Scream Installation Paths
scream_exec_path = '/opt/scream/bin/scream'
scream_args = ['-m','/dev/shm/scream-ivshmem','-o','pulse']
pa_user = 1000
