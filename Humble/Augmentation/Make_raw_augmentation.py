import os
from pyunicorn.timeseries.surrogates import Surrogates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file_index = 0
type = 'Hammer'
iterative = 4
base_folder = 'hammer'
save_folder = 'Raw_data_4'

for root, dirs, files in os.walk('../EMG_Processing/data/'+base_folder):
    filename = []
    for file in files:
        full_fname = os.path.join(root, file)
        filename.append(full_fname)

for index, fn in enumerate(filename):
    with open(fn, 'r') as file:
        sp = []
        row = []

        for line in file:
            sp = line.rstrip().split()
            if sp[0] == '' or sp[0] == '\n':
                pass
            else:
                row.append(list(map(float, sp[:])))

        time = []
        ch = [[],[],[],[],[],[],[],[]]
        angle = []

        for r in np.array(row):
            time.append(r[0])
            ch[0].append(r[1])
            ch[1].append(r[2])
            ch[2].append(r[3])
            ch[3].append(r[4])
            ch[4].append(r[5])
            ch[5].append(r[6])
            ch[6].append(r[7])
            ch[7].append(r[8])
            angle.append(r[9])
        td = np.array([])
        td = np.append(td, time, axis=0)
        for i in range(8):
            td = np.vstack([td, ch[i]])
        td = np.vstack([td, angle])

        for i in range(iterative):
            file_index += 1
            d = Surrogates(original_data=td, silence_level=2).AAFT_surrogates(td)

            fw = open('../Data/'+save_folder+'/'+type+'/'+str(file_index)+'.txt', 'w')
            for num in range(len(d[0])):
                fw.write(str(num)+"\t"+str(d[1][num])+"\t"+str(d[2][num])+"\t"+str(d[3][num])+"\t"+str(d[4][num])+"\t"+
                      str(d[5][num])+"\t"+str(d[6][num])+"\t"+str(d[7][num])+"\t"+str(d[8][num])+"\t"+str(d[9][num])+"\n")

