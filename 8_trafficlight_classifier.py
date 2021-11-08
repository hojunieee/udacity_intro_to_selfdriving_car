#=========Loading and Visualizing the Traffic Light Dataset =========

import cv2 # computer vision library
import helpers # helper functions

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg # for loading in images

%matplotlib inline

# Image data directories
IMAGE_DIR_TRAINING = "traffic_light_images/training/"
IMAGE_DIR_TEST = "traffic_light_images/test/"

# Using the load_dataset function in helpers.py
# Load training data
IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TRAINING)



#=========Preprocessed Date =========

# This function should take in an RGB image and return a new, standardized version (32x32px.)
def standardize_input(image):
    
    #we need to copy the input before we rersize it 
    standard_im = np.copy(image)
    standard_im = cv2.resize(image, (32, 32))
    return standard_im
    

## TODO: One hot encode an image label Given a label - "red", "green", or "yellow" - return a one-hot encoded label
def one_hot_encode(label):
    ## TODO: Create a one-hot encoded label that works for all classes of traffic lights
    one_hot_encoded = [] 
    if label =="red":
        one_hot_encoded = [1, 0, 0]
    elif label =="yellow":
        one_hot_encoded = [0, 1, 0]
    else:
        one_hot_encoded = [0, 0, 1]        
    return one_hot_encoded


  def standardize(image_list):
    # Empty image data array
    standard_list = []

    # Iterate through all the image-label pairs
    for item in image_list:
        image = item[0]
        label = item[1]

        # Standardize the image
        standardized_im = standardize_input(image)

        # One-hot encode the label
        one_hot_label = one_hot_encode(label)    

        # Append the image, and it's one hot encoded label to the full, processed list of image data 
        standard_list.append((standardized_im, one_hot_label))
    return standard_list

  
# Standardize all training images
STANDARDIZED_LIST = standardize(IMAGE_LIST)


#=========Feature Extraction =========

# Convert and image to HSV colorspace
# Visualize the individual color channels

image_num = 1001
test_im = STANDARDIZED_LIST[image_num][0]
test_label = STANDARDIZED_LIST[image_num][1]

# Convert to HSV
hsv = cv2.cvtColor(test_im, cv2.COLOR_RGB2HSV)

# Print image label
print('Label [red, yellow, green]: ' + str(test_label))

# HSV channels
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]

# Plot the original image and the three channels
f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20,10))
ax1.set_title('Standardized image')
ax1.imshow(test_im)
ax2.set_title('H channel')
ax2.imshow(h, cmap='gray')
ax3.set_title('S channel')
ax3.imshow(s, cmap='gray')
ax4.set_title('V channel')
ax4.imshow(v, cmap='gray')



## TODO: Create a brightness feature that takes in an RGB image and outputs a feature (Must use HSV colorspace)
def create_feature(rgb_image): 
    ## TODO: Convert image to HSV color space
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)

    ## TODO: Create and return a feature value and/or vector
    feature = []
    v = hsv[:,:,2]

#optional
def create_feature2(rgb_image):
    r = rgb_image[:,:,0]
    g = rgb_image[:,:,1]
    b = rgb_image[:,:,2]

    # Visualize the individual color channels
    f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20,10))
    ax1.set_title('Red channel')
    ax1.imshow(r)
    ax2.set_title('Green channel')
    ax2.imshow(g)
    ax3.set_title('Blue channel')
    ax3.imshow(b)
    
