#!/bin/bash

curPath=$(dirname "$0")

#Download All Haggling Sequences without downloading videos
$curPath/getData.sh 170221_haggling_b1 0 0
$curPath/getData.sh 170221_haggling_b2 0 0
$curPath/getData.sh 170221_haggling_b3 0 0
$curPath/getData.sh 170221_haggling_m1 0 0
$curPath/getData.sh 170221_haggling_m2 0 0
$curPath/getData.sh 170221_haggling_m3 0 0


$curPath/getData.sh 170224_haggling_a1 0 0
$curPath/getData.sh 170224_haggling_a2 0 0
$curPath/getData.sh 170224_haggling_a3 0 0
$curPath/getData.sh 170224_haggling_b1 0 0
$curPath/getData.sh 170224_haggling_b2 0 0
$curPath/getData.sh 170224_haggling_b3 0 0

$curPath/getData.sh 170228_haggling_a1 0 0
$curPath/getData.sh 170228_haggling_a2 0 0
$curPath/getData.sh 170228_haggling_a3 0 0
$curPath/getData.sh 170228_haggling_b1 0 0
$curPath/getData.sh 170228_haggling_b2 0 0
$curPath/getData.sh 170228_haggling_b3 0 0

$curPath/getData.sh 170404_haggling_a1 0 0
$curPath/getData.sh 170404_haggling_a2 0 0
$curPath/getData.sh 170404_haggling_a3 0 0
$curPath/getData.sh 170404_haggling_b1 0 0
$curPath/getData.sh 170404_haggling_b2 0 0
$curPath/getData.sh 170404_haggling_b3 0 0

$curPath/getData.sh 170407_haggling_a1 0 0
$curPath/getData.sh 170407_haggling_a2 0 0
$curPath/getData.sh 170407_haggling_a3 0 0
$curPath/getData.sh 170407_haggling_b1 0 0
$curPath/getData.sh 170407_haggling_b2 0 0
$curPath/getData.sh 170407_haggling_b3 0 0

#Extract Tar Files
$curPath/extractAll.sh 170221_haggling_b1
$curPath/extractAll.sh 170221_haggling_b2
$curPath/extractAll.sh 170221_haggling_b3
$curPath/extractAll.sh 170221_haggling_m1
$curPath/extractAll.sh 170221_haggling_m2
$curPath/extractAll.sh 170221_haggling_m3

$curPath/extractAll.sh 170224_haggling_a1
$curPath/extractAll.sh 170224_haggling_a2
$curPath/extractAll.sh 170224_haggling_a3
$curPath/extractAll.sh 170224_haggling_b1
$curPath/extractAll.sh 170224_haggling_b2
$curPath/extractAll.sh 170224_haggling_b3

$curPath/extractAll.sh 170228_haggling_a1
$curPath/extractAll.sh 170228_haggling_a2
$curPath/extractAll.sh 170228_haggling_a3
$curPath/extractAll.sh 170228_haggling_b1
$curPath/extractAll.sh 170228_haggling_b2
$curPath/extractAll.sh 170228_haggling_b3

$curPath/extractAll.sh 170404_haggling_a1
$curPath/extractAll.sh 170404_haggling_a2
$curPath/extractAll.sh 170404_haggling_a3
$curPath/extractAll.sh 170404_haggling_b1
$curPath/extractAll.sh 170404_haggling_b2
$curPath/extractAll.sh 170404_haggling_b3

$curPath/extractAll.sh 170407_haggling_a1
$curPath/extractAll.sh 170407_haggling_a2
$curPath/extractAll.sh 170407_haggling_a3
$curPath/extractAll.sh 170407_haggling_b1
$curPath/extractAll.sh 170407_haggling_b2
$curPath/extractAll.sh 170407_haggling_b3