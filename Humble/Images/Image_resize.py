import os
from PIL import Image

def resize_image(image_path, save_path):
    image = Image.open(image_path)
    after_img = image.resize((227,227))
    after_img.save(save_path+'.png')

img_type = ['I_easy', 'I_fair']

categori = ['Biceps', 'Triceps', 'Hammer', 'Rvcurl']
for folder in img_type:
    for ca in categori:
        base_path = './AAFT_0/'+ca+'/'
        save_path = '../Data/resultVecsFigs/AAFT_0/'+ca+'/'
        for top, dir, files in os.walk(base_path + folder):
            for i, file in enumerate(files):
                resize_image(base_path + folder + '/' + file, save_path + folder + '/' + str(i))


#resize_image()