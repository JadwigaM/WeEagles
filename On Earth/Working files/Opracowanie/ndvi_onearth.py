# WeEagles Team
# code to work on NDVI
# based on https://projects.raspberrypi.org/en/projects/astropi-ndvi changed by Antoni Moskal


import cv2
import numpy as np
#The fastie colour map takes dark pixels and makes them white. Then the brighter the original pixels, the further along the spectrum the colours are shifted. So dark grey pixels become blue, while bright white pixels become red.
from fastiecm import fastiecm
from picamera import PiCamera
import picamera.array
nazwa = input('podaj nazwe zdjecia do opracowania ')


plik = '/home/pi/Desktop/' + nazwa + '.jpg'
#original = cv2.imread('/home/pi/Desktop/imageR10.jpg')
original = cv2.imread(plik)




def display(image, image_name):
    image = np.array(image, dtype=float)/float(255)
    shape = image.shape
    height = int(shape[0]/2)
   
    width = int(shape[1]/2)
   
    image = cv2.resize(image, (width, height))
    #cv2.namedWindow(image_name)
    cv2.imshow(image_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def contrast_stretch(im):
    #find the top brightness of pixels in the image in the top 5% and bottom 5% of your image.
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)
    #set the maximum brightness and minimum brightness on the new image you are going to create. The brightest a pixel’s colour can be is 255, and the lowest is 0.
    out_min = 0.0
    out_max = 255.0
    """
some calculations need to be performed to change all the pixels in the image, so that the image has the full range of contrasts from 0 to 255.
Add these lines to stretch out the pixel values and return the contrasted image.
"""
    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

def calc_ndvi(image):
    #To adjust the pixels in the image and only work with red and blue, the image needs splitting into its three seperate channels. r for red, g for green, and b for blue.
    b, g, r = cv2.split(image)
    """
Now the red and blue channels need to be added together and stored as bottom. The blue channel can then have the red channel subtracted (remember that red would mean unhealthy
plants or no plants), and then divided by the bottom calculation. Because we’re doing a division, we also need to make sure that none of our divisors are 0, or there will be an error.
"""
# HQ Camera + RED filter   
    bottom = (r.astype(float) + b.astype(float))
    bottom[bottom==0] = 0.01
    ndvi = (b.astype(float) - r) / bottom


# NoIR+blue filter 
    #bottom = (r.astype(float) + b.astype(float))
    #bottom[bottom==0] = 0.01
    #ndvi = (r.astype(float) - b) / bottom # THIS IS THE CHANGED LINE


    #bottom = (r.astype(float) + g.astype(float))
    #bottom[bottom==0] = 0.01
    #ndvi = (g.astype(float) - r) / bottom
    return ndvi


contrasted = contrast_stretch(original)
cont = nazwa + '_constrasted.png'
cv2.imwrite(cont , contrasted)              
print('NDVI')
#pass in the contrasted image, display it, and save it.
ndvi = calc_ndvi(contrasted)
#display(ndvi, 'NDVI')
cont3 = nazwa + '_ndvi_c.png'
cv2.imwrite(cont3, ndvi)
ndvi_contrasted = contrast_stretch(ndvi)

"""
catch patches of brighter pixels. To once again enhance the image, it can be run through the contrast_stretch function.
Now you can see healthy plant life by the brightness of the pixels in the ndvi_contrasted.png image.
"""
#display(ndvi_contrasted, 'NDVI Contrasted')
print('NDVI Contrasted')
cont2 = nazwa + '_ndvi_constrasted.png'
cv2.imwrite(cont2, ndvi_contrasted)
#cv2.imwrite('ndvi_contrasted.png', ndvi_contrasted)
#Now the image can be converted using cv2 colour mapping, and written out as a new file
color_mapped_prep = ndvi_contrasted.astype(np.uint8)
#convert the image using the fastie colour map, display it, and write a new file.
color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
#display(color_mapped_image, 'Color mapped')
map = nazwa + '_color_mapped.png'
cv2.imwrite(map, color_mapped_image)
#cv2.imwrite('color_mapped_image.png', color_mapped_image)
# write out the original array to a file.
#cv2.imwrite('original.png', original)
print('koniec')
