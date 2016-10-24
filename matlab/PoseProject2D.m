function [pt] = PoseProject2D(pts, cam, bApplyDistort)
% [pt] = PoseProject2D(pts, cam, bApplyDistort)
% pts - Nx3 points
% cam - camera structure, with R, t, distCoef fields
% bApplyDistort - apply distortion flag
%
% Returns
% pt - Nx2 projected points

x = bsxfun(@plus, cam.R * pts', cam.t(:));
xp = bsxfun(@rdivide, x(1:2,:), x(3,:));

%Apply distortion
%Distortion parameter order follows opencv format
%(http://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html)
if bApplyDistort
    X2 = xp(1,:).*xp(1,:);
    Y2 = xp(2,:).*xp(2,:);
    XY = xp(1,:).*xp(2,:);
    r2 = X2+Y2;
    r4 = r2.*r2;
    r6 = r2.*r4;

    Kp = cam.distCoef;
    radial       = 1.0 + Kp(1)*r2 + Kp(2)*r4 + Kp(5)*r6;
    tangential_x = 2.0*Kp(3)*XY + Kp(4)*(r2 + 2.0*X2);
    tangential_y = 2.0*Kp(4)*XY + Kp(3)*(r2 + 2.0*Y2);

    xp = [radial;radial].*xp(1:2,:) + [tangential_x; tangential_y];
end

pt = bsxfun(@plus, cam.K(1:2,1:2)*xp, cam.K(1:2,3))';
