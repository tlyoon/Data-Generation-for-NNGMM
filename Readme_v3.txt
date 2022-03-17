This version (ver 3) is similar to version 2. The difference is that the algorithm to generate random configurations has been improved. In this version, the configurations generated are supposed to have avoided the problem of overlapping radius plagued by version 2. This shall result in a more efficient yield of configuration data that do not lead to 'none convergence' issues when evaluated by gmt. 


READ ME  version 2
==================

Codes in this folder is meant to generate dataset config.npy, lable.npy by gmt based on random configurations. These dataset are to be used as training and inference data to train neural network representation of the gmt calculator. 

1. The configuration for particle aggregates of various size N ranging from 2 to nLp at fixed wavelength. These data are compactly appended to config.npy. Each block of configuration has a dimension of (nLp+2) row x 3 column, with the format


x1(1) x2(1) x3(1) x4(1) 	<- coordinates and radius of particle 1
x1(2) x2(2) x3(2) x4(2) 	<- coordinates and radius of particle 2
...
x1(N) x2(N) x3(N) x4(N) 	<- coordinates and radius of particle N (the last particle)
0     0     0     0     	<- zeros for row N+1
0     0     0     0     	<- zeros for row N+2
...
0     0     0     0     	<- zeros for row nLp  
$N    $wl   $Rem    $Imm  	<- Number of particles, wavelength, Real(reflective index), Im(reflective index)

Each of this block will be reshaped into a row vector of shape 1 x (4*nLp + 4). Each row vector will be in turn appended into reap/config.npy. If a total of Nc configurations are generated, the dimension of config.py will be Nc x (4*nLp + 4).

For the special case of nLp=100, the shape of config.npy would be (Nc row x 404 column), where Ndat is the number of random gmt samples (say 10^6 or more). 404 column refers to 4*100 + 4 = 404.


2. The Cext for each corresponding configuration as calculated by gmmf0 will be appended to reap/label.npy. The dimension with reap/label.npy is a column vector of dimension Nc x 1. 


HOW TO USE THE CODE
===================

Data of gmt output in the form of reap/config.npy and reap/label.npy in the current directory will be accumulated by using the script in this package. To use the script:

0. Duplicate the template/ directory and name it, e.g., projectX:
	
	cp -r template projectX
	cd projectX

1. Edit the parameters in gen_gmt_npy.sh

2. Launch the code ./launch_local.sh in a local computer node, say compute-0-21.

3. A couple of directories named with the format $hostname.1/, $hostname.2/ ... will appear within projectX/. The number of such directories is $nproc-1, where $nproc is the number of cpu thread in the computer node where launch_local.sh is launched. 

4. gmt will generate many random sample and save them in the current directory in the form of config.npy and label.npy.

5. To speed up the accumulation of gmt data, repeat step 2 in another computer node (e.g., ssh compute-0-27) which has a nfs shared directory of projectX. Wihtout editing the content of gen_gmt_npy.sh, launch the code ./launch_local.sh in compute-0-27. A couple of new directories in addition to the ones in step 3 will be generated within projectX/. 

6. These directories will generate samples of gmt data in a parallel manner, saving the gmd data samples in separate sub-dictories c21.1, c21.2, c21.3, ...,c21.8, c22.1, c22.2, c22.3,..., c22.8. 

7. Reap all the data in the label.npy and config.npy files in all sub-dictories c21.1, c21.2,c21.3, ...,c21.8, c22.1,c22.2,c22.3,...,c22.8 by using the code reap_npy.py.

	python reap_npy.py

will append all label.npy and config.npy from all sub-directories into reap/config.npy and reap/label.npy.

