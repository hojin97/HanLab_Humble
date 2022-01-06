from pyunicorn.timeseries.surrogates import Surrogates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from pyts.image import GramianAngularField

with open('Humble1205_2058_29.txt') as file:
    row = []
    for line in file:
        sp = line.strip().split('\t')
        row.append(list(map(float, sp[:3])))

row = np.array(row)

t = []
data1 = []
data2 = []
for r in row:
    t.append(r[0])
    data1.append(r[1])
    data2.append(r[2])

td = np.array([])
td = np.append(td, t, axis=0)
td = np.vstack([td, data1])
td = np.vstack([td, data2])

d = Surrogates(original_data=td, silence_level=2).AAFT_surrogates(td)
#d = Surrogates(original_data=td, silence_level=2).refined_AAFT_surrogates(td,10000)

data = [d[1], d[0]]
gasf = GramianAngularField(image_size=20, method='summation')
X_gasf = gasf.fit_transform(data)

fig = plt.figure(figsize=(8, 4))
grid = ImageGrid(fig, 111,
                 nrows_ncols=(1, 1),
                 axes_pad=0.15,
                 share_all=True
                 )

images = [X_gasf[0]]
for image, ax in zip(images, grid):
    im = ax.imshow(image, cmap='rainbow', origin='lower')
ax.cax.colorbar(im)
ax.cax.toggle_label(True)

plt.suptitle('Gramian Angular Summation Fields', y=0.98, fontsize=16)
plt.show()