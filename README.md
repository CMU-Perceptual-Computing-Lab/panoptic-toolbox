PanopticStudio Toolbox
======================

This repository shows how to work with the [Panoptic Studio](http://domedb.perception.cs.cmu.edu) (Panoptic) data.

## Quick start guide
Follow these steps to set up a simple example:

### 1. Check out the codebase
```
git clone https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox
cd panoptic-toolbox
```

### 2. Download the sample data
This bash script requires curl or wget.
```
./scripts/getData.sh sampleData
```

You can also download any other seqeunce through this script. Just use the the name of the target sequence instead of the "sampleData". 
```
./scripts/getData.sh 160422_ultimatum
```

You can also specify the number of videos you want to donwload. 
```
./scripts/getData.sh sampleData (VGA_Video_Number) (HD_Video_Number)
```

For example, the following command will download 240 vga videos and 10 videos.  
```
./scripts/getData.sh sampleData 240 10
```

Note that we have sorted the VGA camera order so that you download uniformly distributed view. 


### 3. Extract the images & skeleton data
This step requires [ffmpeg](https://ffmpeg.org/).
```
./scripts/extractAll.sh sampleData
```
This will extract images, for example `sampleData/vgaImgs/01_01/01_01_00000000.png`, and the corresponding 3D skeleton data, for example `sampleData/vgaPose3d_stage1/body3DScene_00000000.json`.

`extractAll.sh` is a simple script that combines the following set of commands (you shouldn't need to run these again):
```bash
cd sampleData
../scripts/vgaImgsExtractor.sh # PNG files from VGA video (25 fps)
../scripts/hdImgsExtractor.sh # PNG files from HD video (29.97 fps)
tar -xf vgaPose3d_stage1.tar # Extract skeletons at VGA framerate
tar -xf hdPose3d_stage1.tar # Extract skeletons for HD
cd ..
```

### 4. Run the examples
Python examples (require numpy, matplotlib):
```
cd python
jupyter notebook example.ipynb
```
The result should look like [this](https://github.com/CMU-Perceptual-Computing-Lab/panopticapi_d/blob/master/python/example.ipynb).

Matlab example:
```matlab
>>> cd matlab
>>> demo
```


KinopticStudio Toolbox
======================

Kinoptic Studio is a subsystem of Panoptic Studio, which is composed of 10 Kinect2 sensors. 

Kinoptic Studio can be independently used from the Panoptic Studio.

See our [PtCloudDB document](http://domedb.perception.cs.cmu.edu/ptclouddb.html) for more details

## Quick start guide
Follow these steps to set up a simple example:


### 1. Download a data

Assuming you want to donwload a sequence named "160422_haggling1"

```
./scripts/getData_kinoptic.sh 160422_haggling1
```

This script will download the following files. 

* 160422_haggling1/kinect_shared_depth/ksynctables.json   #sync table
* 160422_haggling1/kinect_shared_depth/KINECTNODE%d/depthdata.dat  #depth files
* 160422_haggling1/kcalibration_160422_haggling1.json #multiple kinects calibration files
* 160422_haggling1/kinectVideos/kinect_50_%d.mp4 #rgb video files


### 2. Extract RGB frames

```
cd 160422_haggling1
../scripts/kinectImgsExtractor.sh
```

### 3. Run demo to generate point clouds from 10 kinects

```
matlab ./matlab/demo_kinoptic_gen_ptcloud.m
```

Note that you should set your "root_path" and "seqName" in this demo file. 



### 4. Run demo to project point clouds on a HD view

```
matlab ./matlab/demo_kinoptic_projection.m
```

Similarly, note that you should set your "root_path" and "seqName" in this demo file. 


## Panoptic 3D PointCloud DB ver.1
You can download all sequences included in our [3D PointCloud DB ver.1](https://docs.google.com/spreadsheets/d/1MsD9ioWBToHWz0E33gzFS5nDDjVHRECE2bZ1vM1ff_I/edit?usp=sharing) using the following script:

```
./scripts/getDB_ptCloud_ver1.sh
```



