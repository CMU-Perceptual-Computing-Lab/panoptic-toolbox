function simple_ply_write2b_color( V, C, name )
%function simple_ply_write( V, F, C, name )
%
%     V is a Nx3 matrix of vertex coordinates.
%     F is a Mx3 matrix of vertex indices.
%     C is a Nx3 matrix of vertex colors (or the empty matrix).
%     fname is the filename to save the PLY file.

fid = fopen(name,'w');
% 'format binary_little_endian 1.0\n' ... 
fprintf(fid,[ 'ply\n' ...
              'format ascii 1.0\n' ...
              'comment author: Pepe\n' ...
              'comment object: another object\n' ]);         

fprintf(fid, 'element vertex %d\n', size(V,1));    % number of vertices

fprintf(fid, ['property float32 x\n' ...
              'property float32 y\n' ...
              'property float32 z\n' ]);
%           
% fprintf(fid, ['property float32 nx\n' ...
%   'property float32 ny\n' ...
%   'property float32 nz\n' ]);

if ~isempty(C)
%     fprintf(fid, ['property red   uchar\n' ...
%                   'property green uchar\n' ...
%                   'property blue  uchar\n' ]);
    fprintf(fid, ['property uchar red\n' ...
                  'property uchar green\n' ...
                  'property uchar blue\n' ]);
    
    if (size(C,2) == 4)
        fprintf(fid,'property uchar alpha\n');
    end
end

%fprintf(fid, 'element face %d\n', size(F,1));      % number of faces

%fprintf(fid, 'property list uchar int vertex_indices\n');

fprintf(fid, 'end_header\n');
% fclose(fid);
% fid = fopen(name,'a','ieee-le');
% ------------------------------------------------------------------------------
% Vertex data
if isempty(C)
    fprintf(fid,'%f %f %f\n', V');
    %fprintf(fid,'%f %f %f %f %f %f\n', [V'; N']);
else
%     fprintf(fid,'%f %f %f %d %d %d\n', [ V round(double(C)) ]');
if (size(C,2) == 4)
    fprintf(fid,'%f %f %f %d %d %d %d\n', [ V N round(double(C)) ]');
else
    
    fprintf(fid,'%f %f %f %d %d %d\n', [ V round(double(C)) ]');
end
%     for idr=1:size(V,1)
%         fwrite(fid, V(idr,1:3), 'float32',0, 'l');
%         fwrite(fid, C(idr,1:3), 'uint8');
%     end
end

% Face data: 1st # is entries in the list (a 'uchar' in this case) 
% sz = size(F);
% if ~isempty(F)
%     fprintf(fid,'%d %d %d %d\n', [ sz(2)*ones(sz(1),1) F-1 ]');      % convert 1 to 0 offset of 1st vertex ID
% end

fclose(fid);
% ------------------------------------------------------------------------------