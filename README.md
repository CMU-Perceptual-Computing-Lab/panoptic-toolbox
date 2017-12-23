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

See our [tutorial page](http://domedb.perception.cs.cmu.edu/tutorials/cvpr17/index.html) for more details about calibration and synchronization.

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

### 3. Run demo

```
matlab ./matlab/demo_kinoptic_gen_ptcloud.m
```

Note that you should set your "root_path" and "seqName" in this demo file. 


PanopticDB Toolbox
======================
PanopticDB is a database collected by Panoptic Studio.

## Quick start guide
Follow these steps to download and extract PanopticDB.


### 1. Download data

Assuming you want to donwload a sequence whose name contains substring "170221" in version "a2" (the current latest version) into the directory "./PanopticDB/"
```
./scripts/getPanopticDB.sh ./PanopticDB/ a2 170221
```

This script will download the following files. 

* ./PanopticDB/a2/annot_calib.tar.gz    # calibration data for all sequences
* ./PanopticDB/a2/annot_3dskeleton.tar.gz    # 3D annotation for all sequences
* ./PanopticDB/a2/annot_2dskeleton.tar.gz    # 2D annotation for all sequences
* ./PanopticDB/a2/sampleList.mat    # a Matlab data file containing data information
* ./PanopticDB/a2/imgs/170221_haggling_b3.tar.gz    # Image data for one sequence containing '170221' in the name
* ......    # And all other sequences containing '170221' in the name

In order to download all image sequence data, just omit the 3rd argument of the script.


### 2. Extract data from tars

```
./scripts/extractPanopticDB.sh ./PanopticDB/
```
The argument is set to the directory where the data are downloaded.

### 3. Run the Matlab demo

```matlab
>> cd matlab
>> demo_panopticdb
```
