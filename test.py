import cv2
import numpy as np
import math

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
    blankImage = np.zeros((image1.shape[0], image1.shape[1],3), np.uint8)
    
    xPos, yPos = 0, 0
    while xPos <  image1.shape[1]: #Loop through rows
        while yPos < image1.shape[0]: #Loop through collumns
            valR = int(image1.item(yPos, xPos,2)*ratio + image2.item(yPos, xPos,2)*(1-ratio))
            valG = int(image1.item(yPos, xPos,1)*ratio + image2.item(yPos, xPos,1)*(1-ratio))
            valB = int(image1.item(yPos, xPos,0)*ratio + image2.item(yPos, xPos,0)*(1-ratio))
            blankImage.itemset((yPos, xPos, 0), valB) #Set B to val
            blankImage.itemset((yPos, xPos, 1), valG) #Set G to val
            blankImage.itemset((yPos, xPos, 2), valR) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1
    cv2.imwrite("images/L2_output.jpg", blankImage)
    cv2.imshow("opencv",blankImage)






def increase_brightness(image, percent):
    blankImage = np.zeros((image.shape[0], image.shape[1],3), np.uint8)
    xPos, yPos = 0, 0
    while xPos <  image.shape[1]: #Loop through rows
        while yPos < image.shape[0]: #Loop through collumns
            r = image.item(yPos, xPos,2)
            g = image.item(yPos, xPos,1)
            b = image.item(yPos, xPos,0)
            r = int(256 + r + (256 - r) * percent / 100.0)%256
            g = int(256 + g + (256 - g) * percent / 100.0)%256
            b = int(256 + b + (256 - b) * percent / 100.0)%256
            blankImage.itemset((yPos, xPos, 0), b) #Set B to val
            blankImage.itemset((yPos, xPos, 1), g) #Set G to val
            blankImage.itemset((yPos, xPos, 2), r) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1

    cv2.imshow("opencv",blankImage)


    return;

def solveAffine( m,o):
    oInv = np.linalg.inv(o) 
    a1 = np.transpose(np.dot(oInv, m[:,0]))
    a2 = np.transpose(np.dot(oInv, m[:,1]))
    a3 = np.transpose(np.dot(oInv, m[:,2]))
    a = np.concatenate((a1, a2, a3))
    return a

def applyMatrix(image, matrix):
    blankImage = np.zeros((image.shape[0], image.shape[1],3), np.uint8)
    
    xPos, yPos = 0, 0
    while xPos <  image.shape[1]: #Loop through rows
        while yPos < image.shape[0]: #Loop through collumns
            pos = np.matrix([[xPos], [yPos], [1]])
            newPos = np.dot(matrix,pos)
            # # print([xPos, yPos],newPos)
            # # print(math.ceil(newPos[0,0]),math.floor(newPos[0,0]), math.ceil(newPos[1,0]),math.floor(newPos[1,0]))
            posX = max(0, min(math.floor(newPos[0,0]) , image.shape[1]-1))#696.11 1006 
            posY = max(0, min(math.floor(newPos[1,0]) , image.shape[0]-1)) #695
            print(posX, posY, xPos,yPos, image.shape[1]-1, newPos[0,0], image.shape[0]-1, newPos[1 ,0])
            print(xPos)
            blankImage.itemset((yPos, xPos, 0), image[posY, posX, 0]) #Set B to val
            blankImage.itemset((yPos, xPos, 1), image[posY, posX, 1]) #Set G to val
            blankImage.itemset((yPos, xPos, 2), image[posY, posX, 2]) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1
    

    cv2.imwrite("images/L4_output.jpg", blankImage)
    cv2.imshow("opencv",blankImage)

    return 1
# m = np.matrix('0, 0, 1; 1007 0 1; 1007 696 1; 0 696 1; 0 348 1')
# o = np.matrix('0, 0, 1; 995 135 1; 922 684, 1;64 466 1;30 240 1 ')

m = np.matrix('0, 0, 1; 1007 0 1; 1007 696 1;')
o = np.matrix('0, 0, 1; 995 135 1; 922 684, 1;')

# pts1 = np.float32([[50,50],[200,50],[50,200]])
# pts2 = np.float32([[10,100],[200,50],[100,250]])
# m = cv2.getAffineTransform(pts1,pts2)

matrix = solveAffine(o, m)
image = cv2.imread("images/L3.jpg")
applyMatrix(image, matrix   )
cv2.waitKey(0)

##### Question 1 ######
# threashold("images/L1.jpg", "images/L1_output.jpg", 2**20)
# cv2.imshow("opencv",cv2.imread("images/L1_output.jpg"))
# print("asd")

#### Question 2 ######
# img1 = cv2.imread("images/L1.jpg")
# img2 = resize("images/logo.jpg", img1.shape[1], img1.shape[0])
# blend(img1, img2, .2)

##### Question 3 ######
# increase_brightness(cv2.imread("images/L1.jpg"), 50)