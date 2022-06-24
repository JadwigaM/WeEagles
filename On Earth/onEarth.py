# Team WeEagles 
# Program based on:
#https://projects.raspberrypi.org/en/projects/astropi-ndvi
#Changed by Antoni Moskal
import cv2
import numpy as np
from PIL import Image
#The fastie colour map takes dark pixels and makes them white. Then the brighter the original pixels, the further along the spectrum the colours are shifted. So dark grey pixels become blue, while bright white pixels become red.
from fastiecm import fastiecm
from picamera import PiCamera
import picamera.array
from pathlib import Path
import csv

# paths definition
base_folder = Path(__file__).parent.resolve()
nazwa = input('Enter picture name ')

#print(nazwa)
#these lines to your code, to setup and use the Raspberry Pi camera. Comment out the line that loads the park.png image.
# original = cv2.imread('park.png') #Comment out this line, as no longer used

plik = nazwa + '.jpg'
print(plik)
#original = cv2.imread('/home/pi/Desktop/imageR10.jpg')
original = cv2.imread(plik)
def create_csv_file(data_file):
    """Create a new CSV file and add the header row"""
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Image file", "other percentange:", "water percentage:  ", "Vegetation percentange: ", "clouds%")
     
        writer.writerow(header)

def add_csv_data(data_file, data):
    """Add a row of data to the data_file CSV"""
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)


"""
The next stage is to load an image and display it on the screen.
cv2.imread is used to load an image
np.array(original, dtype=float)/float(255) is used to convert the image to an array with the correct type
cv2.namedWindow is used to create a display window
cv2.imshow is used to show an image in a window
cv2.waitKey stops the window from vanishing, until a key is pressed
cv2.destroyAllWindows() closes the window when the key has been pressed
get the width and height of the image you are using, and then scale the values down. 
shape = original.shape
height = int(shape[0]/2)
width = int(shape[1]/2)
"""

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
    in_min = np.percentile(im, 3)
    in_max = np.percentile(im, 96)
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

def contrast_stretch1(im):
    #find the top brightness of pixels in the image in the top 5% and bottom 5% of your image.
    in_min = np.percentile(im, 1)
    in_max = np.percentile(im, 99)
    #set the maximum brightness and minimum brightness on the new image you are going to create. The brightest a pixel’s colour can be is 255, and the lowest is 0.
    out_min = 00.0
    out_max = 250.0
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

def ndvi_clouds(plik, picname1):
    imag=Image.open(plik) # Analiza NDVI
    
    imag=imag.convert("RGB")
    pixels = imag.load()
    
    meanVis = 0.
        #X,Y=0,0
    NDVI = 0
    NDWI = 0
    pNDWI = 0
    sumR = 0
    sumG = 0
    sumB = 0
    sumNDVI = 0
    sumNDWI = 0
    sumpNDWI = 0
    sumaNDVI = 0
    sumaNDWI = 0
    sumapNDWI = 0
    pveg1 = 0
    pwat1 = 0
    pcloud1 = 0
    pcloud2 = 0
    pclouda = 0
    other = 0
    other1 = 0
    pveg = 0
    pwat = 0
    pcloud = 0
    for x in range(0, 2016):
        for y in range(0, 1988):
            pixelRGB=imag.getpixel((x,y))
            R,G,B=pixelRGB
            sumR = R + sumR
            sumG = G + sumG
            sumB = B + sumB

            if (R+B) != 0:
                NDVI=(B-R)/(R+B)
            else:
                NDVI = 0
            if  NDVI > 0.9:
                pixels[x, y] = (255, 0, 0)
                pveg1 = pveg1 + 1.
            elif NDVI <= 0.9 and NDVI >= 0.85 :
                #pixels[x, y] = (0, 215, 0)
                pixels[x, y] = (220, 0, 0)
                pveg1 = pveg1 + 1.
            elif NDVI < 0.85 and NDVI >= 0.8 :
                #pixels[x, y] = (0, 215, 0)
                pixels[x, y] = (200, 0, 0)
                pveg1 = pveg1 + 1.

            elif NDVI < 0.8 and NDVI >= 0.7 :
                pixels[x, y] = (150, 0, 0)
                pveg1 = pveg1 + 1
            elif NDVI < 0.7 and NDVI >= 0.6 :
                pixels[x, y] = (100, 0, 0)
                pveg1 = pveg1 + 1
            elif NDVI < 0.6 and NDVI >= 0.5 :
                pixels[x, y] = (150, 150, 0)
                pveg1 = pveg1 + 1
            elif NDVI < 0.5 and NDVI >= 0.4 :
                pixels[x, y] = (255, 0, 0)
                pveg1 = pveg1 + 1
            elif NDVI < 0.4 and NDVI >= 0.3 :
                pixels[x, y] = (220, 0, 0)
                pveg1 = pveg1 + 1
            elif NDVI < 0.3 and NDVI >= 0.25 :
                pixels[x, y] = (200, 0, 0)
                pveg1 = pveg1 + 1
            elif NDVI < 0.25 and NDVI >= 0.2 :
                pixels[x, y] = (180, 0, 0)
                pveg1 = pveg1 + 1
            
            elif NDVI < 0.2 and NDVI >= 0.15 :
                pixels[x, y] = (150, 0, 0);
                pveg1 = pveg1 + 1
            elif NDVI < 0.15 and NDVI >= 0.1 :
                pixels[x, y] = (130, 0, 0);
                pveg1 = pveg1 + 1
            elif NDVI < 0.1 and NDVI >= 0.02 :
                pixels[x, y] = (100, 10, 100)
                pveg1 = pveg1 + 1
            elif NDVI < 0.02 and NDVI >= 0.0 :
                pixels[x, y] = (10, 10, 180)
                other = other + 1
            elif NDVI < 0.0 and NDVI >= -0.05 :
                pixels[x, y] = (100, 0, 220)
                other = other + 1
            
            elif NDVI < -0.05 and NDVI >= -0.1 :
                pixels[x, y] = (0, 0, 220)
                other = other + 1
            
            elif NDVI < -0.1 and NDVI >= -0.15 :
                pixels[x, y] = (0, 0, 150)
                other = other + 1
            elif NDVI < -0.15 and NDVI >= -0.2 :
                pixels[x, y] = (0, 0, 100)
                pwat1 = pwat1 + 1
            elif NDVI < -0.2 and NDVI >= -0.3 :
                pixels[x, y] = (10, 10, 10)
                pwat1 = pwat1 + 1
            elif NDVI <= -0.3:
                pixels[x, y] = (0, 0, 0)
                pwat1 = pwat1 + 1
            meanVis = float ((R+G+B)/3.0)
            #print("meanVis", meanVis, "R", R, "G", G, "B", B) 
            if R > 0.97 * meanVis and G > 0.97 * meanVis and B > 0.97 * meanVis: # to be changed

                pixels[x, y] = (255, 255, 255)
                pcloud1 = pcloud1 + 1
    other = (100*other1)/4007808
    pveg = (100*pveg1)/4007808
    pwat = (100*(pwat1))/4007808
    pcloud = (100*(pcloud1))/4007808

    print( "water percentage:  ", pwat, "vegetation percentange: ",pveg, "clouds percentage", pcloud, "other percentange: ",other )

    print(sumR, sumG, sumB)

    base_folder = Path(__file__).parent.resolve()
    data_file = base_folder/"data.csv"
    create_csv_file(data_file)
    data = (
            nazwa,
            other,
            pwat,
            pveg,
                  )
    add_csv_data(data_file, data)
       
    imag=imag.save(picname1)
    print('NDVI-a')



#display(original, 'Original')
# convert your image and display it on the screen.
contrasted = contrast_stretch(original)
#display(contrasted, 'Contrasted original')
#save your high contrast image by adding a single line to the end of your code, so that you can compare the two images in your file browser. It will be called contrasted.png.
#cv2.imwrite('contrasted.png', contrasted)
cont = nazwa + '_contrasted.png'
cv2.imwrite(cont , contrasted)              
print('NDVI')
#pass in the contrasted image, display it, and save it.
#ndvi = calc_ndvi(contrasted)
#tu zmienilem 14.06.2022
ndvi = calc_ndvi(contrasted)
#display(ndvi, 'NDVI')
cont3 = nazwa + '_ndvi_c.png'
#cv2.imwrite(cont3, ndvi)
ndvi_contrasted = contrast_stretch1(ndvi)

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
#
#
color_mapped_prep = ndvi_contrasted.astype(np.uint8)

#convert the image using the fastie colour map, display it, and write a new file.
color_mapped_image = cv2.applyColorMap(color_mapped_prep, fastiecm)
#display(color_mapped_image, 'Color mapped')
map = nazwa + '_color_mapped.png'
cv2.imwrite(map, color_mapped_image)
#cv2.imwrite('color_mapped_image.png', color_mapped_image)
# write out the original array to a file.
#cv2.imwrite('original.png', original)
#
#New NDVI
#plik = '/home/pi/Desktop/' + nazwa + '.jpg'
plik = nazwa + '.jpg'
#picname = pic1 + ".jpg"
picname1 = nazwa + "_ndvi_a.png"
ndvi_clouds(plik, picname1)
#imag=Image.open(plik) # Analiza NDVI
    

print('koniec')
