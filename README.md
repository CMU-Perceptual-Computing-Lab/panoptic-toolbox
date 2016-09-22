PanopticStudio Toolbox
======================

This repository shows how to work with the [Panoptic Studio](http://domedb.perception.cs.cmu.edu) (Panoptic) data.

## Quick start guide
Follow these steps to set up a simple example:

### Check out the codebase
```
git clone https://github.com/hanbyulj/panopticapi_d
cd panopticapi_d
```

### Download the sample data
This bash script requires curl or wget.
```
./scripts/getData.sh sampleData
```

### Extract the images & skeleton data
This step requires [ffmpeg](https://ffmpeg.org/).
```
./scripts/extractAll.sh sampleData
```
The above command is a convenience script that combines the following set of commands:
```
cd sampleData
../scripts/vgaImgsExtractor.sh
../scripts/hdImgsExtractor.sh
tar -xf vgaPose3d_stage1.tar
tar -xf hdPose3d_stage1.tar
cd ..
```

### Run the examples
Python examples (require numpy, matplotlib):
```
cd python
jupyter notebook example.ipynb
```
or, to show frame `100` from camera `01_02`,
```
python python/show_frame.py ./sampleData 01_02 100
```

Matlab example:
```matlab
>>> cd matlab
>>> demo
```
