% Demo to show simple examples to use Panoptic Dataset

% Dataset Path
datasetDir='../sampleData';
vgaImgDir = [datasetDir '/vgaImgs'];
vgaPoseDir = [datasetDir '/vgaPose3d_stage1'];
calibFileName = [datasetDir '/calibration_sampleData.json'];
frameStart = 0;
frameEnd = 9;
vga_panelIdx =1;
vga_camIdx =1;

% Data is kept in json format
addpath('jsonlab');

%% Load body pose data
poseData = PoseLoaderJson(vgaPoseDir,frameStart,frameEnd); % poseData{idx} contains skeletons per frame

%% Load calibration data
camName =sprintf('%02d_%02d',vga_panelIdx,vga_camIdx);
calibData= loadjson(calibFileName);
cameras = calibData.cameras;
targetCam =[];
for idx=1:length(cameras)
    if(strcmp(cameras{idx}.name,camName))
        targetCam = cameras{idx}
        break;
    end
end
% buf = targetCam.distCoef(4)
% targetCam.distCoef(4) = targetCam.distCoef(5)
% targetCam.distCoef(5) = buf;
%% Projection on a image
frameIdx = poseData{1}.frameIdx;    %Just use the first frame of the loaded poseData
imPath = sprintf('%s/%02d_%02d/%02d_%02d_%08d.jpg',vgaImgDir,...
				 vga_panelIdx,vga_camIdx,vga_panelIdx,vga_camIdx,frameIdx);
im = imread(imPath);

pose2D={};
for i=1:length(poseData{1}.bodies);
    pose2D{i} = PoseProject2D(poseData{1}.bodies{i}.joints15,targetCam,true);
end
Visualize2DProjection(im,pose2D);

saveas(gcf, 'example_projection.jpg');

%% Visualize body pose data in 3D
Visualize3DPose(poseData);

saveas(gcf, 'example_3d.jpg');
