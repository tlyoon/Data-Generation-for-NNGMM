import numpy as np
import os 
import random

os.system('ls config*.npy > ls.dat')
f = open("ls.dat", "r")
llsdat=f.readlines() 

lconfig=[ llsdat[i].rstrip() for i in range(len(llsdat)) ]
print('')
for i in lconfig:
    if len(i.split('.'))==3:
       datetime=i.split('.')[1]
       l='label.' + datetime + '.npy'
       #print(i,l,os.path.isfile(l))
       if not os.path.isfile(l):
           continue
    else:
        l='label.npy'
#        print(i,l)
    f1=i;f2=l
    #print(f1,f2)
    print(f1,np.load(f1).shape)
    print(f2,np.load(f2).shape)
    datafile=np.load(f2)
    lendata=len(datafile)
    ranint=random.randint(0,lendata)
    ran2=random.randint(ranint+1,lendata)
    print('sample content in',f2)
    print(datafile[ranint:ran2])

    datafile=np.load(f1)
    print('sample content in',f1)
    print(datafile[ranint:ran2])
    if True in np.isnan(datafile):
        print("************* WARNING ********************")
        print('nan is found in ',f1)
        print("************* WARNING ********************")
    print('')

os.system('rm -rf ls.dat')
