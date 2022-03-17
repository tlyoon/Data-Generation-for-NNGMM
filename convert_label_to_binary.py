
## place this script in a folder containing original data files, e.g., label.170000_p1@c27, config.170000_p1@c27, ...
## which contain -99999.0 and nan. It will scan the directory for all label.*.npy, config.*.npy
## files to generate a corresponding copy file named e.g., label.170000_b_p1@c27, config.170000_b_p1@c27
import sys
import atexit
import time
import numpy as np, os 

def executeSomething():
    #code here
    time.sleep(60)


files=os.listdir()
files.remove('convert_label_to_binary.py')
print(files)
print('')


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
    ##
    #### remove nan and rename to *_b_ from orig data files #######
    for i in files:
        if len(i.split('label.'))==2 and i.split('.')[-1]=='npy' and \
            len(i.split('_c'))!=2  and len(i.split('_b'))!=2 and len(i.split('_bb'))!=2:
            
            midname=i.split('.')[1]
            config='config.'+i.split('.')[1]+'.npy'
            #print(config,os.path.isfile(config))
            #print(i,os.path.isfile(i))
            Xte=config
            Yte=i
            print(Xte,os.path.isfile(Xte))
            print(Yte,os.path.isfile(Yte))
            print('')
            
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
            dY_testc={i:dY_test[i] for i in dY_test if not np.isnan(dY_test[i])}
            dY_testckeys=list(dY_testc.keys())
            Y_testc=list(dY_testc.values())
            Y_testc=np.array(Y_testc)
            
            X_testc=[ X_test[i] for i in dY_testckeys ]
            X_testc=np.array(X_testc)
            
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
                #newXte=n0Xte+'.' + str(X_testc.shape[0])+ psource + '_b.npy'
                newXte=n0Xte+'.'+str(X_testc.shape[0])+'_b'+psource+'.npy'
            except:
                #integer='.'+ n1Xte.split('_')[0]
                #newXte=n0Xte+'.'+str(X_testc.shape[0])+'_b.npy'
                newXte=n0Xte+'.'+str(X_testc.shape[0])+'_b'+psource+'.npy'
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
                #newYte=n0Yte+'.' + str(Y_testc.shape[0])+ psource + '_b.npy'
                newYte=n0Yte+'.'+str(Y_testc.shape[0])+'_b'+psource+'.npy'
            except:
                integer=n1Yte.split('_')[0]
                #newYte=n0Yte+'.'+str(Y_testc.shape[0])+'_b.npy'
                newYte=n0Yte+'.'+str(Y_testc.shape[0])+'_b'+psource+'.npy'
            np.save(newYte,Y_testc)
            print(Yte,Xte,'have been cleaned. The resultant files have been saved as',newYte,newXte)
            print('')
    #### remove nan and rename to *_b_ from orig data files #######
    
    
    print('')
    print('Now, begin constructing binary Y files')
    files=os.listdir()
    files.remove('convert_label_to_binary.py')
    print(files)
    print('')
    
    
    #### start constructing binary Y files 
    for i in files:
        if len(i.split('label.'))==2 and i.split('.')[-1]=='npy' and \
            len(i.split('_c'))!=2  and len(i.split('_b'))==2 and len(i.split('_bb'))!=2:
            midname=i.split('.')[1]
            config='config.'+i.split('.')[1]+'.npy'
            Xte=config
            Yte=i
            print(Xte,os.path.isfile(Xte))
            print(Yte,os.path.isfile(Yte))
            print('')
            print('to convert ',Yte,'into binary version')
            print('')
            
            ###
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
            print('before convertion',Yte, ':',Y_test.shape)
            dY_test=dict(zip(list(range(len(Y_test))),Y_test))
            Y_testc={}
            for i in range(len(dY_test)):
                if dY_test[i] == -99999.0:
                    Y_testc[i]='F'
                else:
                    Y_testc[i]='T'
            Y_testc=[ i for i in Y_testc.values() ]
            print('after conversion',Yte,':', len(Y_testc))
            #####    
                   
            ### rename and save Ytestc ########
            #n0Yte=Yte.split('.npy')[0].split('.')[0]
            #try: 
            #    integer=int(n1Yte.split('_')[0])
            #    psource='_'+n1Yte.split('_')[1]
            #    newYte=n0Yte+'.'+str(Y_testc.shape[0])+'_bb'+psource+'.npy'
            #except:
            #
            integer=n1Yte.split('_')[0]
            #    newYte=n0Yte+'.'+str(len(Y_testc))+'_bb'+psource+'.npy'
            newYte=Yte.split('_b')[0]+'_bb'+Yte.split('_b')[1]
            np.save(newYte,Y_testc)
            os.remove(Yte)
            os.rename(newYte,Yte)
            print(Yte,'has been converted. The resultant file is saved as',Yte)
            print('check if np.shape(X_test) == len(np.load(Yte))')
            print(np.shape(X_test)[0] == len(np.load(Yte)))
            print('np.shape(X_test)[0]:',np.shape(X_test)[0])
            print('len(np.load(Yte)):',len(np.load(Yte)))
            print('')
            
            ###
    #### end start constructing binary Y files 
    
    ##
		### end Place your code here
		
except KeyboardInterrupt:
    sys.exit(0)