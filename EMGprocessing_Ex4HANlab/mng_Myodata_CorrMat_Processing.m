clear all;
close all;
addpath('./export_fig-master/export_fig-master');  
% 'AAFT(4)','AAFT(5)'
AAFTList = {'AAFT(0)','AAFT(2)','AAFT(3)','AAFT(10)','AAFT(20)'};
MapList = {'hadamard'};
ExerciseList = {'rvcurl','hammer'};

for p=1:5    
    strAAFTnum = AAFTList{p};    
    for q=1:1
        strcmap = MapList{q};            
        for r=1:2
        strExercise = ExerciseList{r};    
        
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
            
%             for i=1:1
            for i=1:K
               Myodata_CorrMat_Processing(strExercise,i,strcmap,strAAFTnum ); 
            end        
        end
    end
end