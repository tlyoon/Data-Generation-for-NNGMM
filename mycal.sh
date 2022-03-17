#! /bin/bash

gfortran multiply.f90
nlast=$(cat mycal.in | awk 'END {print NR-1}')
#echo 'nlast:' $nlast
d1=$(( $nlast - 27 + 1 ))
totalatomnumber=$(printf "%.0f\n" $(cat mycal.in | awk -v nlast=$nlast 'NR==nlast {print $3}' ))
xx=$(cat mycal.in | awk -v nlast=$nlast 'NR>=27 && NR <= nlast {print}' | awk '{print $3}')
rm -rf XINIB.dat
for (( i=1; i<=$totalatomnumber; i++ ))
do  
	for (( j=1; j<=4; j++ ))
	do
	index=$(( (( 4*(( $i-1 )) )) + $j ))
	#echo 'i,j,index' $i $j $index
	xx[$j]=$(cat mycal.in | awk -v nlast=$nlast -v ind=$index 'NR==(27+ind-1) && NR <= nlast {print}' | awk '{print $3}')
	done 
	echo ${xx[1]} ${xx[2]} ${xx[3]} ${xx[4]} real imaginary >> XINIB.dat
done
###

nwl=$(cat data.dat | awk '{print $1}') ## random positive interger, >= 2, number of wavelength, for trouble shooting set to 32 #####
wllo=$(cat data.dat | awk '{print $2}')  ## random positive float, lower limit of wavelength
wlhi=$(cat data.dat  | awk '{print $3}')  ## random positive float, lower limit of wavelength
relo=$(cat data.dat | awk '{print $4}')  ## random positive float, lower limit of Re(m)
rehi=$(cat data.dat  | awk '{print $5}')  ## random positive float, upper limit of Re(m)
imlo=$(cat data.dat | awk '{print $6}')  ## random positive float, lower limit of Re(m)
imhi=$(cat data.dat  | awk '{print $7}')  ## random positive float, upper limit of Re(m)

i=1
while [ $i -le $nwl ]
do
 random=$( printf "0.%03d\n" $(( RANDOM % 1000000 )) )
 wl=$(echo $wllo $wlhi $random | awk '{print $1+($2-$1)*$3}')
 random=$( printf "0.%03d\n" $(( RANDOM % 1000000 )) )
 re=$(echo $relo $rehi $random | awk '{print $1+($2-$1)*$3}')
 random=$( printf "0.%03d\n" $(( RANDOM % 1000000 )) )
 im=$(echo $imlo $imhi $random | awk '{print $1+($2-$1)*$3}') 
 echo '$i $wl $re $im: ' $i $wl $re $im 
 echo $wl > temp1
 echo $totalatomnumber >> temp1
 cat  temp1 XINIB.dat > temp2
 rm -rf temp1
 #cat temp2
 #rm -rf temp1 temp2
 sed -i -e "s/wavelength/$wl/g" temp2
 sed -i -e "s/real/$re/g" temp2
 sed -i -e "s/imaginary/$im/g" temp2
 mv temp2 bk7s2.k
 #echo 'bk7s2.k:' 
 #cat bk7s2.k
 rm -rf temp2
 rm -rf gmm01f.out
 ./gmm01f > /dev/null 2>&1
 if [ -f gmm01f.out ]; then 
	echo "$(awk 'FNR==5 { print $2 }' gmm01f.out) " > label.dat
	./sort_bk7s2.sh > bk7s2.dat
	## call python script to append bk7s2.dat into config.npy and label.dat into label.npy
	python bk7s2.py
	##
 else
	echo 'gmm01f.out is absent. Non-convergence occurs.'
	echo "-99999" > label.dat
	./sort_bk7s2.sh > bk7s2.dat
	## call python script to append bk7s2.dat into config.npy and label.dat into label.npy
	python bk7s2.py
 fi
 i=$[$i+1]
done
rm -rf a.out XINIB.dat bk7s2.k 
#label.dat 
#bk7s2.dat *.out 

