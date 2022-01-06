clear all;
close all;
addpath('./export_fig-master/export_fig-master');  

% ColormapList = {'jet','bone'};
strcmap = 'jet';
ExerciseList = {'hammer','rvcurl'};
AAFTList = {'AAFT(0)','AAFT(2)','AAFT(3)','AAFT(4)','AAFT(5)','AAFT(10)','AAFT(20)'};

for p=2:7
    strAAFTnum = AAFTList{p};    
    for q=1:2
        strExercise = ExerciseList{q};
        switch strAAFTnum
            case 'AAFT(0)'
                K = 60;
            case 'AAFT(2)'
                K = 120;
            case 'AAFT(3)'
                K = 180;
            case 'AAFT(4)'
                K = 240;    
            case 'AAFT(5)'
                K = 300;    
            case 'AAFT(10)'
                K = 600;
            case 'AAFT(20)'
                K = 1200;
        end
%         for i=1:2
        for i=1:K
           Myodata_All_Vectorizing(strExercise,i,strcmap,strAAFTnum ); 
           Myodata_All_Vectorizing_midAng(strExercise,i,strcmap,strAAFTnum ); 
        end        
    end
end