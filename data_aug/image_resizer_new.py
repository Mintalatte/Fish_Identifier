import numpy as np
from PIL import Image
import os
from os import listdir

camera_height = 1944
camera_width = 2592
shrinking = 4
target_height = int(camera_height / shrinking)
target_width = int(camera_width / shrinking)

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
    # if smaller, then expand
    if (max(orig_shape[0] - target_height, orig_shape[1] - target_width) <= 0):
        alpha_height = target_height / orig_shape[0]
        alpha_width = target_width / orig_shape[1]
        # expanding using PIL  
        # print("expanding")
        if (alpha_height > alpha_width):
            new_image = rgb_image.resize(( int(alpha_width * orig_shape[1]), int(alpha_width * orig_shape[0]) ))
        else:
            new_image = rgb_image.resize(( int(alpha_height * orig_shape[1]), int(alpha_height * orig_shape[0]) ))
    # if larger. then shrink
    else:
        alpha_height = target_height / orig_shape[0]
        alpha_width = target_width / orig_shape[1]
        # shrinking using PIL 
        # print("shrinking")
        if (alpha_height > alpha_width):
            new_image = rgb_image.resize(( int(alpha_width * orig_shape[1]), int(alpha_width * orig_shape[0]) ))
        else:
            new_image = rgb_image.resize(( int(alpha_height * orig_shape[1]), int(alpha_height * orig_shape[0]) ))
    
    # print(new_image.size)
    # Filling with self-written function 
    new_array_image = np.array(new_image)
    resized_rgb_image = np.zeros((target_height, target_width, 3))
    
    # print(target_height, target_width)
    
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
            formatted_image.save("../dataset/" + folder_path + "_fixed/" + str(counter) + '.png', 'png')
            counter += 1
            # print(counter)
        else:
            print("ERROR: ", images_name)
    return 1

multiple_image_RGB_resize("Pomfret")
print("Pomfret done")
multiple_image_RGB_resize("SilverCarp")
print("SilverCarp done")

# test_image = np.array([[1,2,3],[4,5,6],[7,8,9]])
# test_result = single_image_resize(test_image)
# print("test input image:")
# print(test_image)
# print("output for a standard size of 9 * 9")
# print(test_result)