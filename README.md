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

### 2. Download a sample data and other data
To download a dataset, named "171204_pose1_sample" in this example, run the following script.
```
./scripts/getData.sh 171204_pose1_sample
```

This bash script requires curl or wget.


This script will create a folder "./171204_pose1_sample" and download the following files.

* 171204_pose1_sample/hdVideos/hd_00_XX.mp4  #synchronized HD video files (31 views)
* 171204_pose1_sample/vgaVideos/KINECTNODE%d/vga_XX_XX.mp4 #synchrponized VGA video files (480 views)
* 171204_pose1_sample/calibration_171204_pose1_sample.json #calibration files
* 171204_pose1_sample/hdPose3d_stage1_coco19.tar #3D Body Keypoint Data (coco19 keypoint definition)
* 171204_pose1_sample/hdFace3d.tar #3D Face Keypoint Data 
* 171204_pose1_sample/hdHand3d.tar #3D Hand Keypoint Data 

Note that this sample example currently does not have VGA videos.

You can also download any other seqeunce through this script. Just use the the name of the target sequence instead of the "171204_pose1_sample". 

For example, 

```
./scripts/getData.sh 171204_pose1
```

for the full version of [171204_pose1](http://domedb.perception.cs.cmu.edu/171204_pose1.html) sequence.

You may find the names of other sequences in our website:

[Browsing dataset](http://domedb.perception.cs.cmu.edu/dataset.html).

You can also specify the number of videos you want to donwload. 
```
./scripts/getData.sh (sequenceName) (VGA_Video_Number) (HD_Video_Number)
```

For example, the following command will download 240 vga videos and 10 videos.  
```
./scripts/getData.sh 171204_pose1_sample 240 10
```

Note that we have sorted the VGA camera order so that you download uniformly distributed view. 


### 3. Extract the images & 3D keypoint data

This step requires [ffmpeg](https://ffmpeg.org/).
```
./scripts/extractAll.sh 171204_pose1_sample
```
This will extract images, for example `171204_pose1_sample/hdImgs/00_00/00_00_00000000.jpg`, and the corresponding 3D skeleton data, for example `171204_pose1_sample/hdPose3d_stage1_coco19/body3DScene_00000000.json`.

`extractAll.sh` is a simple script that combines the following set of commands (you shouldn't need to run these again):
```bash
cd 171204_pose1_sample
../scripts/vgaImgsExtractor.sh # PNG files from VGA video (25 fps)
../scripts/hdImgsExtractor.sh # PNG files from HD video (29.97 fps)
tar -xf vgaPose3d_stage1.tar # Extract skeletons at VGA framerate
tar -xf hdPose3d_stage1.tar # Extract skeletons for HD
cd ..
```

### 4. Run demo programs (Python)
This codes require numpy, matplotlib.


Visualizing 3D keypoints (body, face, hand):

```
cd python
jupyter notebook demo_3Dkeypoints_3dview.ipynb
```
The result should look like [this](https://github.com/CMU-Perceptual-Computing-Lab/panopticapi_d/blob/master/python/demo_3Dkeypoints_3dview.ipynb).


Reprojecting 3D keypoints (body, face, hand) on a selected HD view:

```
cd python
jupyter notebook demo_3Dkeypoints_reprojection_hd.ipynb
```
The result should look like [this](https://github.com/CMU-Perceptual-Computing-Lab/panopticapi_d/blob/master/python/demo_3Dkeypoints_reprojection_hd.ipynb).



### 4. Run demo programs (Matlab)

Note: Matlab code is outdated, and does not handle 3D keypoint outputs (coco19 body, face, hand). 
Please see this code only for reference. We will update this later.

Matlab example (outdated):
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

## License

Panoptic Studio Dataset is freely available for free non-commercial use. 


## References

By using the dataset, you agree to cite at least one of the following papers. 

@InProceedings{Joo_2015_ICCV,
author = {Joo, Hanbyul and Liu, Hao and Tan, Lei and Gui, Lin and Nabbe, Bart and Matthews, Iain and Kanade, Takeo and Nobuhara, Shohei and Sheikh, Yaser},
title = {Panoptic Studio: A Massively Multiview System for Social Motion Capture},
booktitle = {ICCV},
year = {2015} }

@article{Joo_2017_TPAMI,
title={Panoptic Studio: A Massively Multiview System for Social Interaction Capture},
author={Joo, Hanbyul and Simon, Tomas and Li, Xulong and Liu, Hao and Tan, Lei and Gui, Lin and Banerjee, Sean and Godisart, Timothy Scott and Nabbe, Bart and Matthews, Iain and Kanade, Takeo and Nobuhara, Shohei and Sheikh, Yaser},
journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
year={2017} }

@article{Simon_2017_CVPR,
title={Hand Keypoint Detection in Single Images using Multiview Bootstrapping},
author={Simon, Tomas and Joo, Hanbyul and Sheikh, Yaser},
journal={CVPR},
year={2017} }



