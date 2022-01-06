import os
from pyunicorn.timeseries.surrogates import Surrogates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from pyts.image import GramianAngularField

np.seterr(invalid='ignore')

# dataset\bi에 이두근 데이터를 위치시키고 해당 폴더 안의 모든 파일을 읽어옴
# dataset\tri에 삼두근 데이터를 위치시키고 해당 폴더 안의 모든 파일을 읽어옴
for root, dirs, files in os.walk('dataset/bi'):
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
            # d = Surrogates(original_data=td, silence_level=2).refined_AAFT_surrogates(td,100)

            # ============  Gramian ============= #

            # ============  rms 로 Gramian 그리는 경우 ============= #
            data = [d[1], d[0]]

            # Summation
            gasf = GramianAngularField(image_size=18, method='summation')
            X_gasf = gasf.fit_transform(data)

            # Difference
            # gadf = GramianAngularField(image_size=24, method='difference')
            # X_gadf = gadf.fit_transform(data)

            fig = plt.figure(figsize=(8, 4))
            grid = ImageGrid(fig, 111,
                             nrows_ncols=(1, 1),
                             share_all=True)

            images = [X_gasf[0]]

            for image, ax in zip(images, grid):
                im = ax.imshow(image, cmap='rainbow', origin='lower')
            ax.cax.toggle_label(True)

            ax.axis('off')
            ax.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off',
                           labeltop='off', labelright='off', labelbottom='off')
            plt.savefig('AAFT\Gramian\Bi\RMS\Gramian_' + str(index * 100 + i) + '.png', pad_inches=0)
            plt.cla()
            plt.close('all')

            # ============  angle 로 Gramian 그리는 경우 ============= #
            data = [d[2], d[0]]

            # Summation
            gasf = GramianAngularField(image_size=18, method='summation')
            X_gasf = gasf.fit_transform(data)

            # Difference
            # gadf = GramianAngularField(image_size=24, method='difference')
            # X_gadf = gadf.fit_transform(data)

            fig = plt.figure(figsize=(8, 4))
            grid = ImageGrid(fig, 111,
                             nrows_ncols=(1, 1),
                             share_all=True)

            images = [X_gasf[0]]

            for image, ax in zip(images, grid):
                im = ax.imshow(image, cmap='rainbow', origin='lower')
            ax.cax.toggle_label(True)

            ax.axis('off')
            ax.tick_params(axis='both', left='off', top='off', right='off', bottom='off', labelleft='off',
                           labeltop='off', labelright='off', labelbottom='off')
            plt.savefig('AAFT/Gramian/Bi/Angle/Gramian_' + str(index * 100 + i) + '.png', pad_inches=0)
            plt.cla()
            plt.close('all')