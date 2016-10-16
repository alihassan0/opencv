import cv2
import numpy as np


def threashold( src, dist, breakPoint):
    img = cv2.imread(src)
    imageWidth = 669 #Get image width
    imageHeight = 325 #Get image height

    xPos, yPos = 0, 0

    while xPos < imageWidth: #Loop through rows
        while yPos < imageHeight: #Loop through collumns
            val1 = img[yPos, xPos,2]*2**16 + img[yPos, xPos,1]*2**8 +img[yPos, xPos,0]
            val = 255 if val1 > breakPoint else 0
            img.itemset((yPos, xPos, 0), val) #Set B to val
            img.itemset((yPos, xPos, 1), val) #Set G to val
            img.itemset((yPos, xPos, 2), val) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1

    cv2.imwrite(dist, img) #Write image to file
    return;

def resize(imagePath, width, height):
    blankImage = np.zeros((height,width,3), np.uint8)
    sourceImage = cv2.imread(imagePath)
    
    xPos, yPos = 0, 0
    while xPos < width: #Loop through rows
        while yPos < height: #Loop through collumns
            valR = sourceImage.item(int((yPos*1.0) / height * sourceImage.shape[0]), \
                                    int((xPos*1.0) / width * sourceImage.shape[1]),2)
            valG = sourceImage.item(int((yPos*1.0) / height * sourceImage.shape[0]), \
                                    int((xPos*1.0) / width * sourceImage.shape[1]),1)
            valB = sourceImage.item(int((yPos*1.0) / height * sourceImage.shape[0]), \
                                    int((xPos*1.0) / width * sourceImage.shape[1]),0)
            blankImage.itemset((yPos, xPos, 0), valB) #Set B to val
            blankImage.itemset((yPos, xPos, 1), valG) #Set G to val
            blankImage.itemset((yPos, xPos, 2), valR) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1

    cv2.imshow("opencv",blankImage)
    return blankImage;

def blend(image1, image2, ratio):
    blankImage = np.zeros((img1.shape[0], img1.shape[1],3), np.uint8)
    
    xPos, yPos = 0, 0
    while xPos <  img1.shape[1]: #Loop through rows
        while yPos < img1.shape[0]: #Loop through collumns
            valR = int(image1.item(yPos, xPos,2)*ratio + image2.item(yPos, xPos,2)*(1-ratio))
            valG = int(image1.item(yPos, xPos,1)*ratio + image2.item(yPos, xPos,1)*(1-ratio))
            valB = int(image1.item(yPos, xPos,0)*ratio + image2.item(yPos, xPos,0)*(1-ratio))
            blankImage.itemset((yPos, xPos, 0), valB) #Set B to val
            blankImage.itemset((yPos, xPos, 1), valG) #Set G to val
            blankImage.itemset((yPos, xPos, 2), valR) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1

    cv2.imshow("opencv",blankImage)





##### Question 1 ######
# threashold("images/L1.jpg", "images/L1_output.jpg", 2**20)
# cv2.imshow("opencv",cv2.imread("images/L1_output.jpg"))


##### Question 2 ######
img1 = cv2.imread("images/L1.jpg")
img2 = resize("images/logo.jpg", img1.shape[1], img1.shape[0])
blend(img1, img2, .2)

cv2.waitKey(0)
