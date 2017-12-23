% A demo to show a simple example to project pointclouds to rgb images
%
% Note: the point cloud is located in the same coordinate of
% panoptic studio (480 VGAs + 31 HDs)
%
% Note2: Frame indices of output ply files are consistent to HD frames of the
% Panoptic Studio. That is ptcloud_000000001.ply is the first frame of HD videos
%
% Note3: This code assumes that your matalb has Computer Vision toolbox to
% save and visualize point cloud data
% (https://www.mathworks.com/help/vision/3-d-point-cloud-processing.html)
%
% Hanbyul Joo (hanbyulj@cs.cmu.edu) and Tomas Simon (tsimon@cs.cmu.edu)

% Input Path Setting  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The following folder hiearchy is assumed:
% (root_path)/(seqName)/hdImgs
% (root_path)/(seqName)/calibration_(seqName).json
% (root_path)/(seqName)/kcalibration_(seqName).json

%Set the following variables 
root_path = '[]' %Set your path
seqName = '[]' %Set your target sequence name
%root_path = '/posefs0c/panoptic' %An example
%seqName = '171204_pose1' %An example
hd_index_list= 395:1:410; % Target frames you want to export ply files

%Target camera (see 'Camera Naming Rule' of
%http://domedb.perception.cs.cmu.edu/tools.html)
panelIdx = 0;  %0 means HD
camIdx = 10;   


%Relative Paths
%kinectImgDir = sprintf('/%s/%s/kinectImgs',root_path,seqName);  
panopticHDImgDir = sprintf('/%s/%s/hdImgs',root_path,seqName);
panopcalibFileName = sprintf('%s/%s/calibration_%s.json',root_path,seqName,seqName);
plyInputDir = sprintf('/%s/%s/kinoptic_ptclouds',root_path,seqName); 
%plyInputDir ='[]'; %Set this manually if you have ply files in another folder

%Other parameters
bRemoveFloor= 1;  %Turn on, if you want to remove points from floor
floorHeightThreshold = 5; % Adjust this (0.5cm ~ 7cm), if floor points are not succesfully removed

addpath('jsonlab');
addpath('kinoptic-tools');

%% Load Panoptic Calibration File
panoptic_calibration = loadjson(panopcalibFileName);
panoptic_camNames = cellfun( @(X) X.name, panoptic_calibration.cameras, 'uni', false ); %To search the targetCam
camCalibData = panoptic_calibration.cameras{find(strcmp(panoptic_camNames, sprintf('%02d_%02d', panelIdx, camIdx)))};   

for hd_index = hd_index_list
    
    in_fileName = sprintf('%s/ptcloud_hd%08d.ply', plyInputDir, hd_index);    
    pointcloud = pcread(in_fileName);
    
    %% Delete floor light
    if bRemoveFloor
        floorPtIdx =(find(pointcloud.Location(:,2)>-floorHeightThreshold));      %Up-direction => negative Y axis
        
        pts = pointcloud.Location;
        pts(floorPtIdx,:) =[];
        
        colors = pointcloud.Color;
        colors(floorPtIdx,:) =[];
        out_pc = pointCloud(pts);
        out_pc.Color = colors;
        
        pointcloud = out_pc;
    end    
    
    figure; pcshow(pointcloud);
    title('Pt cloud from all kinects after filtering');
    view(0,-80);
    disp('Press any key');
    waitforbuttonpress;
    
    %
    %rgbFileName = sprintf('%s/50_%02d/50_%02d_%08d.jpg',kinectImgDir,idk,idk,cindex);
    rgbFileName = sprintf('%s/%s/%s_%08d.jpg',panopticHDImgDir,camCalibData.name,camCalibData.name,hd_index);
    rgbim = imread(rgbFileName); % cindex: 1 based
    figure; imshow(rgbim);

    
    [pt2] = PoseProject2D(pointcloud.Location(1:5:end,:), camCalibData, 1);
       
    pt2_x = pt2(:,1);
    pt2_y = pt2(:,2);
    
    idx = find(pt2_x<0 |  pt2_y<0 | pt2_x>1920 | pt2_y>1080 );
    pt2(idx,:) = [];
    hold on; plot(pt2(:,1),pt2(:,2),'.');
    axis equal;
    
    disp('Press any key');
    waitforbuttonpress;   
    
end

