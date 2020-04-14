from config.config import scream_exec_path, scream_shm_path
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

    if process is None:
      process = subprocess.Popen([scream_exec_path, scream_shm_path])
      print('Started scream')

    # make sure scream dies
    atexit.register(killer)
