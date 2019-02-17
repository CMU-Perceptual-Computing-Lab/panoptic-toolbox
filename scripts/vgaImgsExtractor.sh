#!/bin/bash

# This extracts image files from VGA videos
# It should be run from the same directory containing the folder "vgaVideos"
# (E.g., sampleData/ )
# It takes an optional parameter specifying the output format (png or jpg)
# See http://domedb.perception.cs.cmu.edu

fmt=${1-jpg}

inputFolderName=vgaVideos
outputFolderName=vgaImgs

# older version bash compatibility, for version greater than 4.1, it can be for p in {1..20}
for p in $(seq 1 20)
	do
	for c in $(seq 1 24)
		do
		videoFileName=$(printf "$inputFolderName/vga_%02d_%02d.mp4" $p $c)
		outputvideoFileName=$(printf "$outputFolderName/%02d_%02d" $p $c)
		if [ -f $videoFileName ]; then
			mkdir -pv $outputvideoFileName
			echo "Generate Images from $videoFileName"
			fileName=$(printf "$outputvideoFileName/%02d_%02d_%%08d.${fmt}" $p $c) 
			ffmpeg -i $videoFileName -q:v 1 -f image2 -start_number 0 "$fileName"
		#else
		#	echo "$videoFileName (Skipping.)"
		fi
	done
done


