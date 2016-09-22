panopticapi_d
=============

panopticapi shows how to work with the [Panoptic Studio](http://domedb.perception.cs.cmu.edu) (Panoptic) data. 

# Quick start guide
Follow these steps to set up a simple example: 

### Check out the codebase
```
git clone https://github.com/hanbyulj/panopticapi_d
cd panopticapi_d 
```

### Download the sample data 
This step requires curl or wget.
```
./getData.sh sampleData
```

### Extract the images & skeleton data 
This step requires [ffmpeg](https://ffmpeg.org/). 
```
cd sampleData
./vgaImgsExtractor.sh
./hdImgsExtractor.sh
tar -xf vgaPose3d_stage1.tar
cd ..
```

### Run the examples
Python example notebook (requires numpy, jupyter):
```
cd python
jupyter notebook example.ipynb
```

Matlab example:
```
>>> cd matlab 
>>> demo
```
