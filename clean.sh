#! /bin/bash

rm -rf  tgmN.dat texpN.dat gmt.dat xdata xdata.dat *.out
rm -rf pltgmexpN.jpg aggregate.jpg dirname.dat a.out bk7s2.dat bk7s2.k
rm -rf temp *.out mycal.dat *.log
rm -rf dakota_mycal.stdout workdir* 
rm -rf dakota.rst dakota_mycal.in mycal.in
rm -rf  fort.* label.dat XINIB.dat bk7s2.dat ../reap data.dat reap/
hn=$(hostname); rm -rf $hn.*
rm -rf *.npy *.ppid

rm -rf orientate.in orientat.out
