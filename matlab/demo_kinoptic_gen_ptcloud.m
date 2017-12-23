% A demo to show a simple example to generate pointcloud generation 
% from 10 Kinect depth maps of Kipnoptic studio
%
% Note: the output point cloud is located in the same coordinate of
% panoptic studio (480 VGAs + 31 HDs) where 3D skeletons are defined. 
%
% Note2: Frame indices of output ply files are consistent to HD frames of the
% Panoptic Studio. That is ptcloud_000000001.ply is the first frame of HD videos
%
% Note3: This code assumes that your matalb has Computer Vision toolbox to
% save and visualize point cloud data
% (https://www.mathworks.com/help/vision/3-d-point-cloud-processing.html)
%
% Hanbyul Joo (hanbyulj@cs.cmu.edu) and Tomas Simon (tsimon@cs.cmu.edu)

% Input/Output Path Setting  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The following folder hiearchy is assumed:
% (root_path)/(seqName)/kinect_shared_depth
% (root_path)/(seqName)/kinectImgs
% (root_path)/(seqName)/kcalibration_(seqName).json
% (root_path)/(seqName)/ksynctables_(seqName).json
% (root_path)/(seqName)/calibration_(seqName).json
% (root_path)/(seqName)/synctables_(seqName).json

root_path = '[]' %Put your root path where sequence folders are locates
seqName = '[]'  %Put your target sequence name here
hd_index_list= 500:500; % Target frames you want to export ply files

%The followings are an example
% root_path = '/posefs0c/panoptic' %An example
% seqName = '160422_haggling1' %An example
% hd_index_list= 500:510; % Target frames you want to export ply files

%Relative Paths
kinectImgDir = sprintf('%s/%s/kinectImgs',root_path,seqName);  
kinectDepthDir = sprintf('%s/%s/kinect_shared_depth',root_path,seqName);
calibFileName = sprintf('%s/%s/kcalibration_%s.json',root_path,seqName,seqName);
syncTableFileName = sprintf('%s/%s/ksynctables_%s.json',root_path,seqName,seqName);
panopcalibFileName = sprintf('%s/%s/calibration_%s.json',root_path,seqName,seqName);
panopSyncTableFileName = sprintf('%s/%s/synctables_%s.json',root_path,seqName,seqName);

% Output folder Path
%Change the following if you want to save outputs on another folder
plyOutputDir=sprintf('%s/%s/kinoptic_ptclouds',root_path,seqName);
mkdir(plyOutputDir);
disp(sprintf('PLY files will be saved in: %s\',plyOutputDir));

%Other parameters
bVisOutput = 1; %Turn on, if you want to visualize what's going on
bRemoveFloor= 1;  %Turn on, if you want to remove points from floor
floorHeightThreshold = 0.5; % Adjust this (0.5cm ~ 7cm), if floor points are not succesfully removed
                            % Icreasing this may remove feet of people
bRemoveWalls = 1; %Turn on, if you want to remove points from dome surface

addpath('jsonlab');
addpath('kinoptic-tools');

%% Load syncTables
ksync = loadjson(syncTableFileName);
knames = {};
for id=1:10; knames{id} = sprintf('KINECTNODE%d', id); end

psync = loadjson(panopSyncTableFileName); %%Panoptic Sync Tables


%% Load Kinect Calibration File
kinect_calibration = loadjson(calibFileName); 

panoptic_calibration = loadjson(panopcalibFileName);
panoptic_camNames = cellfun( @(X) X.name, panoptic_calibration.cameras, 'uni', false ); %To search the targetCam


hd_index_list = hd_index_list+2; %This is the output frame (-2 is some weired offset in synctables)

for hd_index = hd_index_list

    hd_index_afterOffest = hd_index-2; %This is the output frame (-2 is some weired offset in synctables)
        
%     if( mod(hd_index_afterOffest,10)~=0)
%         continue;       %We ALWAYS save every 10th frames.
%     end
    out_fileName = sprintf('%s/ptcloud_hd%08d.ply', plyOutputDir, hd_index_afterOffest);
    
%     if exist(out_fileName,'file')
%         disp(sprintf('Already exists: %s\n',out_fileName));
%         continue;
%     end
    
    %% Compute Universal time
    selUnivTime = psync.hd.univ_time(hd_index);
    fprintf('hd_index: %d, UnivTime: %.3f\n', hd_index, selUnivTime)


    %% Main Iteration    
    all_point3d_panopticWorld = []; %point cloud output from all kinects
    all_colorsv = [];   %colors for point cloud 


    for idk = 1:10  %Iterating 10 kinects. Change this if you want a subpart

        if idk==1 && bVisOutput   %Visualize the results from the frist kinect only. 
            vis_output = 1;
        else
            vis_output = 0;
        end

        %% Select corresponding frame index rgb and depth by selUnivTime
        % Note that kinects are not perfectly synchronized (it's not possible),
        % and we need to consider offset from the selcUnivTime
        [time_distc, cindex] = min( abs( selUnivTime - (ksync.kinect.color.(knames{idk}).univ_time-6.25) ) );  %cindex: 1 based
        ksync.kinect.color.(knames{idk}).univ_time(cindex);
        % assert(time_dist<30);
        [time_distd, dindex] = min( abs( selUnivTime - ksync.kinect.depth.(knames{idk}).univ_time ) ); %dindex: 1 based

        % Filtering if current kinect data is far from the selected time
        fprintf('idk: %d, %.4f\n', idk, selUnivTime - ksync.kinect.depth.(knames{idk}).univ_time(dindex));
        if abs(ksync.kinect.depth.(knames{idk}).univ_time(dindex) - ksync.kinect.color.(knames{idk}).univ_time(cindex))>6.5
            fprintf('Skipping %d, depth-color diff %.3f\n',  abs(ksync.kinect.depth.(knames{idk}).univ_time(dindex) - ksync.kinect.color.(knames{idk}).univ_time(cindex)));    
            continue;
        end
        % assert(time_dist<30);
        % time_distd
        if time_distc>30 || time_distd>17 
            fprintf('Skipping %d\n', idk);
            [time_distc, time_distd];
            continue;
        end

        % Extract image and depth
        %rgbim_raw = kdata.vobj{idk}.readIndex(cindex); % cindex: 1 based
        rgbFileName = sprintf('%s/50_%02d/50_%02d_%08d.jpg',kinectImgDir,idk,idk,cindex);
        depthFileName = sprintf('%s/KINECTNODE%d/depthdata.dat',kinectDepthDir,idk);

        rgbim = imread(rgbFileName); % cindex: 1 based
        %depthim_raw = kdata.vobj{idk}.readDepthIndex(dindex);  % cindex: 1 based
        depthim = readDepthIndex_1basedIdx(depthFileName,dindex);  % cindex: 1 based

        %Check valid pixels
        validMask = depthim~=0; %Check non-valid depth pixels (which have 0)
        nonValidPixIdx = find(validMask(:)==0);
        %validPixIdx = find(validMask(:)==1);

        if vis_output
            figure; imshow(rgbim);     title('RGB Image');
            figure; imagesc(depthim);  title('Depth Image');
            figure; imshow(validMask*255); title('Validity Mask');
        end

        %% Back project depth to 3D points (in camera coordinate)
        camCalibData = kinect_calibration.sensors{idk};

        % point3d (N x 3): 3D point cloud from depth map in the depth camera cooridnate
        % point2d_color (N x 2): 2D points projected on the rgb image space
        % Where N is the number of pixels of depth image (512*424)
        [point3d, point2d_incolor] = unprojectDepth_release(depthim, camCalibData, true);


        validMask = validMask(:) &  ~(point3d(:,1)==0);
        nonValidPixIdx = find(validMask(:)==0);


        point3d(nonValidPixIdx,:) = nan;
        point2d_incolor(nonValidPixIdx,:) = nan;

%         if vis_output
%             figure; plot3(point3d(:,1),point3d(:,2),point3d(:,3),'.'); axis equal;  %Plot raw 3D points
%         end

        %% Filtering based on the distance from the dome center
        domeCenter_kinectlocal = camCalibData.domeCenter;
        
        if bRemoveWalls
            dist = sqrt(sum(bsxfun(@minus, point3d(:,1:3), domeCenter_kinectlocal').^2,2));
            point3d(dist>2.5,:) = nan;
            point3d(point3d(:,2)>2.3,:) = nan;
        end

        if vis_output
            figure; plot3(point3d(:,1),point3d(:,2),point3d(:,3),'.'); axis equal;  %Plot raw 3D points
            title('Unprojecting Depth from Kinect1 (after filtering dome wall');
            view(2);
        end


        %% Project 3D points (from depth) to color image
        colors_inDepth = multiChannelInterp( double(rgbim)/255, ...
            point2d_incolor(:,1)+1, point2d_incolor(:,2)+1, 'linear');

        colors_inDepth = reshape(colors_inDepth, [size(depthim,1), size(depthim,2), 3]);
        colorsv = reshape(colors_inDepth, [], 3);


        % valid_mask = depthim~=0;
        validMask = validMask(:) & ~isnan(point3d(:,1));
        validMask = validMask(:) & ~isnan(colorsv(:,1));
        %nonValidPixIdx = find(validMask(:)==0);
        validPixIdx = find(validMask(:)==1);

        if vis_output
            %Note that this image has an artifact since no z-buffering are
            %performed 
            %That is, occluded part may extract colors from RGB image
            figure; imshow(colors_inDepth); 
            title('Depth map, after extracting colors from RGB image');
        end

        %% Extract color for depth camera
        if vis_output
            figure; scatter3(point3d(:,1),point3d(:,2),point3d(:,3),1,colorsv);  axis equal;
            title('Pt cloud from Kinect1, after extracting colors');
            view(2);
        end


        %% Transform Kinect Local to Panoptic World

        % Kinect local coordinate is defined by depth camera coordinate
        panoptic_calibData = panoptic_calibration.cameras{find(strcmp(panoptic_camNames, sprintf('50_%02d', idk)))};
        M = [panoptic_calibData.R, panoptic_calibData.t];
        T_panopticWorld2KinectColor = [M; [0 0 0 1]]; %Panoptic_world to Kinect_color
        T_kinectColor2PanopticWorld = inv(T_panopticWorld2KinectColor);

        scale_kinoptic2panoptic = eye(4);
        scaleFactor = 100;%0.01; %centimeter to meter
        scale_kinoptic2panoptic(1:3,1:3) = scaleFactor*scale_kinoptic2panoptic(1:3,1:3);

        %T_kinectColor2KinectLocal = [calib_rgbCam.Mdist;[0 0 0 1]];  %Color2Depth camera coordinate
        T_kinectColor2KinectLocal = camCalibData.M_color;%[camCalibData.M_color;[0 0 0 1]];  %Color2Depth camera coordinate
        T_kinectLocal2KinectColor = inv(T_kinectColor2KinectLocal);

        T_kinectLocal2PanopticWorld =  T_kinectColor2PanopticWorld* scale_kinoptic2panoptic* T_kinectLocal2KinectColor;

        %% Merge Multiple Kinects into world_kinect coordinate (1st Kinect's coordinate)
        % Transform 3D points to kinect_world coordinate
        %T_kinectLocal2KinectWorld = inv(camCalibData.M_world2sensor);       %kinectLocal to kinectWorld (1st Kinect's cooridnate)
        %point3d_kinectWorld = T_kinectLocal2KinectWorld*[point3d'; ones(1, size(point3d,1))];
        %point3d_kinectWorld = point3d_kinectWorld(1:3,:)';
        %point3d_kinectWorld = double(point3d_kinectWorld);
        %all_point3d_kinectWorld = [all_point3d_kinectWorld ; point3d_kinectWorld(validPixIdx,:)];
        %all_colorsv = [all_colorsv ; colorsv(validPixIdx,:)];


        %% Merge Multiple Kinects into panoptic_kinect coordinate
        %Transform to panoptic coordinate
        point3d_panopticWorld = T_kinectLocal2PanopticWorld*[point3d'; ones(1, size(point3d,1))];
        point3d_panopticWorld = point3d_panopticWorld(1:3,:)';
        point3d_panopticWorld = double(point3d_panopticWorld);

        all_point3d_panopticWorld = [all_point3d_panopticWorld; point3d_panopticWorld(validPixIdx,:)];
        all_colorsv = [all_colorsv ; colorsv(validPixIdx,:)];

    end

    %% Visualize Point Cloud
%     if bVisOutput
%         %sampling = 20;   %Too slow to visualize all points
%         figure; scatter3(all_point3d_kinectWorld(1:sampling:end,1),all_point3d_kinectWorld(1:sampling:end,2),all_point3d_kinectWorld(1:sampling:end,3),1, all_colorsv(1:sampling:end,:));  axis equal;
%         %figure; scatter3(all_point3d_panopticWorld(1:sampling:end,1),all_point3d_panopticWorld(1:sampling:end,2),all_point3d_panopticWorld(1:sampling:end,3),1, all_colorsv(1:sampling:end,:));  axis equal;
%         title('Pt cloud from all kinects (sampled by 20 for faster visualization)');
%         view(2);
%     end

    if isempty(all_point3d_panopticWorld)
        break;
    end
    
    %% Delete floor light
    if bRemoveFloor
                
        % Delete floor points
        % Crop floor 
        floorPtIdx =(find(all_point3d_panopticWorld(:,2)>-floorHeightThreshold));      %Up-direction => negative Y axis
        all_point3d_panopticWorld(floorPtIdx,:) =[];
        all_colorsv(floorPtIdx,:) =[];
        
        %%Delete floor light
        ptCopy = all_point3d_panopticWorld;
        ptCopy(:,2) =0;
        ptCopy = ptCopy.^2;
        distFromCenter =sqrt(sum(ptCopy,2));
        outliers =(find(distFromCenter>225));      %Up-direction => negative Y axis
        all_point3d_panopticWorld(outliers,:) =[];
        all_colorsv(outliers,:) =[];
    end
    
    
   
    %% Save point cloud as a ply file
    %simple_ply_write2b_color( all_point3d_kinectWorld, all_colorsv*255, sprintf('%s/frame%08d.ply', plyOutputDir, frameIdx) );
  
    out_pc = pointCloud(all_point3d_panopticWorld);
    out_pc.Color = uint8(round(all_colorsv*255));
     
    %% Visualize Point Cloud
    if bVisOutput
        close all;
        pcshow(out_pc);
        title('Pt cloud from all kinects after filtering');
        view(2);
    end   
    
    pcwrite(out_pc,out_fileName,'PLYFormat','ascii');
    
    
    
end

