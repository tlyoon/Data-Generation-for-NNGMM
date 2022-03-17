#! /bin/bash

dirs=$(ls -d */)
for i in $dirs
	do 	
		cd $i	
		ll=$(ls *label*_b*  | grep 'npy')
		lc=$(ls *config*_b*)
		echo ln -s "$PWD"/$ll /home/tlyoon/dakota/dakota-gmt/data_generation/data_test/
		#echo ln -s "$PWD"/$lc /home/tlyoon/dakota/dakota-gmt/data_generation/data_test/
		ln -s "$PWD"/$ll /home/tlyoon/dakota/dakota-gmt/data_generation/data_test/
		#ln -s "$PWD"/$lc /home/tlyoon/dakota/dakota-gmt/data_generation/data_test/
		cd ../
	echo ''
	done
