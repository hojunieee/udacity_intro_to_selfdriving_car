import numpy as np
import matplotlib.image as mpimg  # for reading in images

import matplotlib.pyplot as plt
import cv2  # computer vision library

%matplotlib inline

# Read in the image
image = mpimg.imread('images/waymo_car.jpg')

# Print out the image dimensions
print('Image dimensions:', image.shape)

# Change from color to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

plt.imshow(gray_image, cmap='gray')



## TODO: Define the color selection boundaries in HSV values

## TODO: Define the masked area and mask the image
# Don't forget to make a copy of the original image to manipulate

lower_h = np.array([10]) 
upper_h = np.array([80])

# Define the masked area
mask2 = cv2.inRange(h, lower_h, upper_h)

masked_image2 = np.copy(image)
masked_image2[mask2 != 0] = [0]

# Display it!
plt.imshow(masked_image2)





# Image data directories
image_dir_training = "day_night_images/training/"
image_dir_test = "day_night_images/test/"

# Using the load_dataset function in helpers.py
# Load training data
IMAGE_LIST = helpers.load_dataset(image_dir_training)

# Print out 1. The shape of the image and 2. The image's label

# Select an image and its label by list index
image_index = 0
selected_image = IMAGE_LIST[image_index][0]
selected_label = IMAGE_LIST[image_index][1]

# Display image and data about it
plt.imshow(selected_image)
print("Shape: "+str(selected_image.shape))
print("Label: " + str(selected_label))


# This function should take in an RGB image and return a new, standardized version
def standardize_input(image):
    
    ## TODO: Resize image so that all "standard" images are the same size 600x1100 (hxw) 
    standard_im = cv2.resize(image, (600, 1100))

    return standard_im
    
# Examples: 
# encode("day") should return: 1
# encode("night") should return: 0


def encode(label):
        
    numerical_val = 0
    ## TODO: complete the code to produce a numerical label
    if label == "day":
        numerical_val=1
    elif label == "night":
        numerical_val=0
    else:
        return "error"
    return numerical_val

  
def standardize(image_list):
    
    # Empty image data array
    standard_list = []

    # Iterate through all the image-label pairs
    for item in image_list:
        image = item[0]
        label = item[1]

        # Standardize the image
        standardized_im = standardize_input(image)

        # Create a numerical label
        binary_label = encode(label)    

        # Append the image, and it's one hot encoded label to the full, processed list of image data 
        standard_list.append((standardized_im, binary_label))
        
    return standard_list
  
# Standardize all training images
STANDARDIZED_LIST = standardize(IMAGE_LIST)


# Display a standardized image and its label

# Select an image by index
image_num = 0
selected_image = STANDARDIZED_LIST[image_num][0]
selected_label = STANDARDIZED_LIST[image_num][1]

# Display image and data about it
## TODO: Make sure the images have numerical labels and are of the same size
plt.imshow(selected_image)
print("Shape: "+str(selected_image.shape))
print("Label [1 = day, 0 = night]: " + str(selected_label))
