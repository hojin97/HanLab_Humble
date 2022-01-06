%----------------------------------------------------------\
% EMGprocess1.m
% Author : Han U. Yoon (2014/09/02)
% Purpose: practice EMG process
% Revise note: 
%----------------------------------------------------------\

function EMGprocess1

global filteredResult rmsResult datalength 

%%-- read file
filename = 'TRIAL_7.anc';
fid = fopen(filename,'r');
N = 158;
S_text = textscan(fid,'%s',N);
datafieldspec = '%f   %f %f %f %f %f %f   %f %f %f %f %f %f   %f %f %f %f %f %f    %f %f %f %f %f %f    %f %f %f %f %f %f%f %f %f %f %f %f%f %f %f %f    %f %f %f %f';
S_data = textscan(fid,datafieldspec);
fclose(fid);
%---------------------------------------------------------------------------\
% S_data{1,1} = time, sampling rate ts = 1/1000 sec
% S_data{1,2} -- S_data{1,7} = F1X F1Y F1Z M1X M1Y M1Z
% S_data{1,8} -- S_data{1,13} = F2X F2Y F2Z M2X M2Y M2Z
% S_data{1,14} -- S_data{1,19} = F3X F3Y F3Z M3X M3Y M3Z
% S_data{1,20} -- S_data{1,25} = F4X F4Y F4Z M4X M4Y M4Z
% S_data{1,26} ------ S_data{1,41} = EMG1, EMG2, ---- EMG 16
% S_data{1,42} -- S_data{1,45} = C58, C59, C60, PedarX
%---------------------------------------------------------------------------\
% Indexing example
% S{1,1}(1): The first time data = 0.000
% S{1,28}(1000): EMG3 data at time 0.999 sec
%---------------------------------------------------------------------------\

% fieldlength = length(S_data); 
datalength = length(S_data{1,1});

ts = 0.001; % sampling time
% Duration = (datalength - 1) / ts;
scale_factor = 3.0504871567759078830823737821081e-4;

numEMG = 8;
LPfiltered_EMG = zeros(numEMG,datalength);
movingRMS_EMG = zeros(numEMG,datalength);

for i=1:numEMG
    
    Voltage = (S_data{1,26+i-1}-mean(S_data{1,26+i-1}(1:2000))) * scale_factor;
    absVoltage = abs(Voltage);
    
    %% -- original data
    figure(1);
    plot(Voltage);
    % -- figure setting (safe to ignore this!)
    xAxis = ts*get(gca,'XTick');
    set(gca,'XTickLabel',xAxis);
    set(gca,'YLim',[-1.5 1.5]);
    strtitle = sprintf('original EMG%d',i);
    title(strtitle);
    xlabel('[sec]');
    ylabel('[v]')

    %% - processed data
    figure(2);
    % -- apply butterworth filter
    butterWorthLP(absVoltage,15);
    hf = plot(filteredResult,'g'); hold on;
    LPfiltered_EMG(i,:) = filteredResult;
    
    % -- moving RMS
    movingRMS(absVoltage,40);
    hr = plot(rmsResult,'r'); hold off;
    movingRMS_EMG(i,:) = rmsResult;
    
    % -- figure setting (safe to ignore this!)
    xAxis = ts*get(gca,'XTick');
    set(gca,'XTickLabel',xAxis);
    set(gca,'YLim',[-0.1 1.0]);
    strtitle = sprintf('processed EMG%d',i);
    title(strtitle);
    xlabel('[sec]');
    ylabel('[v]');
    legend([hf hr],'butterworth LP-filtered','moving RMS','SouthEast');
    
    pause;
    
end

matfilename = 'processedEMGdata.mat';
save(matfilename,'LPfiltered_EMG','movingRMS_EMG','numEMG','datalength');

end


%------------------------- subfunctions --------------------------%

function butterWorthLP(data,freq)
global filteredResult

[B,A]=butter(4,2*freq/1000,'low');
% absdata = abs(data);
filteredResult = filtfilt(B,A,data);

end

function movingRMS(data, windowSize)
global rmsResult datalength

hWD = windowSize/2; % 10

for i=1:datalength
    
    if i < hWD
        x = data(1:i+hWD);
        y(i) = norm(x)/sqrt(length(x));
    else if i > datalength-hWD
             x = data(i-hWD:datalength);
             y(i) = norm(x)/sqrt(length(x));
        else % normal range
             x = data(i- hWD+1: i+hWD);
             y(i) = norm(x)/sqrt(length(x));   
         end
    end
    
rmsResult = y;    
    
end

end
