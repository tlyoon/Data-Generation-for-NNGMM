import os 
import time

def executeSomething():
    #code here
    time.sleep(60)

files=os.listdir()
files.remove('convert_label_to_binary.py')
#print(files)
#print('')

for i in files:
    if len(i.split('@'))==2:
        
        state='cd ' + i + '; ln -s ../convert_label_to_binary.py . ; cd ../'
        print(state)        
        os.system(state)
        
        state='cd ' + i + '; python convert_label_to_binary.py'
        print(state)
        #os.system(state)
        
        state='unlink ' + i + '/convert_label_to_binary.py'
        print(state)        
        os.system(state)
