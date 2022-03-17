import os 
from time import sleep

exe='grep_isnan.py'

files=os.listdir()
try:
    files.remove(exe)
except:
    zero=0

for i in files:
    if len(i.split('@'))==2:
        state='cd ' + i + '; ln -s ../' + exe + ' . ; cd ../'
        print(state)        
        os.system(state)
        
        state='cd ' + i + '; python ' + exe
        print(state)
        os.system(state)
        sleep(5)
        
        state='unlink ' + os.path.join(i,exe)
        print(state)
        os.system(state)        
        
        print('os.path.isfile(os.path.join(i,exe))',os.path.isfile(os.path.join(i,exe)))
        print('')
