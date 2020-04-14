import devices, monitor, scream
from config import config

from flask import Flask

api = Flask(__name__)

@api.route('/post_init', methods=['GET'])
def post_init():
    scream.start()
    return str(True)

@api.route('/startup', methods=['GET'])
def startup():
    print('Starting {}'.format(config.vm_name))
    return str(devices.run('start {}'.format(config.vm_name)))

@api.route('/shutdown', methods=['GET'])
def shutdown():
    print('Shutting down {}'.format(config.vm_name))
    return str(devices.run('shutdown {} --mode acpi'.format(config.vm_name)))

@api.route('/attach', methods=['GET'])
def attach():
    for device,xml in config.devices.items():
        print("Attaching {} to {}".format(device, config.vm_name))
        if not devices.attach(config.vm_name, xml):
            return str(False)
    return str(True)

@api.route('/detach', methods=['GET'])
def detach():
    for device,xml in config.devices.items():
        print("Detaching {} from {}".format(device, config.vm_name))
        if not devices.detach(config.vm_name, xml):
            return str(False)
    return str(True)

@api.route('/show', methods=['GET'])
def show():
    good = True
    for m,(shown,hidden) in config.monitors.items():
        print('Showing VM (monitor: {}, input code: {})'.format(m, shown))
        if not monitor.set_input(m, shown):
            good = False
    return str(good)

@api.route('/hide', methods=['GET'])
def hide():
    good = True
    for m,(shown,hidden) in config.monitors.items():
        print('Showing Host (monitor: {}, input code: {})'.format(m, hidden))
        if not monitor.set_input(m, hidden):
            good = False
    return str(good)

@api.route('/toggle_hidden', methods=['GET'])
def toggle_hidden():
    good = True
    for m,(shown,hidden) in config.monitors.items():
        print('Toggling View (monitor: {}, input codes: {},{})'.format(m,shown,hidden))
        if not monitor.toggle_input(m, shown, hidden):
            good = False
    return str(good)

if __name__ == '__main__':
    api.run()
