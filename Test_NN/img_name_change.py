import os
import shutil

file_path = './valid_data/Bi/'
save_path = './valid_data/'
for root, dirs, files in os.walk(file_path):
    for file in files:
        shutil.copyfile(os.path.join(file_path, file), save_path+'Bi_'+file)

file_path = './valid_data/Tri/'
save_path = './valid_data/'
for root, dirs, files in os.walk(file_path):
    for file in files:
        shutil.copyfile(os.path.join(file_path, file), save_path + 'Tri_' + file)