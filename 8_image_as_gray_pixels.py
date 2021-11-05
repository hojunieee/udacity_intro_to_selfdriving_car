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
