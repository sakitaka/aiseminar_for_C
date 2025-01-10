import cv2


def take_picture(no,dire):
    camera =cv2.VideoCapture(0)
    re, img =camera.read()
    if re:
        img =cv2.resize(img, dsize =(224,224))
        cv2.imwrite(dire+"img_"+str(no)+".jpg",img)
        cv2.imshow("camera",img)
    else:
        print("no camera device")
    return img


for i in range(0,20):
    #dire = "./data/train/pet/" 
    dire = "./data/val/pet/"
    #dire = "./data/train/can/"
    #dire = "./data/val/can/"
    s = input("{}:press_enter".format(i))
    take_picture(i, dire)
