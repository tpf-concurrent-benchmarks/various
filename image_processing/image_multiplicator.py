'''
This programs multiplies the images in a folder,
to do so it opens all the images in folder_1 and saves the following in folder_2:
- The original image
- The image flipped horizontally
- The image flipped vertically
Then, from the images in folder_2 it saves the following in folder_3:
- The original image
- The image rotated 90 degrees
- The image rotated 180 degrees
- The image rotated 270 degrees
'''
import os
from PIL import Image

folder_1 = 'input'
folder_2 = 'folder_2'
folder_3 = 'folder_3'

# Create folder_2 and folder_3 if they don't exist
if not os.path.exists(folder_2):
    os.makedirs(folder_2)
if not os.path.exists(folder_3):
    os.makedirs(folder_3)
    
# Flip images in folder_1

for filename in os.listdir(folder_1):
    img = Image.open(f'{folder_1}/{filename}')
    raw_filename, extension = os.path.splitext(filename)
    
    flip_h = img.transpose(Image.FLIP_LEFT_RIGHT)
    flip_v = img.transpose(Image.FLIP_TOP_BOTTOM)
    
    img.save(f'{folder_2}/{raw_filename}_flip_0{extension}')
    flip_h.save(f'{folder_2}/{raw_filename}_flip_h{extension}')
    flip_v.save(f'{folder_2}/{raw_filename}_flip_v{extension}')

# Rotate images in folder_2

for filename in os.listdir(folder_2):
    img = Image.open(f'{folder_2}/{filename}')
    raw_filename, extension = os.path.splitext(filename)
    
    rotate_90 = img.transpose(Image.ROTATE_90)
    rotate_180 = img.transpose(Image.ROTATE_180)
    rotate_270 = img.transpose(Image.ROTATE_270)
    
    img.save(f'{folder_3}/{raw_filename}_rotate_0{extension}')
    rotate_90.save(f'{folder_3}/{raw_filename}_rotate_90{extension}')
    rotate_180.save(f'{folder_3}/{raw_filename}_rotate_180{extension}')
    rotate_270.save(f'{folder_3}/{raw_filename}_rotate_270{extension}')