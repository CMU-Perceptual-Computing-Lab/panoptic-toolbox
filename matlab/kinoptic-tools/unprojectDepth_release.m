function [p3d, p2d] = unprojectDepth_release(depth, camCalibData, bGenColorMap)

[X,Y] = meshgrid( (0:511), (0:423) );
p2dd = [X(:) Y(:)];


depthcam.Kdist = camCalibData.K_depth;
depthcam.Mdist = camCalibData.M_depth(1:3,:);
depthcam.distCoeffs = camCalibData.distCoeffs_depth;

p3d = unproject([p2dd depth(:)], depthcam);

%if exist('cam', 'var') && ~isempty(cam)
if  exist('bGenColorMap', 'var') && bGenColorMap
%     cam2.R = cam.Mdist(1:3,1:3);
%     cam2.t = cam.Mdist(1:3,4);
%     cam2.K = cam.Kdist;
%     cam2.distCoef = cam.distCoeffs;

     rgbcam.R = camCalibData.M_color(1:3,1:3);
     rgbcam.t = camCalibData.M_color(1:3,4);
     rgbcam.K = camCalibData.K_color;
     rgbcam.distCoef = camCalibData.distCoeffs_color;
    [pt] = PoseProject2D(p3d(:,1:3), rgbcam, 1);
    p2d = pt;
    %imagePoints = cv.projectPoints(p3d(:,1:3), cam.rvec, cam.tvec, cam.Kdist, cam.distCoeffs(1:5));
    %p2d = squeeze(imagePoints);
end