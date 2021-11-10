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



## TODO: Create a brightness feature that takes in an RGB image and outputs a feature vector and/or value
## This feature should use HSV colorspace values
def create_feature(rgb_image): 
    #Define default feature to red to be safe
    feature="red"
    
    # TODO: Convert image to HSV color space
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    v = hsv[:,:,2]
    
    #1. mask the image and remove traffic light box
    masked_image = remove_traffic_box(rgb_image)
    #plt.imshow(masked_image)
    
    #2. crop the image
    cropped=crop_that_image(masked_image)
    plt.imshow(cropped)
    #If the traffic light box was not detected, just return red light
    h, w, c = cropped.shape
    if h==0 or w==0:
        return feature
    
    #3. Check both filters and label the feature
    if properly_cropped(cropped):
        if check_location(cropped)in check_color(cropped):
            feature = check_location(cropped)
    else:
        if check_location(cropped)in check_color(cropped):
            feature = check_location(cropped)
    return feature

    
#=====================helper code=====================
def remove_traffic_box(rgb_image):
    #Convert rgb into hsv
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    #get the value pixels
    v = hsv[:,:,2]
    #Set the range for the value filter
    lower_v = np.array([160]) 
    upper_v = np.array([255])
    # Define the masked area
    mask = cv2.inRange(v, lower_v, upper_v)
    masked_image = np.copy(rgb_image)
    masked_image[mask == 0] = [0]
    return masked_image
    

def crop_that_image(rgb_image):
    # Make a copy of the image to manipulate
    image_crop = np.copy(rgb_image)
    #Convert rgb into hsv
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    #get the value pixels
    v = hsv[:,:,2]
    #Define boudaries 
    LB=0
    UB=0
    RB=31
    DB=31
    
    #Find the left boundary
    for x in range(31):
        if horizontal_cut(v,x):
            LB=x
            break
    #Find the right boundary
    for x in range(31,0,-1):
        if horizontal_cut(v,x):
            RB=x
            break
    #Find upper boundary
    for y in range(31):
        if vertical_cut(v,y):
            UB=y
            break
    #Find down(lower) boundary
    for y in range(31,0,-1):
        if vertical_cut(v,y):
            DB=y
            break
    
    if UB>=DB or LB>=RB:
        LB=UB=0
        RB=DB=0
    
    # Using image slicing, subtract the row_crop from top/bottom and col_crop from left/right
    image_crop = rgb_image[UB:DB, LB:RB, :]
    
    return image_crop


def horizontal_cut(matrix,X):
    maxstreak=0
    index=0
    streak=0
    while index<32:
        if matrix[index][X]==0:
            streak=streak+1
            index=index+1
        else:
            maxstreak=max(maxstreak,streak)
            streak=0
            index=index+1
    if maxstreak>15:
        return True
    else:
        return False
    
    
def vertical_cut(matrix,Y):
    maxstreak=0
    index=0
    streak=0
    while index<32:
        if matrix[Y][index]==0:
            streak=streak+1
            index=index+1
        else:
            maxstreak=max(maxstreak,streak)
            streak=0
            index=index+1
    
    if maxstreak>10:
        return True
    else:
        return False
    

def properly_cropped(rgb_image):
    height=len(rgb_image)
    width=len(rgb_image[0])
    area=height*width
    lighted_pixel_counter=0
    #Check if the masked area is more than 50%
    for y in range(height):
        for x in range(width):
            if v[y][x]!=0:
                lighted_pixel_counter=lighted_pixel_counter+1
    if lighted_pixel_counter/area >0.5:
        return False
    else:
        return True
    
    
def check_location(rgb_image):
    #Set the default color to red to be safe
    color="red"
    height=len(rgb_image)
    width=len(rgb_image[0])
    lighted_pixel_location=list()
    # Make a copy of the image to manipulate
    image_crop = np.copy(rgb_image)
    #Convert rgb into hsv
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    #Get the value pixels
    v = hsv[:,:,2]
    #Take an average of the y-location where it hasn't been masked
    for y in range(height):
        for x in range(width):
            if v[y][x]!=0:
                lighted_pixel_location.append(y)
    ave_lighted=np.average(lighted_pixel_location)
    #label it!
    if ave_lighted > 2*height/3:
        color="green"
    elif ave_lighted > height/3:
        color="yellow"
    return color


def check_color(rgb_image):
    #Since yellow is vague, just put it as a default
    color=['yellow']
    height=len(rgb_image)
    width=len(rgb_image[0])
    
    
    # Make a copy of the image to manipulate
    image_crop = np.copy(rgb_image)
    #Convert rgb into hsv
    hsv = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2HSV)
    #Get the value pixels
    v = hsv[:,:,2]
    
    
    #Get average RGB values
    average_RGB = []
    lighted_pixel = []    
    for y in range(height):
        for x in range(width):
            if v[y][x]!=0:
                lighted_pixel.append(image_crop[y][x])
                
    average_RGB = np.average(lighted_pixel, axis=0)
    aveR=average_RGB[0]
    aveG=average_RGB[1]
    aveB=average_RGB[2]
    
    if type(average_RGB)!=list:
        return ['red']
    
    if aveR>200:
        color.append('red')
    if aveG>200:
        color.append('green')
        
    return color
