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
  <address type="usb" bus="0" port="1"/>
</hostdev>
"""

devices['mouse'] = """
<hostdev mode="subsystem" type="usb" managed="yes">
  <source>
    <vendor id="0x12cf"/>
    <product id="0x0219"/>
  </source>
  <address type="usb" bus="0" port="2"/>
</hostdev>
"""

INPUT_DVI = 3
INPUT_DP = 15

monitors = {
    1: (INPUT_DP,INPUT_DVI),
}

# Service hostname
hostname = '192.168.86.26'

# Scream Installation Paths
scream_exec_path = '/opt/scream/Receivers/pulseaudio-ivshmem/scream-ivshmem-pulse'
scream_shm_path = '/dev/shm/scream-ivshmem'
pa_user = 1000
