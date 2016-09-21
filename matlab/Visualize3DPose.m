function [ output_args ] = Visualize3DPose( poseData)
%% Visualization
maxSkelVisNum=10;

if(length(poseData)==0)
    disp('Warning: poseData is not valid');
    return;
end

hFig= figure; hold on;
cc=hsv(maxSkelVisNum);
set(hFig, 'Position', [500 100 900 600]);
title('3D viewer');
BoneJointOrder = { [2 1 3] ...   %{headtop, neck, bodyCenter}
                    , [1 4 5 6] ... %{neck, leftShoulder, leftArm, leftWrist}
                    , [3 7 8 9] ...  %{neck, leftHip, leftKnee, leftAnkle}
                    , [1 10 11 12]  ... %{neck, rightShoulder, rightArm, rightWrist}
                    , [3 13 14 15]};    %{neck, rightHip, rightKnee, rightAnkle}


skeletonDraw ={};   %Draw unit for each humann. 
for o=1:maxSkelVisNum
    drawObj ={};
   %drawObj{1-5} for skeleton drawing
    for j=1:length(BoneJointOrder)
        colorIdx = mod(o,maxSkelVisNum)+1;
        drawObj{j} = plot3([0 0],[0 0], [0 1], 'color',cc(colorIdx,:), 'linewidth',2, 'marker','*', 'markersize', 4);
    end
    %drawObj{6} for head-caption line
    %drawObj{7} for caption 
    drawObj{end+1} = plot3([0 0],[0 0], [0 1], 'linewidth',1);
    drawObj{end+1} = text(0,0,0,'','FontSize',15);   
    skeletonDraw{o} = drawObj;
end

xlabel('x');
ylabel('z');
zlabel('y');
view(0,-60)
set(gca,'box','on')
ylim([-300 0])
xlim([-300 300])
zlim([-300 300])
set(gca,'dataaspectratio',[1 1 1],'activepositionproperty','OuterPosition'), cameratoolbar
grid on;

[X,Z] = meshgrid(-500:50:500, -500:50:500);
Y = X*0;
surf(X,Y,Z);
colormap([0.95  0.95  0.95])
axis equal;

for idx = 1:length(poseData)
    tic;    
    ylim([-300 0])
    xlim([-300 300])
    zlim([-300 300])
    
    for o=1:length(skeletonDraw)
        for jj=1:length(skeletonDraw{o})
           set(skeletonDraw{o}{jj},'Visible','off');
        end
    end
    for o=1:length(poseData{idx}.bodies)
         
        for jj=1:length(skeletonDraw{o})
            set(skeletonDraw{o}{jj},'Visible','on');
        end
        
        % draw skeletons
        for j=1:size(BoneJointOrder,2)
            jointPts =[];   % Nx3 matrix
            
            for jj=1:size(BoneJointOrder{j},2)
                jointIdx =  BoneJointOrder{j}(jj);
                jointPts = [jointPts ; poseData{idx}.bodies{o}.joints15(jointIdx,:)];
            end
            set(skeletonDraw{o}{j},'xdata',jointPts(:,1));
            set(skeletonDraw{o}{j},'ydata',jointPts(:,2));
            set(skeletonDraw{o}{j},'zdata',jointPts(:,3));
        end
        
        % draw subject IDs
        headPos = poseData{idx}.bodies{o}.joints15(2,:);
        captionPos = headPos;
        captionPos(2) = captionPos(2)-30;

        %line
        set(skeletonDraw{o}{end-1},'Visible','on');
        set(skeletonDraw{o}{end-1},'xdata',[headPos(1) captionPos(1)]);
        set(skeletonDraw{o}{end-1},'ydata',[headPos(2) captionPos(2)]);
        set(skeletonDraw{o}{end-1},'zdata',[headPos(3) captionPos(3)]);

        %caption
        captionStr =sprintf('ID: %d\n',poseData{idx}.bodies{o}.id);
        set(skeletonDraw{o}{end},'Visible','on');
        set(skeletonDraw{o}{end},'String',captionStr);
        set(skeletonDraw{o}{end},'Position',captionPos);    
    end

    time = toc;
    time = max(0.04- time,0);   %for vga frame rate: 25Hz
    pause(time);
    drawnow; 
end


end

