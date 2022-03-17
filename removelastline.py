import numpy as np

filein='label.1504202123.npy'
print('np.shape(np.load('+filein+')):',np.shape(np.load(filein)))


rawdata=np.load(filein)
removed=rawdata[:-1]

fileout=filein.split('.npy')[0]+'_rm.npy'
np.save(fileout,removed)

print('np.shape(np.load('+fileout+')):',np.shape(np.load(fileout)))
