#! /bin/bash
#### note: must not echo anything other than existed to avoid upsetting the code because it is to be exported to bk7s2.dat
maxatomnumber=$(cat data.dat | awk '{print $8}')
wl=$(cat bk7s2.k | awk 'FNR==1')
natom=$(cat bk7s2.k | awk 'FNR==2')
Rem=$(cat bk7s2.k | awk 'FNR==3 {print $5}')
Imm=$(cat bk7s2.k | awk 'FNR==3 {print $6}')
cat bk7s2.k | awk 'NR>=3 {print $1, $2, $3, $4}' 
for (( j=$(( $natom + 1 )); j<=$maxatomnumber; j++ ))
do
	echo 0 0 0 0
done
echo $natom   $wl    $Rem    $Imm

