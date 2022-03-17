## this script scans the present directory for all {config.*_c_*.npy, label.*_c_*.npy}, {config.*_b_*.npy, label.*_b_*.npy} file pairs and fix up all nan errors within them. 
## The erronous file pairs will be renamed systematically, e.g., 
## config.320682_c_p25@c21.npy --> config.320669_c_p25@c21.npy 
##  label.320682_c_p25@c21.npy -->  label.320669_c_p25@c21.npy
## Note that only config.*_c_*.npy and label.*_c_*.npy files are rectified.


import numpy as np
import os

dirs=[ i for i in os.listdir() if (len(i.split('config'))==2 and len(i.split('_c'))==2) or \
      (len(i.split('config'))==2 and len(i.split('_b'))==2) ]
for i in dirs:
    print('')
    #print(i)
    ilabel='label'+i.split('config')[1]
    datal=np.load(ilabel)
    #array_sum = np.sum(datal)
    #array_has_nan = np.isnan(array_sum)
    #if array_has_nan:
    #    print(ilabel,'has_nan:',array_has_nan)
    #else:
    #    print(ilabel,'does not has nan')
        
    datac=np.load(i)
    array_sum = np.sum(datac)
    array_has_nan = np.isnan(array_sum)
    
    if array_has_nan:
        print('')
        print(i,'has_nan. To fix it.')
        state=[ i for i in range(len(datac)) if np.isnan(np.sum(datac[i])) ]
        print('The following lines have nan and are to be deleted',state)
        
        print('before deletion len(datal),len(datac)',len(datal),len(datac))       
        datac=np.delete(datac,state,axis=0)
        datal=np.delete(datal,state,axis=0)
        print('after deletion len(datal),len(datac)',len(datal),len(datac))       
        
        bname=i.split('_p')[-1]
        ldatac=str(len(datac))
        fnc2=ldatac+'_c_p'
        cname='config.'+fnc2+bname
        lname='label.'+fnc2+bname
        os.remove(i)
        os.remove(ilabel)
        np.save(cname,datac)
        np.save(lname,datal)
        print(i,'and',ilabel,'have been fixed and renamed',cname,lname)     
    else:
        print(i,'does not has nan')
