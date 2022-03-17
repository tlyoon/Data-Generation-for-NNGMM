#! /bin/bash

rm -rf reap/
rm -rf *.ppid
comdir=$(for i in $(ls -d */); do echo ${i%%/}; done | grep "\.")
for i in $comdir
do
        rm -rf $i
        echo $i removed
done

nproc=$(cat /proc/cpuinfo | grep processor | awk -F':' 'END {print $2 }')
nproc=$(( $nproc  ))
#echo nproc $nproc

hostname=$(hostname)
#echo $hostname
for (( j=1; j<=$nproc; j++ ))
do
dirname=$hostname.$j
mkdir $dirname
cd $dirname
ln -s ../*.py .
ln -s ../*.f90 .
ln -s ../gmm01f* .
unlink gmm01f
cp ../gmm01f . ; chmod +x gmm01f
ln -s ../*.sh .
nohup ./gen_gmt_npy.sh &
PID=$!
echo $PID > ../$PID.ppid
cd  ../
done

# wait
ppid=$(ls *.ppid | awk -F".ppid" '{print $1}')
for i in $ppid:
do
        echo 'wait for ' $i
        wait $i
done

python reap_npy.py
fni=$(ls reap | awk '{print}' | awk -F"config." '{print $2}' | awk '$1 !="" {print}')
cd reap
cp ../clean_config.py .
cp ../rename_data.py .

f=clean_config.py

find=$'Xte=\'config.1130@cws.npy\''
replace=$'Xte=\'config.'$fni$'\''
echo $find 
echo $replace
sed -i "s|${find}|${replace}|g" $f

find=$'Yte=\'label.1130@cws.npy\''
replace=$'Yte=\'label.'$fni$'\''
echo $find 
echo $replace
sed -i "s|${find}|${replace}|g" $f

python clean_config.py
python rename_data.py

cp ../check_dim.py .
python check_dim.py

ac=$(hostname | awk '{ print substr($0, length($0)-1) }')

lastno=$(ls ~/dakota/dakota-gmt/data_generation/data_repo_bk | grep $ac | awk -F"@" '{print $1}' | awk -F"p" '{print $2}' | sort -n | awk 'END {print}')

index=$(( $lastno + 1 ))
hni='p'$index'@c'$(hostname | awk '{ print substr($0, length($0)-1) }')

cd ../
rm -rf $hni
mkdir $hni
cd $hni
#ln -s ../reap/*.npy .
mv ../reap/*.npy .
cd ..
scp -r "$hni" 10.205.19.225:~/dakota/dakota-gmt/data_generation/data_repo_bk/
wait
#~/dakota/dakota-gmt/data_generation/v3/template/link_npy_fr_repo.sh

