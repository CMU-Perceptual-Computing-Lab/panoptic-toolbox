function [p3d] = unproject( p2d, cam )
    % [p3d] = unproject( p2d, cam )
    % p2d is an Nx3 array with pixel_X, pixel_Y,depth
    % cam contains the depth camera intrinsic parameters
    % cam.Kdist --- 3x3 intrinsic matrix
    % cam.distCoeffs --- OpenCV-style distortion coefficients.
    % Returns:
    %   p3d --- Nx3 array with X,Y,Z coordinates.
    
    % Normalized points
    pn2d = ( cam.Kdist \ [p2d(:,1:2)'; ones(1, size(p2d,1))] )';
    k = [reshape(cam.distCoeffs(1:5),[],1); zeros(12-5,1)];
    x0 = pn2d(:,1); 
    y0 = pn2d(:,2);
    x = x0; y = y0;
    
    % Undistortion iterations.
    % See cv::undistortPoints n modules/imgproc/src/undistort.cpp
    % https://github.com/opencv/opencv
    for iter=1:5
        r2 = x.*x + y.*y;
        icdist = (1 + ((k(1+7)*r2 + k(1+6)).*r2 + k(1+5)).*r2)./(1 + ((k(1+4)*r2 + k(1+1)).*r2 + k(1+0)).*r2);
        deltaX = 2*k(1+2)*x.*y + k(1+3)*(r2 + 2*x.*x)+ k(1+8)*r2+k(1+9)*r2.*r2;
        deltaY = k(1+2)*(r2 + 2*y.*y) + 2*k(1+3)*x.*y+ k(1+10)*r2+k(1+11)*r2.*r2;
        x = (x0 - deltaX).*icdist;
        y = (y0 - deltaY).*icdist;
    end
    pn2d = [x y];
    
    if size(pn2d,2)==1
        pn2d = pn2d';
    end
    p3d = [bsxfun(@times, pn2d, p2d(:,3)*0.001) p2d(:,3)*0.001];
    p3d = (inv([cam.Mdist;[0 0 0 1]])*[p3d ones(size(p3d,1),1)]')';
    p3d(:,4) = [];
