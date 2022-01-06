from pyunicorn.timeseries.surrogates import Surrogates
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from pyts.image import GramianAngularField

# Biceps original data
def original_data_input(file_list, data_type, output_folder):
    create_folder('./' + output_folder + '/', output_folder)

    cnt = 0
    for file_name in file_list:
        sp = list()
        with open('./' + data_type + '/' + file_name) as file:
            row = []
            for line in file:
                if line == '\n':
                    break
                sp = line.strip().split('\t')
                row.append(list(map(float, sp[:3])))

        sp.clear()

        t = []
        rms = []
        angle = []
        for r in np.array(row):
            t.append(r[0])
            rms.append(r[1])
            angle.append(r[2])

        count = len(rms)

        tIndex = np.linspace(0, count / 10, count)

        plt.ylabel("Amplitude")
        plt.xlabel("Time [s]")
        plt.ylim(0, 180)
        plt.plot(tIndex, rms, tIndex, angle, 'r-')
        plt.savefig('./' + output_folder + '/' + str(cnt) + '.png')
        cnt += 1

        plt.cla()
        row.clear()

def original_gramian_data_input(file_list, data_type, output_folder, output_type):
    create_folder('./' + output_folder + '/', output_folder)

    cnt = 0
    for file_name in file_list:
        sp = list()
        with open('./' + data_type + '/' + file_name) as file:
            row = []
            for line in file:
                if line == '\n':
                    break
                sp = line.strip().split('\t')
                row.append(list(map(float, sp[:3])))

        sp.clear()

        d = [[],[],[]]

        for r in np.array(row):
            d[0].append(r[0])
            d[1].append(r[1])
            d[2].append(r[2])
        # d[0] : 시간
        # d[1] : RMS
        # d[2] : ANG
        if output_type == 'rms':
            data = [d[1], d[0]]
        elif output_type == 'angle':
            data = [d[2], d[0]]

        # Summation
        gasf = GramianAngularField(method='summation')
        X_gasf = gasf.fit_transform(data)

        # Difference
        # gadf = GramianAngularField(image_size=24, method='difference')
        # X_gadf = gadf.fit_transform(data)

        fig = plt.figure(figsize=(8, 4))
        grid = ImageGrid(fig, 111,
                         nrows_ncols=(1, 1),
                         axes_pad=0.15,
                         share_all=True,
                         cbar_location="right",
                         cbar_mode="single",
                         cbar_size="7%",
                         cbar_pad=0.3
                         )

        images = [X_gasf[0]]

        for image, ax in zip(images, grid):
            im = ax.imshow(image, cmap='rainbow', origin='lower')
        ax.cax.colorbar(im)
        ax.cax.toggle_label(True)

        plt.savefig('./' + output_folder + '/' + str(cnt) + '.png')
        cnt += 1

        plt.close()
        plt.cla()

# Biceps augmentation
def augmentation_line_graph_data(file_list, data_type, output_folder):
    create_folder('./' + output_folder + '/', output_folder)

    cnt = 1000
    for file_name in file_list:
        sp = list()
        with open('./'+data_type+'/' + file_name) as file:
            row = []
            for line in file:
                if line == '\n':
                    break
                sp = line.strip().split('\t')
                row.append(list(map(float, sp[:3])))

        sp.clear()

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

        # AAFT
        d = Surrogates(original_data=td, silence_level=2).AAFT_surrogates(td)

        # IAAFT
        # d = Surrogates(original_data=td, silence_level=2).refined_AAFT_surrogates(td,10000)

        rms = d[1]
        angle = d[2]

        count = len(rms)

        tIndex = np.linspace(0, count / 10, count)

        plt.ylabel("Amplitude")
        plt.xlabel("Time [s]")
        plt.ylim(0, 180)
        plt.plot(tIndex, rms, tIndex, angle, 'r-')
        plt.savefig('./'+output_folder+'/' + str(cnt) + '.png')
        cnt += 1

        plt.close()
        plt.cla()
        row.clear()

def augmentation_gramian_data(file_list, data_type, output_folder, output_type):
    create_folder('./' + output_folder + '/', output_folder)

    cnt = 10000
    for file_name in file_list:
        sp = list()
        with open('./' + data_type + '/' + file_name) as file:
            row = []
            for line in file:
                if line == '\n':
                    continue
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

        # ============  data augmentation ============= #
        # AAFT
        d = Surrogates(original_data=td, silence_level=2).AAFT_surrogates(td)

        # IAAFT
        # d = Surrogates(original_data=td, silence_level=2).refined_AAFT_surrogates(td,10000)

        # ============  Gramian ============= #
        # d[0] : 시간
        # d[1] : RMS
        # d[2] : ANG
        if output_type == 'rms':
            data = [d[1], d[0]]
        elif output_type == 'angle':
            data = [d[2], d[0]]

        # Summation
        gasf = GramianAngularField(method='summation')
        X_gasf = gasf.fit_transform(data)

        # Difference
        # gadf = GramianAngularField(image_size=24, method='difference')
        # X_gadf = gadf.fit_transform(data)

        fig = plt.figure(figsize=(8, 4))
        grid = ImageGrid(fig, 111,
                         nrows_ncols=(1, 1),
                         axes_pad=0.15,
                         share_all=True,
                         cbar_location="right",
                         cbar_mode="single",
                         cbar_size="7%",
                         cbar_pad=0.3
                         )

        images = [X_gasf[0]]

        for image, ax in zip(images, grid):
            im = ax.imshow(image, cmap='rainbow', origin='lower')
        ax.cax.colorbar(im)
        ax.cax.toggle_label(True)

        plt.savefig('./' + output_folder + '/' + str(cnt) + '.png')
        cnt += 1

        plt.close()
        plt.cla()

def create_folder(filepath, folder_name):
    try:
        if not os.path.exists(filepath):
            os.makedirs(folder_name)
    except OSError:
        print('Error')

def main():
    # Biceps
    path_dir1 = 'C:/Users/Hojin/Desktop/Prj.HomePT/pyunicorn/data_2do'
    file_list1 = os.listdir(path_dir1)

    original_data_input(file_list1, 'data_2do', 'original_2do')
    original_gramian_data_input(file_list1, 'data_2do', 'gramian_original_rms_2do', 'rms')
    original_gramian_data_input(file_list1, 'data_2do', 'gramian_original_ang_2do', 'angle')
    augmentation_line_graph_data(file_list1, 'data_2do', 'line_graph_2do')
    augmentation_gramian_data(file_list1, 'data_2do', 'gramian_aug_rms_2do', 'rms')
    augmentation_gramian_data(file_list1, 'data_2do', 'gramian_aug_ang_2do', 'angle')

    # Triceps
    path_dir2 = 'C:/Users/Hojin/Desktop/Prj.HomePT/pyunicorn/data_3do'
    file_list2 = os.listdir(path_dir2)

    original_data_input(file_list2, 'data_3do', 'original_3do')
    original_gramian_data_input(file_list2, 'data_3do', 'gramian_original_rms_3do', 'rms')
    original_gramian_data_input(file_list2, 'data_3do', 'gramian_original_ang_3do', 'angle')
    augmentation_line_graph_data(file_list2, 'data_3do', 'line_graph_3do')
    augmentation_gramian_data(file_list2, 'data_3do', 'gramian_aug_rms_3do', 'rms')
    augmentation_gramian_data(file_list2, 'data_3do', 'gramian_aug_ang_3do', 'angle')

    print("Finished")

main()




