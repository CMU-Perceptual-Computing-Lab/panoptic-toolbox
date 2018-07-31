#!/bin/bash

curPath=$(dirname "$0")

#Range of motion sequences
$curPath/getData_kinoptic.sh 171204_pose1
$curPath/getData_kinoptic.sh 171204_pose2
$curPath/getData_kinoptic.sh 171204_pose3
$curPath/getData_kinoptic.sh 171204_pose4
$curPath/getData_kinoptic.sh 171204_pose5
$curPath/getData_kinoptic.sh 171204_pose6
$curPath/getData_kinoptic.sh 171026_pose1
$curPath/getData_kinoptic.sh 171026_pose2
$curPath/getData_kinoptic.sh 171026_pose3

#Musical Instruments
$curPath/getData_kinoptic.sh 171026_cello1
$curPath/getData_kinoptic.sh 171026_cello2
$curPath/getData_kinoptic.sh 171026_cello3
$curPath/getData_kinoptic.sh 161029_flute1
$curPath/getData_kinoptic.sh 161029_piano1
$curPath/getData_kinoptic.sh 161029_piano2
$curPath/getData_kinoptic.sh 161029_piano3
$curPath/getData_kinoptic.sh 161029_piano4
$curPath/getData_kinoptic.sh 160906_band1
$curPath/getData_kinoptic.sh 160906_band2
$curPath/getData_kinoptic.sh 160906_band3

#SocialGame sequences
$curPath/getData_kinoptic.sh 160422_ultimatum1
$curPath/getData_kinoptic.sh 160226_ultimatum1
$curPath/getData_kinoptic.sh 160224_ultimatum1
$curPath/getData_kinoptic.sh 160224_ultimatum2
$curPath/getData_kinoptic.sh 160422_mafia2
$curPath/getData_kinoptic.sh 160226_mafia1
$curPath/getData_kinoptic.sh 160226_mafia2
$curPath/getData_kinoptic.sh 160224_mafia1
$curPath/getData_kinoptic.sh 160224_mafia2
$curPath/getData_kinoptic.sh 160422_haggling1
$curPath/getData_kinoptic.sh 160226_haggling1
$curPath/getData_kinoptic.sh 160224_haggling1

#Dance sequences
$curPath/getData_kinoptic.sh 170307_dance1
$curPath/getData_kinoptic.sh 170307_dance2
$curPath/getData_kinoptic.sh 170307_dance3
$curPath/getData_kinoptic.sh 170307_dance4
$curPath/getData_kinoptic.sh 170307_dance5
$curPath/getData_kinoptic.sh 170307_dance6
$curPath/getData_kinoptic.sh 160317_moonbaby1
$curPath/getData_kinoptic.sh 160317_moonbaby2
$curPath/getData_kinoptic.sh 160317_moonbaby3

#Toddler sequences
$curPath/getData_kinoptic.sh 170915_toddler2
$curPath/getData_kinoptic.sh 170915_toddler3
$curPath/getData_kinoptic.sh 170915_toddler4
$curPath/getData_kinoptic.sh 160906_ian5
$curPath/getData_kinoptic.sh 160906_ian3
$curPath/getData_kinoptic.sh 160906_ian2
$curPath/getData_kinoptic.sh 160906_ian1
$curPath/getData_kinoptic.sh 160401_ian3
$curPath/getData_kinoptic.sh 160401_ian2
$curPath/getData_kinoptic.sh 160401_ian1

#Others sequences
$curPath/getData_kinoptic.sh 170915_office1
$curPath/getData_kinoptic.sh 170407_office2
$curPath/getData_kinoptic.sh 160906_pizza1

