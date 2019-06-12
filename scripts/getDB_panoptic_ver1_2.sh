#!/bin/bash

#This list is named as "Panoptic Studio DB Ver 1.2"

curPath=$(dirname "$0")
vgaVideoNum=0
hdVideoNum=0

#Range of motion sequences
$curPath/getData.sh 171204_pose1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171204_pose1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171204_pose2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171204_pose3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171204_pose4 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171204_pose5 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171204_pose6 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171026_pose1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171026_pose2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171026_pose3 $vgaVideoNum $hdVideoNum

#Download All Haggling Sequences without downloading videos
$curPath/getData.sh 170221_haggling_b1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170221_haggling_b2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170221_haggling_b3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170221_haggling_m1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170221_haggling_m2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170221_haggling_m3 $vgaVideoNum $hdVideoNum

$curPath/getData.sh 170224_haggling_a1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170224_haggling_a2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170224_haggling_a3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170224_haggling_b1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170224_haggling_b2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170224_haggling_b3 $vgaVideoNum $hdVideoNum

$curPath/getData.sh 170228_haggling_a1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170228_haggling_a2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170228_haggling_a3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170228_haggling_b1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170228_haggling_b2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170228_haggling_b3 $vgaVideoNum $hdVideoNum

$curPath/getData.sh 170404_haggling_a1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170404_haggling_a2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170404_haggling_a3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170404_haggling_b1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170404_haggling_b2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170404_haggling_b3 $vgaVideoNum $hdVideoNum

$curPath/getData.sh 170407_haggling_a1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170407_haggling_a2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170407_haggling_a3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170407_haggling_b1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170407_haggling_b2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170407_haggling_b3 $vgaVideoNum $hdVideoNum


#Musical Instruments
$curPath/getData.sh 171026_cello1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171026_cello2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 171026_cello3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 161029_flute1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 161029_piano1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 161029_piano2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 161029_piano3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 161029_piano4 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_band1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_band2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_band3 $vgaVideoNum $hdVideoNum

#SocialGame sequences
$curPath/getData.sh 160422_ultimatum1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160226_ultimatum1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160224_ultimatum1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160224_ultimatum2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160422_mafia2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160226_mafia1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160226_mafia2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160224_mafia1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160224_mafia2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160422_haggling1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160226_haggling1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160224_haggling1 $vgaVideoNum $hdVideoNum

#Dance sequences
$curPath/getData.sh 170307_dance1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170307_dance2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170307_dance3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170307_dance4 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170307_dance5 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170307_dance6 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160317_moonbaby1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160317_moonbaby2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160317_moonbaby3 $vgaVideoNum $hdVideoNum

#Toddler sequences
$curPath/getData.sh 170915_toddler2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170915_toddler3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170915_toddler4 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_ian5 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_ian3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_ian2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_ian1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160401_ian3 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160401_ian2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160401_ian1 $vgaVideoNum $hdVideoNum

#Others sequences
$curPath/getData.sh 170915_office1 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 170407_office2 $vgaVideoNum $hdVideoNum
$curPath/getData.sh 160906_pizza1 $vgaVideoNum $hdVideoNum

# #Extract Tar Files
$curPath/extractAll.sh	171204_pose1
$curPath/extractAll.sh	171204_pose2
$curPath/extractAll.sh	171204_pose3
$curPath/extractAll.sh	171204_pose4
$curPath/extractAll.sh	171204_pose5
$curPath/extractAll.sh	171204_pose6
$curPath/extractAll.sh	171026_pose1
$curPath/extractAll.sh	171026_pose2
$curPath/extractAll.sh	171026_pose3
	
$curPath/extractAll.sh	171026_cello1
$curPath/extractAll.sh	171026_cello2
$curPath/extractAll.sh	171026_cello3
$curPath/extractAll.sh	161029_flute1
$curPath/extractAll.sh	161029_piano1
$curPath/extractAll.sh	161029_piano2
$curPath/extractAll.sh	161029_piano3
$curPath/extractAll.sh	161029_piano4
$curPath/extractAll.sh	160906_band1
$curPath/extractAll.sh	160906_band2
$curPath/extractAll.sh	160906_band3
	
	
$curPath/extractAll.sh	160422_ultimatum1
$curPath/extractAll.sh	160226_ultimatum1
$curPath/extractAll.sh	160224_ultimatum1
$curPath/extractAll.sh	160224_ultimatum2
$curPath/extractAll.sh	160422_mafia2
$curPath/extractAll.sh	160226_mafia1
$curPath/extractAll.sh	160226_mafia2
$curPath/extractAll.sh	160224_mafia1
$curPath/extractAll.sh	160224_mafia2
$curPath/extractAll.sh	160422_haggling1
$curPath/extractAll.sh	160226_haggling1
$curPath/extractAll.sh	160224_haggling1
	
$curPath/extractAll.sh	170221_haggling_b1
$curPath/extractAll.sh	170221_haggling_b2
$curPath/extractAll.sh	170221_haggling_b3
$curPath/extractAll.sh	170221_haggling_m1
$curPath/extractAll.sh	170221_haggling_m2
$curPath/extractAll.sh	170221_haggling_m3
$curPath/extractAll.sh	170224_haggling_a1
$curPath/extractAll.sh	170224_haggling_a2
$curPath/extractAll.sh	170224_haggling_a3
$curPath/extractAll.sh	170224_haggling_b1
$curPath/extractAll.sh	170224_haggling_b2
$curPath/extractAll.sh	170224_haggling_b3
$curPath/extractAll.sh	170228_haggling_a1
$curPath/extractAll.sh	170228_haggling_a2
$curPath/extractAll.sh	170228_haggling_a3
$curPath/extractAll.sh	170228_haggling_b1
$curPath/extractAll.sh	170228_haggling_b2
$curPath/extractAll.sh	170228_haggling_b3
$curPath/extractAll.sh	170404_haggling_a1
$curPath/extractAll.sh	170404_haggling_a2
$curPath/extractAll.sh	170404_haggling_a3
$curPath/extractAll.sh	170404_haggling_b1
$curPath/extractAll.sh	170404_haggling_b2
$curPath/extractAll.sh	170404_haggling_b3
$curPath/extractAll.sh	170407_haggling_a1
$curPath/extractAll.sh	170407_haggling_a2
$curPath/extractAll.sh	170407_haggling_a3
$curPath/extractAll.sh	170407_haggling_b1
$curPath/extractAll.sh	170407_haggling_b2
$curPath/extractAll.sh	170407_haggling_b3
	
$curPath/extractAll.sh	170307_dance1
$curPath/extractAll.sh	170307_dance2
$curPath/extractAll.sh	170307_dance3
$curPath/extractAll.sh	170307_dance4
$curPath/extractAll.sh	170307_dance5
$curPath/extractAll.sh	170307_dance6
$curPath/extractAll.sh	160317_moonbaby1
$curPath/extractAll.sh	160317_moonbaby2
$curPath/extractAll.sh	160317_moonbaby3
	
$curPath/extractAll.sh	170915_toddler2
$curPath/extractAll.sh	170915_toddler3
$curPath/extractAll.sh	170915_toddler4
$curPath/extractAll.sh	160906_ian5
$curPath/extractAll.sh	160906_ian3
$curPath/extractAll.sh	160906_ian2
$curPath/extractAll.sh	160906_ian1
$curPath/extractAll.sh	160401_ian3
$curPath/extractAll.sh	160401_ian2
$curPath/extractAll.sh	160401_ian1
	
$curPath/extractAll.sh	170915_office1
$curPath/extractAll.sh	170407_office2
$curPath/extractAll.sh	160906_pizza1