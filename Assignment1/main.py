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

def resize(src, width, height):
    blankImage = np.zeros((height,width,3), np.uint8)
    sourceImage = cv2.imread(src)
    
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
        while yPos < image1.shape[0]: #Loop through columns
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






def increase_brightness(src, percent):
    image = cv2.imread(src)
    blankImage = np.zeros((image.shape[0], image.shape[1],3), np.uint8)
    xPos, yPos = 0, 0
    percent = 1+percent/100.0
    while xPos <  image.shape[1]: #Loop through rows
        while yPos < image.shape[0]: #Loop through collumns
            r = max(0, min(image.item(yPos, xPos,2) * percent , 255))
            g = max(0, min(image.item(yPos, xPos,1) * percent , 255))
            b = max(0, min(image.item(yPos, xPos,0) * percent , 255))
            blankImage.itemset((yPos, xPos, 0), b) #Set B to val
            blankImage.itemset((yPos, xPos, 1), g) #Set G to val
            blankImage.itemset((yPos, xPos, 2), r) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1

    cv2.imshow("opencv",blankImage)

    return blankImage;

def solveAffine( m,o):
    oInv = np.linalg.inv(o) 
    a1 = np.transpose(np.dot(oInv, m[:,0]))
    a2 = np.transpose(np.dot(oInv, m[:,1]))
    a3 = np.transpose(np.dot(oInv, m[:,2]))
    a = np.concatenate((a1, a2, a3))
    return a

def applyMatrix(src, matrix):
    image = cv2.imread(src)
    
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
            # print(posX, posY, xPos,yPos, image.shape[1]-1, newPos[0,0], image.shape[0]-1, newPos[1 ,0])

            
            blankImage.itemset((yPos, xPos, 0), image[int(posY), int(posX), 0]) #Set B to val
            blankImage.itemset((yPos, xPos, 1), image[int(posY), int(posX), 1]) #Set G to val
            blankImage.itemset((yPos, xPos, 2), image[int(posY), int(posX), 2]) #Set R to val

            yPos = yPos + 1 #Increment Y position by 1

        yPos = 0
        xPos = xPos + 1 #Increment X position by 1
    

    cv2.imwrite("images/L4_output.jpg", blankImage)
    cv2.imshow("opencv",blankImage)

    return blankImage




# ##### Question 1 ######
# threashold("images/L1.jpg", "images/L1_output.jpg", 2**22)
# cv2.imshow("opencv",cv2.imread("images/L1_output.jpg"))

#### Question 2 ######
# img1 = cv2.imread("images/L2.jpg")
# img2 = resize("images/logo.jpg", img1.shape[1], img1.shape[0])
# blend(img1, img2, .8)

##### Question 3 ######
# cv2.imwrite("images/L2_output_3.jpg", increase_brightness("images/L2.jpg", 50))

### Question 4 ######

# m = np.matrix('0, 0, 1; 1007 0 1; 1007 696 1')
# o = np.matrix('0, 0, 1; 995 135 1; 922 684, 1')

# matrix = solveAffine(o, m)
# image1 = applyMatrix("images/L3.jpg", matrix)


# m = np.matrix('0, 0, 1; 0 696 1; 1007 696 1')
# o = np.matrix('0, 0, 1; 125 577 1; 1007 696, 1')

# matrix = solveAffine(o, m)
# image2 = applyMatrix("images/L4_output.jpg", matrix)


# blankImage = np.zeros((image1.shape[0], image1.shape[1],3), np.uint8)    
# xPos, yPos = 0, 0
# while xPos <  image1.shape[1]: #Loop through rows
#     while yPos < image1.shape[0]: #Loop through collumns
#         if yPos < xPos* (image1.shape[0]*1.0/image1.shape[1]) :
#             image = image1
#         else :
#             image = image2 
#         r = image.item(yPos, xPos,2)
#         g = image.item(yPos, xPos,1)
#         b = image.item(yPos, xPos,0)
#         blankImage.itemset((yPos, xPos, 0), b) #Set B to val
#         blankImage.itemset((yPos, xPos, 1), g) #Set G to val
#         blankImage.itemset((yPos, xPos, 2), r) #Set R to val

#         yPos = yPos + 1 #Increment Y position by 1

#     yPos = 0
#     xPos = xPos + 1 #Increment X position by 1
# cv2.imshow("opencv",blankImage)
# cv2.imwrite("images/L4_final.jpg", blankImage)

### Question 5 ######

# src = np.float32([[54,54],[189,22],[186,147],[55,184]])
# dst = np.float32([[0,0],[138,0],[138,128],[0, 128]])

# image = cv2.imread("images/L4.jpg")

# res,status = cv2.findHomography(src, dst)
# im_out = cv2.warpPerspective(image, res, (138,128))
# cv2.imshow("opencv",im_out)
# cv2.imwrite("images/L5_output.jpg", im_out)
    
cv2.waitKey(0)
