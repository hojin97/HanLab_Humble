import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import os

def butter_worth_LP(data, cutoff_freq, fs, order=4):
    n_cutoff = cutoff_freq / (fs / 2)
    b, a = butter(order, n_cutoff, 'low')
    y = filtfilt(b, a, data)
    return y

def moving_RMS(data, window_size):
    temp = np.power(data, 2)
    window = np.ones(window_size)/float(window_size)
    return np.sqrt(np.convolve(temp, window, 'same'))

# EMG Processing Myo data per 1 ch
def EMG_processing():
    filename = "./data/biceps/biceps_emg_20ms_trial (1).txt"

    ## File read
    fid = open(filename, 'r')

    data = []
    for data_list in fid:
        temp = []
        for val in data_list.split():
            temp.append(float(val))
        data.append(temp.copy())
    data = np.array(data)
    fid.close()

    ## Parameter
    data_length = len(data)
    fs = 50
    emg_ch = 8

    LP_filltered_EMG = np.zeros((emg_ch, data_length))
    moving_RMS_EMG = np.zeros((emg_ch, data_length))
    # ********* ********* *********

    for i in range(1,emg_ch):
        avg = (data[1:round(data_length * 0.1), i])
        Voltage = (data[:,i] - np.mean(avg))
        abs_Voltage = abs(Voltage)

        ## Draw original data
        plt.figure(1)
        plt.plot(Voltage)
        plt.xlabel('[sec]')
        plt.ylabel('[v]')
        #plt.show()

        ## Draw processed data
        plt.figure(2)

        ## Filter - butterworth
        cutoff_freq = 7.5
        hf = butter_worth_LP(abs_Voltage, cutoff_freq, fs)
        plt.plot(hf, 'g')
        LP_filltered_EMG[i, :] = hf

        ## Moving RMS
        window_size = 10
        hr = moving_RMS(abs_Voltage, window_size)
        plt.plot(hr, 'r')
        moving_RMS_EMG[i, :] = hr

        ## set figure
        plt.xlabel('[sec]')
        plt.ylabel('[v]')
        plt.ylim([0, 150])
        plt.legend()
        plt.show()

# EMG Processing Myo data per 8 ch
def EMG_processing_all(file_path, save_path, numbering):
    ## File read
    fid = open(file_path, 'r')

    data = []
    for data_list in fid:
        temp = []
        for val in data_list.split():
            temp.append(float(val))
        data.append(temp.copy())
    data = np.array(data)
    fid.close()

    ## Parameter
    data_length = len(data)
    fs = 50
    emg_ch = 8
    color = ['r', 'g', 'b', 'y', 'm', 'c', 'gold', 'slategray']

    LP_filltered_EMG = np.zeros((emg_ch, data_length))
    moving_RMS_EMG = np.zeros((emg_ch, data_length))
    # ********* ********* *********

    plt.figure(0)
    plt.plot(data[:, 9]/181)
    plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off',
                    labeltop='off', labelright='off', labelbottom='off')
    plt.ylim([0, 1])
    plt.savefig(save_path + '/Angle/' + numbering + '.png', pad_inches=0)
    plt.cla()
    #plt.show()

    for i in range(1,emg_ch):
        avg = (data[1:round(data_length * 0.1), i])
        Voltage = (data[:,i] - np.mean(avg))
        ## Draw original data
        plt.figure(1)
        plt.plot(Voltage, color[i])
        plt.ylim([0, 180])
        #plt.xlabel('[sec]')
        #plt.ylabel('[v]')
        #plt.show()
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off',
                    labeltop='off', labelright='off', labelbottom='off')
    plt.savefig(save_path + '/EMG_ch8/' + numbering + '.png', pad_inches=0)
    plt.cla()

    for i in range(1, emg_ch):
        avg = (data[1:round(data_length * 0.1), i])
        Voltage = (data[:, i] - np.mean(avg))
        abs_Voltage = abs(Voltage) / 213

        #abs_Voltage = abs_Voltage/max(Voltage)

        ## Filter - butterworth
        plt.figure(2)
        #plt.title('Butterworth filter')
        cutoff_freq = 7.5
        hf = butter_worth_LP(abs_Voltage, cutoff_freq, fs)
        plt.plot(hf, color[i])
        LP_filltered_EMG[i, :] = hf

        #plt.xlabel('[sec]')
        #plt.ylabel('[v]')
        plt.ylim([0, 1])
        #plt.legend('12345678')
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off',
                        labeltop='off', labelright='off', labelbottom='off')
    plt.savefig(save_path+'/Butterworth/' + numbering + '.png', pad_inches=0)
    plt.cla()

    for i in range(1, emg_ch):
        avg = (data[1:round(data_length * 0.1), i])
        Voltage = (data[:, i] - np.mean(avg))
        abs_Voltage = abs(Voltage) / 213
        ## Moving RMS
        plt.figure(3)
        #plt.title('Moving RMS')
        window_size = 10
        hr = moving_RMS(abs_Voltage, window_size)
        plt.plot(hr, color[i])
        moving_RMS_EMG[i, :] = hr

        #plt.xlabel('[sec]')
        #plt.ylabel('[v]')
        plt.ylim([0, 1])
        #plt.legend('12345678')
        plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off',
                        labeltop='off', labelright='off', labelbottom='off')
    plt.savefig(save_path+'/Moving_RMS/' + numbering + '.png', pad_inches=0)
    plt.cla()


for root, dir, files in os.walk('./data/biceps'):
    for i, file in enumerate(files):
        file_path = './data/biceps/'+file
        save_path = './Image/Bi'
        EMG_processing_all(file_path, save_path, str(i))

for root, dir, files in os.walk('./data/triceps'):
    for i, file in enumerate(files):
        file_path = './data/triceps/'+file
        save_path = './Image/Tri'
        EMG_processing_all(file_path, save_path, str(i))
