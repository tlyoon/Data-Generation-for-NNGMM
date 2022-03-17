import os
import numpy as np
from numpy.linalg import norm

rawdata=np.loadtxt('orientate.in')
rawdata=rawdata.tolist()

ranint=int(np.shape(rawdata)[0]/np.shape(rawdata)[1])
xsum=0;ysum=0;zsum=0
for i in range(1,ranint+1):
    #print(i)
    coor=[]
    for j in range(1,4+1):
        index=4*(i-1)+j
        rawdataline=rawdata[index-1]
        x=rawdataline[3]
        if j!=4:
#            print('i,index,j,x:',i,index,j,x)
            coor.append(x)
#        print(rawdataline)
    xsum=xsum+coor[0];ysum=ysum+coor[1];zsum=zsum+coor[2];
#    print(i,coor)
#    print(xsum,ysum,zsum)    
#    print('')
xmean,ymean,zmean=xsum/ranint,ysum/ranint,zsum/ranint
print('xmean,ymean,zmean',xmean,ymean,zmean)


#### remove existing 'orientate.out' and open append a new one 
try:
    os.remove('orientate.out')
except:
    zero=0
f = open('orientate.out', 'a')
#### end remove existing 'orientate.out' and open append a new one 



### shift all coordinates 
xsum=0;ysum=0;zsum=0
xpi=[];ypi=[];zpi=[];ri=[];
for i in range(1,ranint+1):
#    coor=[]
    for j in range(1,4+1):
        index=4*(i-1)+j
        rawdataline=rawdata[index-1]
        x=rawdataline[3]
        if j!=4:
            if j==1:
#                coor.append(x-xmean)
                xp=x-xmean
                xpi.append(xp)
                print('i,index,j,x,xp:',i,index,j,x,xp)
                #f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, xp)))
            if j==2:
#                coor.append(x-ymean)
                yp=x-ymean
                ypi.append(yp)
                print('i,index,j,y,yp:',i,index,j,x,yp)
                #f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, yp)))
            if j==3:
#                coor.append(x-zmean)
                zp=x-zmean
                zpi.append(zp)
                print('i,index,j,z,zp:',i,index,j,x,zp)
                #f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, zp)))
        if j==4:
            print('i,index,j,radius:',i,index,j,x)
            ri.append(x)
            #f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, x)))
    
#    print('i,xp,yp,zp:',i,coor[0],coor[1],coor[2])
#    print('i,xp,yp,zp:',i,xp,yp,zp)
    #print('')
#        print(rawdataline)
    #xsum=xsum+coor[0];ysum=ysum+coor[1];zsum=zsum+coor[2];
    xsum=xsum+xp;ysum=ysum+yp;zsum=zsum+zp;
    #print("$$",i,coor)
    print("xsum,ysum,zsum",xsum,ysum,zsum)
#    print('xmean,ymean,zmean:',xmean,ymean,zmean)    
    print('')
xmean,ymean,zmean=xsum/ranint,ysum/ranint,zsum/ranint
print('all coordinates have been shifted wrp to the centroid')
print('xmean,ymean,zmean',round(xmean),round(ymean),round(zmean))
print('')
### shift all coordinates 

#### constract new coordinate axes using xpi,ypi,zpi,ri 

lenri=len(ri)
listrsqri=[ [ np.square(xpi[i]) + np.square(ypi[i]) + np.square(zpi[i]), ri[i] ] for i in range(len(ri)) ]
slistrsqri=sorted(listrsqri, key=lambda x: x[0])
maxrsq=slistrsqri[-1][0]
maxrsqindex=[ listrsqri.index(x) for x in sorted(listrsqri) ][-1]
allpoints=[ [ xpi[i], ypi[i], zpi[i] ] for i in range(len(xpi)) ]
#print(listrsqri[maxrsqindex],maxrsq)

### derive xcappp #############
axpp=allpoints[maxrsqindex]
#print('axpp',axpp)
normaxpp=norm(axpp)
xcappp=axpp/normaxpp
xcappp=xcappp.tolist()
print('xcappp',xcappp)
print('norm(xcappp)',norm(xcappp))
### derive xcappp #############

### derive ycappp #############
drop2xcappp=[ np.square(norm([ xpi[i], ypi[i], zpi[i] ]))-np.square(np.dot(xcappp,[ xpi[i], ypi[i], zpi[i] ])) for i in range(len(xpi)) ]
sdrop2xcappp=np.sort(drop2xcappp)
maxdrop2xcappp=sdrop2xcappp[-1]
maxdrop2xcapppindex=[ drop2xcappp.index(x) for x in sdrop2xcappp ][-1]
Py=allpoints[maxdrop2xcapppindex]
Pydrop2xcappp=np.dot(Py,xcappp)
aypp=np.array(Py)-np.array(Pydrop2xcappp*np.array(xcappp))
normaypp=norm(aypp)
ycappp=aypp/normaypp
ycappp=ycappp.tolist()
print('ycappp',ycappp)
print('norm(ycappp)',norm(ycappp))
### end derive ycappp #############

### derive zcappp #############
zcappp=np.cross(xcappp,ycappp)
print('zcappp',zcappp)
print('norm(zcappp)',norm(zcappp))
### end derive zcappp #############

#### project all points onto xcappp,ycappp, zcappp, hence transforming all
#### points into the cappp coordinate
allpointspp=[ [ np.dot(allpoints[i],xcappp),np.dot(allpoints[i],ycappp), np.dot(allpoints[i],zcappp),ri[i] ] for i in range(len(allpoints))]


### assigning x and write to orientate.out
#for i in range(1,ranint+1):
for i in range(1,ranint+1):
    xyz=allpointspp[i-1]
    print('xyz',xyz)
    for j in range(1,4+1):
        index=4*(i-1)+j
        x=xyz[j-1]
        
        if j==1:
            print('i,index,j,xpp:',i,index,j,x)
            f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, x)))
        if j==2:
            print('i,index,j,ypp:',i,index,j,x)
            f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, x)))
        if j==3:
            print('i,index,j,zpp:',i,index,j,x)
            f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, x)))
        if j==4:
            print('i,index,j,radius:',i,index,j,x)
            f.write(("%5d %5d %5d %10.3f \n" % (i,index, j, x)))
    
    print('')
### end of assigning x and write to orientate.out

### close 'orientate.out' 
f.close()
### end close 'orientate.out' 

#### end of constract new coordinate axes using xpi,ypi,zpi,ri 
