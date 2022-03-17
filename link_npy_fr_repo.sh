#! /bin/bash

repo_bk='/home/tlyoon/dakota/dakota-gmt/data_generation/v2/record_small/data_repo_bk'
wd='/home/tlyoon/dakota/dakota-gmt/data_generation/v2/record_small/data_train/data_repo'
dirs=$(ls -l $repo_bk | grep '^d' | awk '{print $9}')
echo 'dirs:' $dirs
for i in $dirs:
	do
		i=$(echo $i | awk -F":" '{print $1}')
		cd $wd
		echo $wd '$i:' $i
		f1=$(ls  $repo_bk/$i | grep '_c_' | awk 'NR==1 {print $1}')
		f2=$(ls  $repo_bk/$i | grep '_c_' | awk 'NR==2 {print $1}')
		#echo 'ln -s' $repo_bk/$i/$f1 '.'
		#ls $repo_bk/$i/$f1 
		#echo 'ln -s' $repo_bk/$i/$f2 '.'
		#ls $repo_bk/$i/$f2 

		if [ ! -e $f1 ];
		then
			zero=0
		#	unlink $f1 
			ln -s $repo_bk/$i/$f1 '.'
		fi

        if [ ! -e $f2 ];
        then
			zero=0
		#	unlink $f2
			ln -s $repo_bk/$i/$f2 '.'
        fi
		echo ''
	done
