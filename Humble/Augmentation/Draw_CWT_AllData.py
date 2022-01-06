import os
from pyunicorn.timeseries.surrogates import Surrogates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pywt

for root, dirs, files in os.walk('dataset/tri'):
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
            t.append(r[0])
            data1.append(r[1])
            data2.append(r[2])

        td = np.array([])
        td = np.append(td, t, axis=0)
        td = np.vstack([td, data1])
        td = np.vstack([td, data2])

        for i in range(100):
            # AAFT
            d = Surrogates(original_data=td, silence_level=2).AAFT_surrogates(td)

            # IAAFT
            # d = Surrogates(original_data=td, silence_level=2).refined_AAFT_surrogates(td,10000)

            # ============  CWT Scalogram ============= #

            at = np.linspace(0, 2, 20, endpoint=False)
            asig = d[1]
            asigA = d[2]
            awidths = np.arange(1, 20)

            # ============  rms 로 CWT Scalogram 그리는 경우 ============= #
            acwtmatr, afreqs = pywt.cwt(asig, awidths, 'mexh')

            plt.imshow(acwtmatr, extent=[0, 2, 1, 20], cmap='rainbow', aspect='auto', vmax=abs(acwtmatr).max(),
                       vmin=-abs(acwtmatr).max())  # doctest: +SKIP
            plt.savefig('AAFT\CWT\Tri\RMS\CWT_' + str(index * 100 + i) + '.png', pad_inches=0)  # doctest: +SKIP
            plt.cla()

            # ============  angle 로 CWT Scalogram 그리는 경우 ============= #
            acwtmatr, afreqs = pywt.cwt(asigA, awidths, 'mexh')

            plt.imshow(acwtmatr, extent=[0, 2, 1, 20], cmap='rainbow', aspect='auto', vmax=abs(acwtmatr).max(),
                       vmin=-abs(acwtmatr).max())  # doctest: +SKIP
            plt.savefig('AAFT\CWT\Tri\Angle\CWT_' + str(index * 100 + i) + '.png', pad_inches=0)  # doctest: +SKIP

            plt.cla()
            plt.close('all')

