%----------------------------------------------------------\
% EMGprocessing_Myodata_v0.m
% Author : Han U. Yoon (2021/01/23)
% Purpose: To give some nice exprience to my commrade J.H. and H.J.
% Revise note: ver1.0 
%----------------------------------------------------------\

function EMGprocessing_Myodata_v0

global filteredResult rmsResult datalength 

%%-- read file
% filename = './data/biceps/biceps_emg_20ms_trial (11).txt';
filename = './data/triceps/triceps_emg_20ms_trial (41).txt';
fid = fopen(filename,'r');

N = 80; % need to be elaborated according to data length

datafieldspec = '%f   %f %f %f %f  %f %f %f %f  %f';
S_data = textscan(fid,datafieldspec);
fclose(fid);
%---------------------------------------------------------------------------\
% S_data{1,1} = time stamp, sampling rate ts = 20/1000 sec = 20ms
% S_data{1,2} -- S_data{1,9} = EMG ch1 -- EMG ch 8 value
% S_data{1,10}  = elbow angle
%---------------------------------------------------------------------------\
% Indexing example
% S{1,1}(1): The first time stamp = 1
% S{1,3}(10): EMG ch2 data at time 10x20ms [sec]
%---------------------------------------------------------------------------\

datalength = length(S_data{1,1});
% datalength = N;

ts = 0.020; % sampling time
numEMG = 8;
LPfiltered_EMG = zeros(numEMG,datalength);
movingRMS_EMG = zeros(numEMG,datalength);

for i=1:numEMG
    
    Voltage = ( S_data{1,2+i-1}-mean(S_data{1,2+i-1}(1:(round(datalength*0.1)))) );
    absVoltage = abs(Voltage);
    
    %% -- original data
    figure(1);
    plot(Voltage);
    % -- figure setting (safe to ignore this!)
    xAxis = ts*get(gca,'XTick');
    set(gca,'XTickLabel',xAxis);
%     set(gca,'YLim',[-1.5 1.5]);    
    strtitle = sprintf('original EMG%d',i);
    title(strtitle);
    xlabel('[sec]');
    ylabel('[v]')

    %% - processed data
    figure(2);
    % -- apply butterworth filter
    cutoff_freq = 30;
    butterWorthLP(absVoltage,cutoff_freq); 
    hf = plot(filteredResult,'g'); hold on;
    LPfiltered_EMG(i,:) = filteredResult;
    
    % -- moving RMS
    windowSize = 10;
    movingRMS(absVoltage,windowSize);
    hr = plot(rmsResult,'r'); hold off;
    movingRMS_EMG(i,:) = rmsResult;
    
    % -- figure setting (safe to ignore this!)
    xAxis = ts*get(gca,'XTick');
    set(gca,'XTickLabel',xAxis);
%     set(gca,'YLim',[-0.1 1.0]);
    set(gca,'YLim',[0 150]);
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
