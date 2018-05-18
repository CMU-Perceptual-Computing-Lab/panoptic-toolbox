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

