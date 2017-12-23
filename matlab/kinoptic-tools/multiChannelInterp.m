function V = multiChannelInterp( M, i, j, method )
% Returns a matrix V nPixels x nChannels
% from a 3-dimensional matrix M such that
% V(:, idc) = " M( sub2ind( maskc, j, idc ) ) "

if nargin<4
    method = 'linear';
end

nChannels = size(M,3);
i = i(:);
j = j(:);
V = zeros( length(i), nChannels);
for idc=1:size(M,3)
%     V(:, idc) = M(sub2ind( size(M), i, j, idc*ones(size(i))));
    V(:, idc) = interp2( M(:,:,idc), i, j, method );
end