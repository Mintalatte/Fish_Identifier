import numpy as np
from PIL import Image
import os
from os import listdir

target_height = 1944
target_width = 2592

test_image_height = target_height * 1
test_image_width = target_width * 2

# target_height = 9
# target_width = 9

# test_image_height = 5
# test_image_width = 6

def single_image_resize(partial_image_frame):
    image_orig_size = partial_image_frame.shape
    # fixing unmatched size due to rounding   
    if (image_orig_size[1] < target_width):
        right_col = partial_image_frame[:, -1]
        right_col = right_col[:, np.newaxis]   
        right_cols = np.tile(right_col, (1, target_width - image_orig_size[1]))
        partial_image_frame = np.concatenate((partial_image_frame, right_cols), 1)
    if (image_orig_size[0] < target_height):
        bottom_row = partial_image_frame[-1, :]
        bottom_rows = np.tile(bottom_row, (target_height - image_orig_size[0],1))        
        partial_image_frame = np.concatenate((partial_image_frame, bottom_rows), 0)
    image_frame = partial_image_frame
    # print("Single reshaping done. Current shape:", image_frame.shape, "\n")
    return image_frame
    
def single_image_RGB_resize(png_image, counter, folder_path):
    rgb_image = png_image.convert("RGB")
    array_image = np.array(rgb_image)
    
    orig_shape = array_image.shape
    alpha_height = target_height / orig_shape[0]
    alpha_width = target_width / orig_shape[1]
    
    # expanding using PIL 
    if (alpha_height > alpha_width):
        new_image = rgb_image.resize(( int(alpha_width * orig_shape[1]), int(alpha_width * orig_shape[0]) ))
        print(new_image.size)
    else:
        new_image = rgb_image.resize(( int(alpha_height * orig_shape[1]), int(alpha_height * orig_shape[0]) ))
        print(new_image.size)
    
    # Filling with self-written function 
    new_array_image = np.array(new_image)
    resized_rgb_image = np.zeros((target_height, target_width, 3))
    
    resized_rgb_image[:,:,0] = single_image_resize(new_array_image[:,:,0])
    resized_rgb_image[:,:,1] = single_image_resize(new_array_image[:,:,1])
    resized_rgb_image[:,:,2] = single_image_resize(new_array_image[:,:,2])
    
    return resized_rgb_image

def multiple_image_RGB_resize(folder_path):
    counter = 0
    for images_name in os.listdir(folder_path):
        if (images_name.endswith(".png")):
            png_image = Image.open (folder_path + "/" + images_name)
            
            
            resized_rgb_array = single_image_RGB_resize(png_image, counter, folder_path)
            
            formated_resized = resized_rgb_array.astype(np.uint8)
            formatted_image = Image.fromarray(formated_resized, 'RGB')
            formatted_image.save(folder_path + "_fixed/" + str(counter) + '.png', 'png')
            counter += 1
            print(counter)
        else:
            print("ERROR")
    return 1

multiple_image_RGB_resize("Pomfret")
multiple_image_RGB_resize("SilverCarp")


# test_image = np.array([[1,2,3],[4,5,6],[7,8,9]])
# test_result = single_image_resize(test_image)
# print("test input image:")
# print(test_image)
# print("output for a standard size of 9 * 9")
# print(test_result)