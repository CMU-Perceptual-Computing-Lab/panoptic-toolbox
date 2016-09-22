#!/bin/bash
# Helper script to run other extraction tasks
if [ "$#" -ne 1 ]; then
	echo "This script takes 1 parameter, the path to the data directory, e.g.,"
	echo "./scripts/extractAll.sh ./sampleData" 
fi

# Figure out the path of helper scripts
DIR=$(dirname $(readlink -f $0))
OLDDIR=$PWD

cd $1

# Extract skeletons
if [ -f vgaPose3d_stage1.tar ]; then
	tar -xf vgaPose3d_stage1.tar
fi

if [ -f hdPose3d_stage1.tar ]; then
	tar -xf hdPose3d_stage1.tar
fi



# Extract VGA images
$DIR/vgaImgsExtractor.sh

# Extract HD images
$DIR/hdImgsExtractor.sh

cd $OLDDIR
