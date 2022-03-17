## Use this code to reap all *.npy in directories $hostname.1,$hostname.2,..., into 
## reap/label.npy, reap/config.npy, 

from numpy import loadtxt
import shutil
import os
import numpy as np
pwd=os.getcwd()
#print(os.getcwd())


reapdir=os.path.join(pwd, 'reap')
storagedir=os.path.join(pwd, 'storage')
#print('reapdir',reapdir)
if os.path.isdir(reapdir):
#    print(os.path.isdir(reapdir))
    nothng=0
else:
    os.mkdir(reapdir)


from datetime import datetime
now = datetime.now()
#print("now =", now)
#dt_string = now.strftime("%d/%m/%Y%H:%M:%S")
dt_string = now.strftime("%d%m%Y%H")
#print("date and time =", dt_string)
###

subfolders = [ f.path for f in os.scandir(pwd) if f.is_dir() ]
reaplabel=os.path.join(pwd, 'reap','label.npy')
reapconfig=os.path.join(pwd, 'reap','config.npy')
'''
print('reaplabel:',reaplabel)
print('')
print('reapconfig:',reapconfig)
print('')
print('os.path.isfile(reaplabel):',os.path.isfile(reaplabel))
print('os.path.isfile(reapconfig):',os.path.isfile(reapconfig))
'''


if os.path.isfile(os.path.join(pwd, 'reap','config.npy')):
    shutil.copy(reapconfig,os.path.join(pwd, 'reap','config.'+dt_string+'.npy'))
    os.remove(reapconfig) if os.path.isfile(reapconfig) else [] # get data if exist

if os.path.isfile(os.path.join(pwd, 'reap','label.npy')):
    shutil.copy(reaplabel,os.path.join(pwd, 'reap','label.'+dt_string+'.npy'))
    os.remove(reaplabel) if os.path.isfile(reaplabel) else [] # get data if exist

    
'''
print('os.path.isfile(reaplabel):',os.path.isfile(reaplabel))
print('os.path.isfile(reapconfig):',os.path.isfile(reapconfig))
'''

try: 
    subfolders.remove(reapdir)
except: 
    nothing=0
	
try: 
    subfolders.remove(storagedir)
except: 
    nothing=0

#print('subfolders:',subfolders)

#iblock=0;

###
fbk=os.path.join(subfolders[0], 'bk7s2.dat')
fbkdata = loadtxt(fbk, delimiter=' ')
dim0=np.shape(fbkdata)[0]
dim1=np.shape(fbkdata)[1]
#print('shape of '+fbk,dim0,dim1)
column=dim0*dim1
print('Number of column in each block as determined from',fbk,':',column)
print('')
###
for i in subfolders:
    labelnpy=os.path.join(i, 'label.npy')
    confignpy=os.path.join(i, 'config.npy')
    
    if os.path.isfile(labelnpy) and os.path.isfile(confignpy):
        
        datal=np.load(labelnpy)
        print('np.shape for',labelnpy,'in',i,':',np.shape(datal))     
        y = np.load(reaplabel) if os.path.isfile(reaplabel) else [] 
        nblockl=np.shape(datal)[0]
        np.save(reaplabel,np.append(y,datal))      
        
        datac=np.load(confignpy)
        print('np.shape for',confignpy,'in',i,':',np.shape(datac))
        y = np.load(reapconfig) if os.path.isfile(reapconfig) else []
        
        if not os.path.isfile(reapconfig):
            np.save(reapconfig,datac)
            y=np.load(reapconfig)
        else:    
            y=np.load(reapconfig) if os.path.isfile(reapconfig) else []
            print('shape(y)',np.shape(y),'shape(datac)',np.shape(datac))
            iblock=np.shape(y)[0]+np.shape(datac)[0]
            np.save(reapconfig,np.reshape(np.append(y,datac),(iblock,column)))
 
    loaded=np.load(reapconfig);loadedl=np.load(reaplabel);
    dim=np.shape(loaded);diml=np.shape(loadedl);
    print('shape of reap/config.npy',dim,'shape of reap/label.npy',diml)
    if dim[0]==diml[0]:
        print('Number of blocks in reap/config.npy',dim[0],'tallies with that in reap/label.npy',diml[0],'up to',i)
    else:
        print('Number of blocks in reap/config.npy',dim[0],'DOES NOT tally with that in reap/label.npy',diml[0],'up to',i)
    print('')
#print('*.npy data in', [ os.path.split(j)[-1] for j in subfolders ])
#print(subfolders)
#print('have been reaped into ',reapconfig,'and',reaplabel)
print('')

#### now, check the dimension of the label.npy and config.npy saved in reap/

### read in config.npy to check dimensionality 
loadedl=np.load(reaplabel)
diml=np.shape(loadedl)[0]
print('Number of blocks accumulated in reap/label.npy',diml)
loadedc=np.load(reapconfig)
dimc=np.shape(loadedc)
#print('shape of reap/config.npy',dimc)
print('Number of blocks accumulated in reap/config.npy:',dimc[0])

if diml==dimc[0]:
    import platform
    import socket
    hn='c'+socket.gethostname()[-2:]
    #fnc='config.'+str(dim[0])+'@'+hn+'.npy'
    #fnl='label.'+str(dim[0])+'@'+hn+'.npy'
    fnc='config.'+str(dim[0])+'.npy'
    fnl='label.'+str(dim[0])+'.npy'
    print('save reap/config.npy as',fnc)
    print('save reap/label.npy as',fnl)
    os.system('mv reap/config.npy reap/'+fnc)
    os.system('mv reap/label.npy reap/'+fnl)
else: 
    print('remove reap/config.npy and reap/config.npy because number of block mismatch')
    os.system('rm -rf reap/config.npy  reap/label.npy')
