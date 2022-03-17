import socket,os

#print(os.path.expanduser("~"))
#dir=os.listdir(os.path.expanduser("~")+'/dakota/dakota-gmt/data_generation/v2/record_small/data_train')
dir=os.listdir(os.path.expanduser("~")+'/dakota/dakota-gmt/data_generation/v2/record_small/data_repo_bk')
#dir=os.listdir('/home/tlyoon/dakota/dakota-gmt/data_generation/v2/record_small/data_train')
#print('dir:',dir)

try:
    hnint='c'+str(int(socket.gethostname().split('-')[-1]))
except:
    hnint=socket.gethostname().split('-')[-1].split('.')[0]
cont=[]
for i in dir:
    if len(i.split('@'+hnint))!=1:
        #print(i)
        cont.append(int(i.split('@'+hnint)[0].split('p')[1]))
try:
    p='p'+str(max(cont)+1)
except:
    p='p'+str(1)

#print('hostname:', hnint)
#print('production directory index:',p)

for i in os.listdir():
    if len(i.split('.npy'))>=2:
        j=i.split('.')[-2]
        head=i.split('.')[0]
        rename=head+'.'+j+'_'+p+'@'+hnint+'.npy'
        if i.find(p+'@'+hnint)!=-1:
            print(i,'existed. Not to rename')
        else:
            os.rename(i,rename)
            print(i,'is renamed to',rename)
