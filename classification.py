import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import cv2
from utils import preprocess
import time
import sys
sys.path.append("opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO")
import Jetson.GPIO as GPIO



led_can = 16
led_pet = 23

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_can, GPIO.OUT, initial =GPIO.LOW)
GPIO.setup(led_pet, GPIO.OUT, initial =GPIO.LOW)

#camera = cv2.VideoCapture(0)
def take_picture():
    camera = cv2.VideoCapture(0)
    re, img = camera.read()
    img = cv2.resize(img, dsize=(224,224))
    camera.release()
    return img



model = torch.load("model_weight.pth")
while True:
    s = input("press enter to classify. if you cansel, please type 'q':")
    if s == 'q':break
    img = take_picture()
    preprocessed = preprocess(img)
    output = model(preprocessed)
    output = torch.nn.functional.softmax(output,dim =1).detach().cpu().numpy().flatten()
    category_index = output.argmax()
    print(output)
    if category_index ==0:
        led = led_can
    else:
        led = led_pet
    GPIO.output(led, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(led, GPIO.LOW)

# camera.release()
GPIO.cleanup()

