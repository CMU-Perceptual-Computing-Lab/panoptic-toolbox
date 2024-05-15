# PanopticStudio Toolbox

This repository has a toolbox to download, process, and visualize the [Panoptic Studio](http://domedb.perception.cs.cmu.edu) (Panoptic) data.

# Note:

- May-14-2024: We have built a mirror server at [SNU](http://vcl.snu.ac.kr/panoptic). 
  You may still use the original CMU server, and if the CMU server doesn't respond, You can use the SNU endpoint by simply adding `--snu-endpoint` option in `getData.sh` and `getData_kinoptic` scripts.

# Quick start guide

Follow these steps to set up a simple example:

## 1. Check out the codebase

```
git clone https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox
cd panoptic-toolbox
```

## 2. Download a sample data and other data

To download a dataset, named "171204_pose1_sample" in this example, run the following script.

```
./scripts/getData.sh 171204_pose1_sample
```

This bash script requires curl or wget.

This script will create a folder "./171204_pose1_sample" and download the following files.

- 171204_pose1_sample/hdVideos/hd_00_XX.mp4 #synchronized HD video files (31 views)
- 171204_pose1_sample/vgaVideos/KINECTNODE%d/vga_XX_XX.mp4 #synchrponized VGA video files (480 views)
- 171204_pose1_sample/calibration_171204_pose1_sample.json #calibration files
- 171204_pose1_sample/hdPose3d_stage1_coco19.tar #3D Body Keypoint Data (coco19 keypoint definition)
- 171204_pose1_sample/hdFace3d.tar #3D Face Keypoint Data
- 171204_pose1_sample/hdHand3d.tar #3D Hand Keypoint Data

Note that this sample example currently does not have VGA videos.

You can also download any other seqeunce through this script. Just use the the name of the target sequence: instead of the "171204_pose1panopticHD".
r example,

```
./scripts/getData.sh 171204_pose1
```

for the full version of [171204_pose1](http://domedb.perception.cs.cmu.edu/171204_pose1.html) sequence:.
You can also specify the number of videospanopticHDnt to donwload.

```
./scripts/getData.sh (sequenceName) (VGA_Video_Number) (HD_Video_Number)
```

For example, the following command will download 240 vga videos and 10 videos.

```
./scripts/getData.sh 171204_pose1_sample 240 10
```

Note that we have sorted the VGA camera order so that you download uniformly distributed view.

## 3. Downloading All Available Sequences

You can find the list of currently available sequences in the following link:

[List of released sequences (ver1.2)](https://docs.google.com/spreadsheets/d/1eoe74dHRtoMVVFLKCTJkAtF8zqxAnoo2Nt15CYYvHEE/edit#gid=1333444170)

Downloading all of them (including videos) may take a long time, but downloading 3D keypoint files (body+face+hand upon their availability) should be "relatively" quick.

You can use the following script to download currently available sequences (ver 1.2):

```
./scripts/getDB_panopticHD_ver1_2.sh
```

The default setting is not downloading any videos. Feel free to change the "vgaVideoNum" and "hdVideoNum" in the script to other numbers if you also want to download videos.

You can see the example videos and other information of each sequence: in our website:
[Browsing dataset](http://domedb.perception.cs.cmupanopticHDtaset.html).

Check the 3D viewer in each sequence: page where you can visualize 3D skeletons in your web browser. For example:
http://domedb.perception.cs.cmu.edu/panopticHDpose1.html

## 4. Extract the images & 3D keypoint data

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

## 5. Run demo programs

### Python

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

### Python + OpengGL

- This codes require pyopengl.

- Visualizing 3D keypoints (body, face, hand):

```
python glViewer.py
```

### Matlab

Note: Matlab code is outdated, and does not handle 3D keypoint outputs (coco19 body, face, hand).
Please see this code only for reference. We will update this later.

Matlab example (outdated):

```matlab
>>> cd matlab
>>> demo
```

## Skeleton Output Format

We reconstruct 3D skeleton of people using the method of [Joo et al. 2018](https://ieeexplore.ieee.org/document/8187699).

The output of each frame is written in a json file. For example,

```
{ "version": 0.7,
"univTime" :53541.542,
"fpsType" :"hd_29_97",
"bodies" :
[
{ "id": 0,
"joints19": [-19.4528, -146.612, 1.46159, 0.724274, -40.4564, -163.091, -0.521563, 0.575897, -14.9749, -91.0176, 4.24329, 0.361725, -19.2473, -146.679, -16.1136, 0.643555, -14.7958, -118.804, -20.6738, 0.619599, -22.611, -93.8793, -17.7834, 0.557953, -12.3267, -91.5465, -6.55368, 0.353241, -12.6556, -47.0963, -4.83599, 0.455566, -10.8069, -8.31645, -4.20936, 0.501312, -20.2358, -147.348, 19.1843, 0.628022, -13.1145, -120.269, 28.0371, 0.63559, -20.1037, -94.3607, 30.0809, 0.625916, -17.623, -90.4888, 15.0403, 0.327759, -17.3973, -46.9311, 15.9659, 0.419586, -13.1719, -7.60601, 13.4749, 0.519653, -38.7164, -166.851, -3.25917, 0.46228, -28.7043, -167.333, -7.15903, 0.523224, -39.0433, -166.677, 2.55916, 0.395965, -30.0718, -167.264, 8.18371, 0.510041]
}
] }
```

Here, each subject has the following values.

**id**: a unique subject index within a sequence:. Skeletons with the same id across time represent temporally associated moving skeletons (an individual). However, the same person may have multiple ids **joints19**: 19 3D joint locations, formatted as [x1,y1,z1,c1,x2,y2,z2,c2,...] where each c ispanopticHDjoint confidence score.

The 3D skeletons have the following keypoint order:

```
0: Neck
1: Nose
2: BodyCenter (center of hips)
3: lShoulder
4: lElbow
5: lWrist,
6: lHip
7: lKnee
8: lAnkle
9: rShoulder
10: rElbow
11: rWrist
12: rHip
13: rKnee
14: rAnkle
15: lEye
16: lEar
17: rEye
18: rEar
```

Note that this is different from [OpenPose output order](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md), although our method is based on it.

Note that we used to use an old format (named mpi15 as described in our [outdated document](http://domedb.perception.cs.cmu.edu/tools.html)), but we do not this format anymore.

# KinopticStudio Toolbox

Kinoptic Studio is a subsystem of Panoptic Studio, which is composed of 10 Kinect2 sensors.
Please see: [README_kinoptic](README_kinoptic.md)

# Panoptic 3D PointCloud DB ver.1

You can download all sequences included in our [3D PointCloud DB ver.1](https://docs.google.com/spreadsheets/d/1MsD9ioWBToHWz0E33gzFS5nDDjVHRECE2bZ1vM1ff_I/edit?usp=sharing) using the following script:

```
./scripts/getDB_ptCloud_ver1.sh
```

# Haggling DB

We have released the processed data for the haggling sequence. Please see [Social Signal Processing](https://github.com/CMU-Perceptual-Computing-Lab/ssp) repository.

![Teaser Image](https://github.com/jhugestar/jhugestar.github.io/blob/master/img/cvpr19_ssp.gif)

# License

Panoptic Studio Dataset is freely available for non-commercial and research purpose only.

# References

By using the dataset, you agree to cite at least one of the following papers.

```
@inproceedings{Joo_2015_ICCV,
author = {Joo, Hanbyul and Liu, Hao and Tan, Lei and Gui, Lin and Nabbe, Bart and Matthews, Iain and Kanade, Takeo and Nobuhara, Shohei and Sheikh, Yaser},
title = {Panoptic Studio: A Massively Multiview System for Social Motion Capture},
booktitle = {ICCV},
year = {2015} }

@inproceedings{Joo_2017_TPAMI,
title={Panoptic Studio: A Massively Multiview System for Social Interaction Capture},
author={Joo, Hanbyul and Simon, Tomas and Li, Xulong and Liu, Hao and Tan, Lei and Gui, Lin and Banerjee, Sean and Godisart, Timothy Scott and Nabbe, Bart and Matthews, Iain and Kanade, Takeo and Nobuhara, Shohei and Sheikh, Yaser},
journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
year={2017} }

@inproceedings{Simon_2017_CVPR,
title={Hand Keypoint Detection in Single Images using Multiview Bootstrapping},
author={Simon, Tomas and Joo, Hanbyul and Sheikh, Yaser},
journal={CVPR},
year={2017} }

@inproceedings{joo2019ssp,
  title={Towards Social Artificial Intelligence: Nonverbal Social Signal Prediction in A Triadic Interaction},
  author={Joo, Hanbyul and Simon, Tomas and Cikara, Mina and Sheikh, Yaser},
  booktitle={CVPR},
  year={2019}
}



```
