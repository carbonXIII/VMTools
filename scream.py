from config.config import pa_user, scream_exec_path, scream_args
import subprocess

import os, time, atexit

process = None

def killer():
    if process:
        if process.poll() is None:
            process.terminate()
        print('Scream exit code', process.wait())

def start():
    global process

    if process is None or process.poll() is not None:
        # Attempt to kill all running processes first
        try:
            subprocess.Popen(['killall','-9','scream']).wait()
        except:
            pass

        if pa_user:
            # Impersonate pa_user to avoid issues with local PA servers
            print('Starting scream as uid={}'.format(pa_user))
            cmd = 'machinectl shell $(id -un {})@.host {} {}'.format(
                pa_user,
                scream_exec_path,
                ' '.join(scream_args)
            )
            print('scream cmd:', cmd)
            process = subprocess.Popen([cmd],shell=True)
        else:
            print('Starting scream')
            process = subprocess.Popen([scream_exec_path, *scream_args])

        print('Started scream')

        # make sure scream dies
        atexit.register(killer)
