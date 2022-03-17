#! /bin/bash

rm -rf reap/

hostname=$(hostname)

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

