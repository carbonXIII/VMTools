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
    scream.start()

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

@api.route('/show/<int:sink>/<int:source>', methods=['GET'])
def show(sink, source):
    val = config.monitors[sink][source]
    return str(monitor.set_input(sink, val))

@api.route('/toggle_hidden/<int:sink>/<int:A>/<int:B>', methods=['GET'])
def toggle_hidden(sink, A, B):
    good = True

    a = config.monitors[sink][A]
    b = config.monitors[sink][B]

    return str(monitor.toggle_input(sink, a, b))

if __name__ == '__main__':
    api.run()
