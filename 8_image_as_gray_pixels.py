import numpy as np
import matplotlib.image as mpimg  # for reading in images

import matplotlib.pyplot as plt
import cv2  # computer vision library

%matplotlib inline



# Read in the image
image = mpimg.imread('images/car_green_screen.jpg')

# Print out the image dimensions (height, width, and depth (color))
print('Image dimensions:', image.shape)

# Display the image
plt.imshow(image)

# Define our color selection boundaries in RGB values
lower_green = np.array([0,180,0]) 
upper_green = np.array([100,255,100])



# Define the masked area
mask = cv2.inRange(image, lower_green, upper_green)
#This is outside the car (where the G-values lie between 180-255)

# Vizualize the mask
plt.imshow(mask, cmap='gray')



# Mask the image to let the car show through
masked_image = np.copy(image)

#Turn area that is not zero in the mask, aka outside the car, into [0,0,0] on the original image.
masked_image[mask != 0] = [0, 0, 0]

# Display it!
plt.imshow(masked_image)



# Load in a background image, and convert it to RGB 
background_image = mpimg.imread('images/sky.jpg')

## TODO: Crop it or resize the background to be the right size (450x660)
# Hint: Make sure the dimensions are in the correct order!
standardized_im = cv2.resize(background_image,(660, 450))

## TODO: Mask the cropped background so that the car area is blocked
# Hint: mask the opposite area of the previous image
lower_green = np.array([0,180,0]) 
upper_green = np.array([100,255,100])
mask = cv2.inRange(image, lower_green, upper_green)

crop_background = np.copy(standardized_im)
#Turn area that is zero in the mask, aka the car, into [0,0,0] on the sky image.
crop_background[mask == 0] = [0, 0, 0]

## TODO: Display the background and make sure 
plt.imshow(crop_background)


## TODO: Add the two images together to create a complete image!
complete_image = masked_image + crop_background
plt.imshow(complete_image)
