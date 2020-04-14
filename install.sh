#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo Installing from $DIR to "/opt/vmtools"

# Stop the any already running instances
systemctl stop vmtools || true

# Force Reinstall
rm -rf /opt/vmtools
cp -r . /opt/vmtools

# Install the service itself, and start
cp vmtools.service /etc/systemd/system/
systemctl daemon-reload
systemctl start vmtools


