function hfig = visualize_sigDATA_colormap(sigDATA,nCH,height,stretchFactor,strcmap)

% m =  [
%        0:0.1:1;
%        1:-0.1:0;
%       ];
  
m = sigDATA;  
n = length(m(1,:));

% numEMGch = 2;
% height = 10;
% stretchFactor = 2.0;

for i = 1:nCH
    % m = sigDATA(1,:);
    % n = length(sigDATA(1,:));
    m2 = interp1(1:n, m(i,:), linspace(1, n, stretchFactor*n), 'nearest');
    m3 = repmat(m2,[height, 1]);
    m4(height*(i-1)+1:height*i,:) = m3;
end

hfig = figure(3);
image(m4*256*0.9);

switch strcmap
    case 'jet'
        colormap(jet(256));
    case 'gray'
        colormap(gray(256));
    case 'bone'
        colormap(bone(256));
    otherwise
        error('wrong color map option!');
end

% set(gca,'YDir','normal')
% set(gca,'YTickLabel',{'One';'Two';'Three';'Four'})

axis off;

end