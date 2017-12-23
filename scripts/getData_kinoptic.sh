#!/bin/bash

# This script downloads videos for a specific sequence:
# ./getData.sh [sequenceName] [numVGAViews] [numHDViews]
#
# e.g., to download 10 VGA camera views for the "sampleData" sequence:
# ./getData.sh sampleData 10 0
# 

datasetName=${1-sampleData}
numKinectViews=${2-10} #Specify the number of vga views you want to donwload. Up to 480

# Select wget or curl, with appropriate options
if command -v wget >/dev/null 2>&1; then 
	WGET="wget -c"
	mO="-O"
elif command -v curl >/dev/null 2>&1; then
	WGET="curl -C -" 
	mO="-o"
else
	echo "This script requires wget or curl to download files."
	echo "Aborting."
	exit 1;
fi

# Each sequence gets its own subdirectory
mkdir $datasetName		
cd $datasetName

# Download panoptic calibration data
$WGET $mO calibration_${datasetName}.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$datasetName/calibration_${datasetName}.json

# Download kcalibration data
$WGET $mO kcalibration_${datasetName}.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$datasetName/kinect_shared_depth/kcalibration_${datasetName}.json

# Download synctabls data
$WGET $mO synctables_${datasetName}.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$datasetName/kinect_shared_depth/synctables.json
$WGET $mO ksynctables_${datasetName}.json http://domedb.perception.cs.cmu.edu/webdata/dataset/$datasetName/kinect_shared_depth/ksynctables.json


#####################
# Download kinect rgb videos
#####################
mkdir -p kinectVideos
panel=50
nodes=(1 2 3 4 5 6 7 8 9 10)
for (( c=0; c<$numKinectViews; c++))
do
  fileName=$(printf "kinectVideos/kinect_%02d_%02d.mp4" ${panel} ${nodes[c]})
  echo $fileName;
  #Download and delete if the file is blank
	#cmd=$(printf "$WGET $mO kinectVideos/kinect_%02d_%02d.mp4 http://domedb.perception.cs.cmu.edu/webdata/dataset/$datasetName/videos/kinect_shared_crf0/${datasetName}_kinect%d.mp4 || rm -v $fileName" ${panel} ${nodes[c]} ${nodes[c]})
	cmd=$(printf "$WGET $mO kinectVideos/kinect_%02d_%02d.mp4 http://domedb.perception.cs.cmu.edu/webdata/dataset/$datasetName/videos/kinect_shared_crf20/${datasetName}_kinect%d.mp4 || rm -v $fileName" ${panel} ${nodes[c]} ${nodes[c]})
	echo $cmd
	eval $cmd
done

#####################
# Download kinect depth videos
#####################
mkdir -p kinect_shared_depth
nodes=(1 2 3 4 5 6 7 8 9 10)
for (( c=0; c<$numKinectViews; c++))
do
  subfolder=$(printf "kinect_shared_depth/KINECTNODE%d" ${nodes[c]})
  mkdir $subfolder;
  fileName=$(printf "kinect_shared_depth/KINECTNODE%d/depthdata.dat" ${nodes[c]})
  echo $fileName;
  #Download and delete if the file is blank
	cmd=$(printf "$WGET $mO $fileName http://domedb.perception.cs.cmu.edu/webdata/dataset/$datasetName/$fileName || rm -v $fileName")
	echo $cmd
	eval $cmd
done

