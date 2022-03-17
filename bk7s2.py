import os
import os.path
import numpy as np
from numpy import loadtxt

### raw data ######################
#print('')
# load raw data
print(os.getcwd())
fin='bk7s2.dat'
data = loadtxt(fin, delimiter=' ')
# print the array
dim0=np.shape(data)[0]
dim1=np.shape(data)[1]
#print('shape of '+fin,dim0,dim1)
### reshape raw data into a row vector
column=dim0*dim1
datar=np.reshape(data,(1,column))
dim0r=np.shape(datar)[0]
dim1r=np.shape(datar)[1]
print('shape of reshaped datar',dim0r,dim1r)


# manage label data 
fin='label.dat'
datal = loadtxt(fin)
#print('shape of '+fin,np.shape(datal))
### raw data ######################

### append label data into fin2="lable.npy"
fin="label.npy"
y = np.load(fin) if os.path.isfile(fin) else []
np.save(fin,np.append(y,datal)) 
nblockl=np.shape(np.load(fin))[0]
print('Number of blocks accumulated in '+fin,nblockl)
# end manage label data 


### manage fin2="config.npy"
fin2="config.npy"
 
if not os.path.isfile(fin2):
    np.save(fin2,datar)
    y=np.load(fin2)
    print('shape of '+fin2,'for the first time',np.shape(y))
else:    
    y = np.load(fin2) if os.path.isfile(fin2) else []
    #print('shape of '+fin2,'after append ',np.shape(np.load(fin2)))
    np.save(fin2,np.reshape(np.append(y,datar),(nblockl,column)))
    print('shape of '+fin2,'after append ',np.shape(np.load(fin2)))
nblockr=np.shape(np.load(fin2))[0]
### end manage fin2="config.npy"

print('Number of blocks accumulated in '+fin,nblockl)
print('Number of blocks accumulated in '+fin2,nblockr)


### check if the number of block in config.npy and label.npy are the same
if nblockl==nblockr:
    print('Number of block between '+fin+' and '+ fin2 +' equals:',nblockr)
else:
    print('WARNING !!!! Number of block between '+fin+' and '+ fin2 +' NOT equals:',nblockr,nblockl)
    
   #os.abort() 
print('')