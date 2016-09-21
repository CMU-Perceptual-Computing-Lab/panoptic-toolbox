function [ pose2D] = PoseProject2D(singlePoseData,camData,bApplyDistort)

pose2D = zeros(size(singlePoseData.joints15,1),2);
for i=1:size(singlePoseData.joints15,1)
    temp = camData.R * singlePoseData.joints15(i,:)' + camData.t;
    
    %Apply distortion
    %Distortion parameter order follows opencv format
    %(http://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html)
    if bApplyDistort
        temp = temp/temp(3);
        r2 = temp(1)*temp(1) + temp(2)*temp(2);
        r4= r2*r2;
        r6 = r2*r4;
        X2 = temp(1)*temp(1);
        Y2 = temp(2)*temp(2);
        XY = temp(1)*temp(2);

        radial       = 1.0 + camData.distCoef(1)*r2 + camData.distCoef(2)*r4 + camData.distCoef(5)*r6;
        tangential_x = 2.0*camData.distCoef(3)*XY + camData.distCoef(4)*(r2 + 2.0*X2);
        tangential_y = camData.distCoef(3)*(r2 + 2.0*Y2) + 2.0*camData.distCoef(4)*XY;


        pt_distorted = ones(3,1);
        pt_distorted(1) = radial*temp(1) + tangential_x;
        pt_distorted(2) = radial*temp(2) + tangential_y;    
        pt_distorted = camData.K*pt_distorted;
        pt_distorted = pt_distorted/pt_distorted(3);
        pose2D(i,:) = pt_distorted (1:2);
    else
        pt_ideal = camData.K*temp;
        pt_ideal = pt_ideal/pt_ideal(3);
        pose2D(i,:) = pt_ideal(1:2);
    end
    
    
end
   
end