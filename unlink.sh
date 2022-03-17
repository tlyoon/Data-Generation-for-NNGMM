#! /bin/bash

dirs=$(ls *.npy)
for i in $dirs
	do 			
		echo $i
	echo 'unlink '$i
	unlink $i
	done
