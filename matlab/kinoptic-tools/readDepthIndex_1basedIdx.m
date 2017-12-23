function [im] = readDepthIndex_1basedIdx(fname, idx)
    % Read depth frame at file index (1-based) idx
    % Each frame is 512x424 16-bit uint.
    fid = fopen(fname, 'rb');
    fseek(fid, 2*512*424*(idx-1), 'bof');
    data1 = fread(fid, 512*424, 'uint16=>uint16');
    fclose(fid);
    % Data is stored in row-major.
    im = double(reshape(data1, 512, 424))';
    im = im(:,end:-1:1,:); % Flip left-right
end  