# !/bin/bash
# This extracts image files from HD videos
# It should be run from the same directory containing the folder "hdVideos"
# (E.g., sampleData/ )
# It takes an optional parameter specifying the output format (png or jpg)
# See http://domedb.perception.cs.cmu.edu

fmt=${1-jpg}

inputFolderName=kinectVideos
outputFolderName=kinectImgs
camIdx=-1;
for p in 50
	do
	for c in $(seq 1 10)
		do
		videoFileName=$(printf "$inputFolderName/kinect_%02d_%02d.mp4" $p $c)
		outputvideoFileName=$(printf "$outputFolderName/%02d_%02d" $p $c)
        echo $videoFileName
        echo $outputvideoFilename
        if [ -d  $outputvideoFileName ]; then
        		echo "Already extracted in: $outputvideoFileName";
        		continue;
        fi
		if [ -f $videoFileName ] && [ ! -d  $outputvideoFileName ]; then
		
			mkdir -pv $outputvideoFileName
			echo "Generate Images from $videoFileName"
			fileName=$(printf "$outputvideoFileName/%02d_%02d_%%08d.${fmt}" $p $c) 
			echo fileNameFormat: $fileName
			ffmpeg -i $videoFileName -q:v 1 -f image2 -start_number 1 "$fileName"  #1-based to be same as Matlab
		else
			echo "$videoFileName (File is missing: $videoFileName)"
		fi
	done
done


