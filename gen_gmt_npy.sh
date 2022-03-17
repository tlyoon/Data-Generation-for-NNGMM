#! /bin/bash

# Use this script to generate *.npy data of the configuration a random number of particles in a cubic box and the corresponding Cext calculated via gmmf

# The following quantities are required: 
# 1 maxatomnumber (a positive integer representing the maximun possible number of particles in the system). 
# 2 radius, (seed radius of the atoms, a positive float in an assumed length unit)
# 3 boxlength (defined as $blr*radius*$maxatomnumber )
# 4 totalround (number of round to generate. Defined via totalround=Nroundfactor*maxatomnumber)
# 5 nwl (number of wavelength, large positive integer)
# 6 wllow,wlhi (lower limit of wavelength, upper limit of wavelength)
###############

Nroundfactor=60         ### integer. totalround=$(( $Nroundfactor*$maxatomnumber )) default: 100
nwl=75                 ### integer. Define the number of randomly chosen wavelength. default: 250
			### 50 for TB
maxatomnumber=10  	### integer, small default:10. large default:100
radius=1.0              ### float, baseline (seed) radius reference value. small default:1.0
blr=1.5		        ### float, factor to be multiplied when defining boxlength. small default:1.5
wllow=50                ### float. in unit of nm. lower limit of wavelength range. small default: 50
wlhi=100	    	### float. in unit of nm. upper limit of wavelength range. small default: 100
relow=0.1		### no unit. lower limit of Real(refractive index). small default: 0.001
rehi=1.0   		### no unit. upper limit of Real(refractive index). small default: 1.0
imlow=0.1 		### no unit. lower limit of Im(refractive index). small default: 0.1 
imhi=1.0		### no unit. upper limit of Im(refractive index). small default: 1.0 

#### do not touch anything below this line #############
echo $nwl $wllow $wlhi $relow $rehi $imlow $imhi $maxatomnumber > data.dat

#totalround=3 						### For TS
totalround=$(( $Nroundfactor*$maxatomnumber ))    	### for production

### for seed radius #
factor_deltar=0.99 ### limit factor_deltar to be less than one to avoid occurance of negative radius
fdeltar=$(echo $factor_deltar $radius | awk '{print $1*$2}')
rlo=$(echo $radius $fdeltar | awk '{print $1-$2}')
rhi=$(echo $radius $fdeltar | awk '{print $1+3*$2}')   ##### maximum possible radius
deletarr=$(echo $rhi $rlo | awk '{print $1-$2}')
### end for seed radius #

boxlength=$(echo $rhi $maxatomnumber $blr | awk '{print (2*$1)*$2*$3}') ## default: diameter x maxatomnumber x $blr
xlo=$(echo $boxlength | awk '{print -0.5*$1}')
xhi=$(echo $boxlength | awk '{print 0.5*$1}')
ylo=$xlo; yhi=$xhi;

zlo=$xlo; zhi=$xhi

deltax=$(echo "$xhi $xlo" | awk '{print $1-$2}')
deltay=$(echo "$yhi $ylo" | awk '{print $1-$2}')
deltaz=$(echo "$zhi $zlo" | awk '{print $1-$2}')

LOW=2;HIGH=$maxatomnumber;

for (( round=1; round<="$totalround"; round++ ))
do
	rm -rf XINIB.dat temp1.dat temp2.dat temp3.dat temp4.dat orientate.in
	echo 'round:' $round
	
	### generate random integer between 2 - 100 
	ranint=$(echo $((RANDOM * ($HIGH-$LOW+1) / 32768 + LOW)))
	echo '$ranint:' $ranint
	### end generate random integer between 2 - 100 

	xgap=$(echo $boxlength $ranint $rhi | awk '{print $1-2*$2*$3}')
	xlop=$(echo $xlo $xgap | awk '{print $1+$2}')
	#echo '$xlo,$xhi,$boxlength,$xgap,$xlop' $xlo $xhi $boxlength $xgap $xlop
		
	for (( i=1; i<=$(( $ranint )); i++ ))
	do  
		#### generate radius ###
		random=$( printf "0.%03d\n" $(( RANDOM % 1000 )) )
		#deletarr=$(echo $rhi $rlo | awk '{print $1-$2}')
		rradius=$(echo $rlo $deletarr $random | awk '{print $1+$2*$3}')
		a=$(echo $rradius | awk '{print 2*$1/sqrt(3)}')
	#	echo 'i, rradius, a' $i $rradius $a
		
		for (( j=1; j<=4; j++ ))
		do
		index=$(( (( 4*(( $i-1 )) )) + $j ))
		
		if [ $j -eq 1 ]; then
			random=$( printf "0.%03d\n" $(( RANDOM % 1000000 )) )
			if [ $i -eq 1 ]; then
				xi[1]=$(echo $xlo+$random*$xgap | bc)
			else
				xi[$i]=$(echo ${xi[$i-1]}+$a+$random*a | bc)
			fi
			x[$index]=${xi[$i]}
			#echo 'i,j,index,x[$index],${xi[$i]}' $i $j $index ${x[$index]} ${xi[$i]}
		fi
		
		if [ $j -eq 2 ]; then
			random=$( printf "0.%03d\n" $(( RANDOM % 1000000 )) )
			if [ $i -eq 1 ]; then
				yi[1]=$(echo $xlo+$random*$xgap | bc)
			else
				yi[$i]=$(echo ${yi[$i-1]}+$a+$random*a | bc)
			fi
			x[$index]=${yi[$i]}
			#echo 'i,j,index,x[$index],${yi[$i]}' $i $j $index ${x[$index]} ${yi[$i]}
		fi
		
		if [ $j -eq 3 ]; then
			random=$( printf "0.%03d\n" $(( RANDOM % 1000000 )) )
			if [ $i -eq 1 ]; then
				zi[1]=$(echo $xlo+$random*$xgap | bc)
			else
				zi[$i]=$(echo ${zi[$i-1]}+$a+$random*a | bc)
			fi
			x[$index]=${zi[$i]}
			#echo 'i,j,index,x[$index],${zi[$i]}' $i $j $index ${x[$index]} ${zi[$i]}
		fi

	###### include radius as a parameter to tune #####	
		if [ $j -eq 4 ]; then
#		random=$( printf "0.%03d\n" $(( RANDOM % 1000 )) )
#		deletarr=$(echo $rhi $rlo | awk '{print $1-$2}')
#		x[$index]=$(echo $rlo $deletarr $random | awk '{print $1+$2*$3}')
		x[$index]=$rradius
		fi
	###### end of include radius as a parameter to tune #####
		#echo 'i:',$i, 'index:' $index 'j:' $j, 'x[$index]:', ${x[$index]}
		#echo $i $index $j ${x[$index]} >> orientate.in
		done  
	done ### for i
	
	#### stretching ####
	xilast=${xi[$ranint]};yilast=${yi[$ranint]};zilast=${zi[$ranint]}
	fx=$(echo $boxlength $xilast $xlo | awk '{print ($1-$2)/($2-$3)}')
	fy=$(echo $boxlength $yilast $xlo | awk '{print ($1-$2)/($2-$3)}')
	fz=$(echo $boxlength $zilast $xlo | awk '{print ($1-$2)/($2-$3)}')
	#echo ''
	#echo '$xilast $yilast $zilast' $xilast $yilast $zilast
	for (( i=1; i<=$(( $ranint )); i++ ))
	do  		
		for (( j=1; j<=4; j++ ))
		do
		index=$(( (( 4*(( $i-1 )) )) + $j ))
		
		if [ $j -eq 1 ]; then
			#echo 'before: i,j,index,x[$index]' $i $j $index ${x[$index]}
			x[$index]=$(echo ${x[$index]} $fx $xlo $boxlength | awk '{print $1*(1+$2)-$2*$3-0.5*$4}')
	#		echo 'after: i,j,x[$index]' $i $j $index ${x[$index]}
		fi
		
		if [ $j -eq 2 ]; then
			#echo 'before: i,j,index,x[$index]' $i $j $index ${x[$index]}
			x[$index]=$(echo ${x[$index]} $fy $xlo $boxlength | awk '{print $1*(1+$2)-$2*$3-0.5*$4}')
	#		echo 'after: i,j,$index,x[$index]' $i $j, $index ${x[$index]}
		fi
		
		if [ $j -eq 3 ]; then
			#echo 'before: i,j,index,x[$index]' $i $j, $index ${x[$index]}
			x[$index]=$(echo ${x[$index]} $fz $xlo $boxlength | awk '{print $1*(1+$2)-$2*$3-0.5*$4}')
	#		echo 'after: i,j,$index,x[$index]' $i $j $index ${x[$index]}
		fi

	###### include radius as a parameter to tune #####	
		if [ $j -eq 4 ]; then
#		random=$( printf "0.%03d\n" $(( RANDOM % 1000 )) )
#		deletarr=$(echo $rhi $rlo | awk '{print $1-$2}')
#		x[$index]=$(echo $rlo $deletarr $random | awk '{print $1+$2*$3}')
		x[$index]=$rradius
		fi
	###### end of include radius as a parameter to tune #####
		#echo 'i:',$i, 'index:' $index 'j:' $j, 'x[$index]:', ${x[$index]}
		echo $i $index $j ${x[$index]} >> orientate.in
	#	echo ''
		done
	done ### for i
	echo 'coordinates of all atoms stretched'
	#### end stretching ####
	
	##### reorientate here
	python orientate.py   > /dev/null  ### will generate orientate.out
	echo 'coordinates re-orientated'
	NR=$(cat orientate.out | awk 'END {print NR}')
	for (( i=1; i<=$(( $NR )); i++ ))
	do
        x[$i]=$(cat orientate.out | awk -v i=$i 'NR==i {print $4}')
	done		
	##### end reorientate here

	index1=$(( $index + 1 ))
	#echo 'last index' $index
	#echo 'NR' $NR
	#echo 'index1' $index1
	x[$index1]=$ranint

	totalcoordinate=$(echo $maxatomnumber*4 + 1 | bc)
	rm -rf temp.dat
	echo '** total number of varaibles' >> temp.dat
	echo '** data begins from line 27 and onwards' >> temp.dat
	echo '** the rest are all dummies' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '** ' >> temp.dat
	echo '**' >> temp.dat

	#for (( c=1; c<=$(( $totalcoordinate )); c++ ))
	for (( c=1; c<=$(( $index1 )); c++ ))
	do
	#echo variable $c {x$c} >> temp.dat
	echo variable $c ${x[$c]} >> temp.dat
	#eval TMP="\$c"; echo variable $c \x{$TMP}\ >> temp.dat

	done
	echo end >> temp.dat
	mv temp.dat mycal.in
	nvar=$index1
	echo 'The variables specified are as follows: '
	echo 'max possible number of atom:' $maxatomnumber
	echo 'seed radius:' $radius 'min radius:' $rlo 'max radius:' $rhi; 
	echo 'blr = integer to be multipled when defining boxlength' $blr 
	echo 'boxlength:' $boxlength 'xlo:' $xlo 'xhi:' $xhi
	echo 'number of atoms:' $ranint
	echo 'total number of varaibles:' $nvar
	#echo 'variables:' 
	#echo ${x[@]}
	./mycal.sh
	echo 'round' $round 'has completed.'
	echo ''
done ### end for (( round=1; round<="$totalround"; round++ )) ; do
