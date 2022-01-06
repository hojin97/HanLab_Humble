import os
from pyunicorn.timeseries.surrogates import Surrogates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.seterr(invalid='ignore')

# dataset\bi에 이두근 데이터를 위치시키고 해당 폴더 안의 모든 파일을 읽어옴
# dataset\tri에 삼두근 데이터를 위치시키고 해당 폴더 안의 모든 파일을 읽어옴
for root, dirs, files in os.walk('./dataset/bi'):
    filename = []
    for fname in files:
        full_fname = os.path.join(root, fname)
        filename.append(full_fname)

for index, fn in enumerate(filename):
    with open(fn) as file:

        sp = []
        row = []

        for line in file:
            sp = line.rstrip().split('\t')

            if sp[0] == '' or sp[0] == "\n":
                pass
            else:
                row.append(list(map(float, sp[:3])))

        t = []
        data1 = []
        data2 = []

        for r in np.array(row):
            # r[0] = time
            t.append(r[0])
            # r[1] = rms
            data1.append(r[1])
            # r[2] = angle
            data2.append(r[2])
        print(data1)
        print(data2)
        td = np.array([])
        td = np.append(td, t, axis=0)
        td = np.vstack([td, data1])
        td = np.vstack([td, data2])


        # 하나의 데이터에 대해 AAFT(IAAFT) 를 100번 진행하여 100개의 뻥튀기 된 데이터를 생성 후 시각화를 진행 함
        for i in range(100):
            # AAFT
            d = Surrogates(original_data=td, silence_level=2).AAFT_surrogates(td)

            # IAAFT : refined_AAFT_surrogates(td,100) 에서 마지막 수 ( 여기서는 100 ) 이 IAAFT 의 iteration 을 의미함
            # d = Surrogates(original_data=td, silence_level=2).refined_AAFT_surrogates(td,100)

            rms = d[1]
            angle = d[2]

            count = len(rms)

            tIndex = np.linspace(0, count / 10, count)

            # Draw Line Graph
            plt.plot(tIndex, rms, tIndex, angle, 'r-')
            plt.axis('off')
            plt.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off',
                            labeltop='off', labelright='off', labelbottom='off')
            plt.show()
            plt.savefig('AAFT/LineGraph/Bi/linegraph_' + str(index * 100 + i) + '.png', pad_inches=0)
            plt.cla()
