### reference https://stackabuse.com/tensorflow-2-0-solving-classification-and-regression-problems/

import numpy as np

# provide the names of data files in *.npy format to be 'cleaned'
# these files must come in pair, e.g., Xte='config.2.npy', Yte='label.2.npy'
Xte='config.npy'
Yte='label.npy'

#Yte='label.103402_p3@c27.npy'
#Xte='config.103402_p3@c27.npy'

### dont touch anything below ###########
X_test = np.load(Xte)
Y_test = np.load(Yte)

###### check if dimension in the *.npy data files are consistent.
f1=Xte
f2=Yte
#print(f1,np.load(f1).shape)
#print(f2,np.load(f2).shape)
if  np.load(f1).shape[0] != np.load(f2).shape[0]:
    print('dimension between',f1,f2,'is not consistent. To abort')
    exit()
#####


print('before reshaping,',Yte, ':',Y_test.shape)
print('before reshaping,',Xte, ':',X_test.shape)


#### cleaning test data #######
dY_test=dict(zip(list(range(len(Y_test))),Y_test))
dX_test=dict(zip(list(range(len(X_test))),X_test))

dY_testc={i:dY_test[i] for i in dY_test if not dY_test[i] == -99999.0 and not np.isnan(dY_test[i])}
#dY_testc={i:dY_test[i] for i in dY_test if not np.isnan(dY_test[i])}
dY_testckeys=list(dY_testc.keys())
Y_testc=list(dY_testc.values())
Y_testc=np.array(Y_testc)
#print(dY_testckeys)
X_testc=[ X_test[i] for i in dY_testckeys ]
X_testc=np.array(X_testc)
#print( [Y_testc[i] for i in range(len(Y_testc)) ])
#print( [X_testc[i] for i in range(len(X_testc)) ])

print('after reshaping',Yte,':', Y_testc.shape)
print('after reshaping',Xte,':', X_testc.shape)

### rename and save Xtestc ########
n0Xte=Xte.split('.npy')[0].split('.')[0]
try: 
    n1Xte=Xte.split('.npy')[0].split('.')[1]
except:
    n1Xte=''
    
try: 
    integer=int(n1Xte.split('_')[0])
    psource='_'+n1Xte.split('_')[1]
    newXte=n0Xte+'.' + str(X_testc.shape[0])+ psource + '_c.npy'
except:
    #integer='.'+ n1Xte.split('_')[0]
    newXte=n0Xte+'.'+str(X_testc.shape[0])+'_c.npy'
np.save(newXte,X_testc)


### rename and save Ytestc ########
n0Yte=Yte.split('.npy')[0].split('.')[0]
try: 
    n1Yte=Yte.split('.npy')[0].split('.')[1]
except:
    n1Yte=''

try: 
    integer=int(n1Yte.split('_')[0])
    psource='_'+n1Yte.split('_')[1]
    newYte=n0Yte+'.' + str(Y_testc.shape[0])+ psource + '_c.npy'
except:
    integer=n1Yte.split('_')[0]
    newYte=n0Yte+'.'+str(Y_testc.shape[0])+'_c.npy'
np.save(newYte,Y_testc)

print(Yte,Xte,'have been cleaned. The resultant files have been saved as',newYte,newXte)
#### end cleaning test data #######
