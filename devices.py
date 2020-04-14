import subprocess

def run(args):
    args_ = args.split()
    ret = subprocess.Popen(['virsh'] + args_).wait()
    return ret == 0

def attach(vm, xml):
    return run('attach-device {} --file {} --current'.format(vm, xml))

def detach(vm, xml):
    return run('detach-device {} --file {}'.format(vm, xml))
