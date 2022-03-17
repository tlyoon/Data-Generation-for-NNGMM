#https://stackoverflow.com/questions/788411/check-to-see-if-python-script-is-running

import numpy as np
import os,sys
import shutil
import atexit

import time

def executeSomething():
    #code here
    time.sleep(6)

while True:
    executeSomething()
    
    try:
        # Set PID file
        def set_pid_file():
            pid = str(os.getpid())
            f = open('myCode.pid', 'w')
            f.write(pid)
            f.close()
    
        def goodby():
            pid = str('myCode.pid')
            os.remove(pid)
    
        atexit.register(goodby)
        set_pid_file()
    
        # Place your code here
        os.system('sh launch_local.sh')
        # end Place your code here
    
    except KeyboardInterrupt:
        sys.exit(0)
