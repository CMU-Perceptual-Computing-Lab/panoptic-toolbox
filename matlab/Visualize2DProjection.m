function [ output_args ] = Visualize2DProjection(im,pose2D)
maxSkelVisNum=10;

figure;
if(length(pose2D)==0)
    disp('Warning: poseData is not valid');
    return;
end
cc=hsv(maxSkelVisNum);
BoneJointOrder = { [2 1 3] ...   %{headtop, neck, bodyCenter}
                    , [1 4 5 6] ... %{neck, leftShoulder, leftArm, leftWrist}
                    , [3 7 8 9] ...  %{neck, leftHip, leftKnee, leftAnkle}
                    , [1 10 11 12]  ... %{neck, rightShoulder, rightArm, rightWrist}
                    , [3 13 14 15]};    %{neck, rightHip, rightKnee, rightAnkle}

imshow(im);
hold on;
title('3D Body Pose Projection');
for o=1:length(pose2D)
     colorIdx = mod(o,maxSkelVisNum)+1;
    % draw skeletons
    for j=1:size(BoneJointOrder,2)
        jointPts =[];   % Nx2 matrix

        for jj=1:size(BoneJointOrder{j},2)
            jointIdx =  BoneJointOrder{j}(jj);
            jointPts = [jointPts ; pose2D{o}(jointIdx,:)];
        end
        plot(jointPts(:,1),jointPts(:,2),'color',cc(colorIdx,:));
        hold on;
        
    end
end

axis equal;


end

