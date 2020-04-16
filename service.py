import vm, monitor, scream
from config import config

from flask import Flask

api = Flask(__name__)

@api.route('/post_init', methods=['GET'])
def post_init():
    scream.start()
    return str(True)

@api.route('/startup', methods=['GET'])
def startup():
    res = vm.startup(config.vm_name_hint)
    print('Starting', res[1].name(), '=', res[0], flush=True)
    return str(res[0])

@api.route('/shutdown', methods=['GET'])
def shutdown():
    res = vm.shutdown(config.vm_name_hint)
    print('Shutting down', res[1].name(), '=', res[0], flush=True)
    return str(res[0])

@api.route('/attach', methods=['GET'])
def attach():
    good = True
    for device,xml in config.devices.items():
        res = vm.attach(xml, config.vm_name_hint)
        print('Attached', device, 'to', res[1].name(), '=', res[0], flush=True)
        if not res[0]:
            good = False
    return str(good)

@api.route('/detach', methods=['GET'])
def detach():
    good = True
    print(len(config.devices.items()))
    for device,xml in config.devices.items():
        res = vm.detach(xml, config.vm_name_hint)
        print('Detached', device, 'from', res[1].name(), '=', res[0], flush=True)
        if not res[0]:
            good = False
    return str(good)

@api.route('/show', methods=['GET'])
def show():
    good = True
    for m,(shown,hidden) in config.monitors.items():
        res = monitor.set_input(m, shown)
        print('Showing VM ( monitor:', m, 'input code:', shown, ') =', res, flush=True)
        if not res:
            good = False
    return str(good)

@api.route('/hide', methods=['GET'])
def hide():
    good = True
    for m,(shown,hidden) in config.monitors.items():
        res = monitor.set_input(m, hidden)
        print('Hiding VM ( monitor:', m, 'input code:', hidden, ') =', res, flush=True)
        if not res:
            good = False
    return str(good)

@api.route('/toggle_hidden', methods=['GET'])
def toggle_hidden():
    good = True
    for m,(shown,hidden) in config.monitors.items():
        res = monitor.toggle_input(m, shown, hidden)
        print('Toggle view ( monitor:', m, ') =', res, flush=True)
        if not res:
            good = False
    return str(good)

if __name__ == '__main__':
    api.run()
