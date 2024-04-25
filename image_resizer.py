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

def single_image_resize(image):
    image_orig_size = image.shape
    alpha_height = image_orig_size[0] / target_height
    alpha_width = image_orig_size[1] / target_width
    print("Original alphas:", alpha_height, alpha_width)
    
    # if too tall, duplicate right most column
    if (alpha_width < alpha_height):
        right_col = image[:, -1]
        right_col = right_col[:, np.newaxis]   
        right_cols = np.tile(right_col, (1, int(target_width * alpha_height)-image_orig_size[1]))
        reshaped_image = np.concatenate((image, right_cols), 1)
        print("Larger height fixe, currently shape:", reshaped_image.shape, "current alphas:", np.array(reshaped_image.shape)/(target_height,target_width))
    # if too wide, duplicate bottom most row
    elif (alpha_width > alpha_height):
        bottom_row = image[-1, :]
        bottom_rows = np.tile(bottom_row, (int(target_height * alpha_width)-image_orig_size[0],1))        
        reshaped_image = np.concatenate((image, bottom_rows), 0)
        print("Larger width fixed. Current shape:", reshaped_image.shape, "current alphas:", np.array(reshaped_image.shape)/(target_height,target_width))
    else:
        reshaped_image = image
    
    # determining whether to shrink or to expand
    fixed_alpha = reshaped_image.shape[0] / target_height
    image_frame = np.zeros((target_height, target_width))
    
    # expanding for a small image
    if (fixed_alpha < 1):
        alpha_floor = np.floor(1 / fixed_alpha)
        partial_image_frame_height = int(reshaped_image.shape[0] * alpha_floor)
        partial_image_frame_width = int(reshaped_image.shape[1] * alpha_floor)
        partial_image_frame = np.zeros((partial_image_frame_height, partial_image_frame_width))
        for row_loop in range(partial_image_frame_height):
            for col_loop in range(partial_image_frame_width):
                partial_image_frame[row_loop][col_loop] = reshaped_image[int(np.floor(row_loop / alpha_floor))][int(np.floor(col_loop / alpha_floor))]
        print("Expanding finished, current shape:", partial_image_frame.shape)
    # shrinking for a large image
    elif (fixed_alpha > 1):
        alpha_ceil = int(np.ceil(fixed_alpha))
        partial_image_frame_height = int(np.floor(reshaped_image.shape[0]/ alpha_ceil))
        partial_image_frame_width = int(np.floor(reshaped_image.shape[1]/ alpha_ceil))
        partial_image_frame = np.zeros((partial_image_frame_height, partial_image_frame_width))
        
        for row_loop in range(partial_image_frame_height):
            for col_loop in range(partial_image_frame_width):
                grid_sum = 0
                for orig_row_loop in range(row_loop * alpha_ceil, (row_loop + 1) * alpha_ceil):
                    for orig_col_loop in range(col_loop * alpha_ceil, (col_loop + 1) * alpha_ceil):
                        grid_sum += reshaped_image[orig_row_loop][orig_col_loop]
                grid_avg = grid_sum / alpha_ceil
                partial_image_frame[row_loop][col_loop] = grid_avg
        print("Shrinking finished, current shape:", partial_image_frame.shape, "alpha:", fixed_alpha)
    # simply copying for a nearly matched image
    else:
        partial_image_frame = reshaped_image
        partial_image_frame_height = reshaped_image.shape[0]
        partial_image_frame_width = reshaped_image.shape[1]
    
    # fixing unmatched size due to rounding   
    if (partial_image_frame_width < target_width):
        right_col = partial_image_frame[:, -1]
        right_col = right_col[:, np.newaxis]   
        right_cols = np.tile(right_col, (1, target_width - partial_image_frame_width))
        partial_image_frame = np.concatenate((partial_image_frame, right_cols), 1)
    if (partial_image_frame_height < target_height):
        bottom_row = partial_image_frame[-1, :]
        bottom_rows = np.tile(bottom_row, (target_height - partial_image_frame_height,1))        
        partial_image_frame = np.concatenate((partial_image_frame, bottom_rows), 0)
    image_frame = partial_image_frame
    print("Single reshaping done. Current shape:", image_frame.shape, "\n")
    return image_frame
    
def single_image_RGB_resize(rgb_image_array):
    resized_rgb_image = np.zeros((target_height, target_width, 3))
    
    print(rgb_image_array.shape)
    
    resized_rgb_image[:,:,0] = single_image_resize(rgb_image_array[:,:,0])
    resized_rgb_image[:,:,1] = single_image_resize(rgb_image_array[:,:,1])
    resized_rgb_image[:,:,2] = single_image_resize(rgb_image_array[:,:,2])
    
    return resized_rgb_image

def multiple_image_RGB_resize(folder_path):
    counter = 0
    for images_name in os.listdir(folder_path):
        if (images_name.endswith(".png")):
            png_image = Image.open (folder_path + "/" + images_name)
            rgb_image = png_image.convert("RGB")
            array_image = np.array(rgb_image)
            print("Image name:", images_name, "Image shape:", array_image.shape)
            resized_rgb_array = single_image_RGB_resize(array_image)
            counter += 1
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