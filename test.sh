#!/bin/bash

DEVS="0000:01:00.0 0000:01:00.1 0000:01:00.2 0000:01:00.3 0000:00:01.0"

for DEV in $DEVS; do
    echo "vfio-pci" > /sys/bus/pci/devices/$DEV/driver_override
    echo $DEV > /sys/bus/pci/devices/$DEV/driver/unbind
    echo $DEV > /sys/bus/pci/drivers_probe
done
