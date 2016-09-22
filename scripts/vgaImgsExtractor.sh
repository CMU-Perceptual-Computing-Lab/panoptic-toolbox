#!/bin/bash

# This extracts PNG files from VGA videos
# It should be run from the same directory containing the folder "vgaVideos"
# (E.g., sampleData/ )
# See http://domedb.perception.cs.cmu.edu

inputFolderName=vgaVideos
outputFolderName=vgaImgs
for p in {1..20}
	do
	for c in {1..24}
		do
		videoFileName=$(printf "$inputFolderName/vga_%02d_%02d.mp4" $p $c)
		outputvideoFileName=$(printf "$outputFolderName/%02d_%02d" $p $c)
		if [ -f $videoFileName ]; then
			mkdir -pv $outputvideoFileName
			echo "Generate Images from $videoFileName"
			fileName=$(printf "$outputvideoFileName/%02d_%02d_%%08d.png" $p $c) 
			ffmpeg -i $videoFileName -an -f image2 -start_number 0 "$fileName"
		else
			echo "$videoFileName (Skipping.)"
		fi
	done
done


