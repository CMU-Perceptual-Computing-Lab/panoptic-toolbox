function [ poseData ] = PoseLoaderJson( folderName,frameStart,frameEnd )

poseData ={};
for f=frameStart:frameEnd
    fileName = sprintf('%s/body3DScene_%08d.json',folderName,f);
    if (exist(fileName,'file') ==0)
        disp(sprintf('##ERROR: Cannot find the file: %s\n',fileName));
        break;
    end    
    data = loadjson(fileName);
    poseData{end+1}.frameIdx = f;
    poseData{end}.bodies = data.bodies;     %bodies{}.joint15  contains 1x60 size of vectors
    for i=1:length(poseData{end}.bodies);
        temp = reshape(poseData{end}.bodies{i}.joints15,4,15)';
        poseData{end}.bodies{i}.joints15 = temp(:,1:3); %15x3 matrix where each row represents 3D joint location
        poseData{end}.bodies{i}.scores = temp(:,4);   %15x1 matrix where each row represents 3D joint score
    end
  
    
end
end

