import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import cv2
from utils import preprocess
import time
import sys


from time import sleep
from pykeigan import usbcontroller as usbctrl
from pykeigan import utils
dev2_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KUYN-if00-port0'
dev1_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KWQ4-if00-port0'

##motor setteing###
#------------ initialization ------------#

# default speed
rotate_speed = 60
position_speed = 60

# USBController instance initialization
dev1 = usbctrl.USBController(dev1_path, False)
dev2 = usbctrl.USBController(dev2_path, False)

# Enable motor for position control
dev1.enable_action()
dev2.enable_action()

# Set how to acceleration
dev1.set_curve_type(1)
dev2.set_curve_type(1)
# Set speed of motor for position control
dev1.set_speed(utils.rpm2rad_per_sec(rotate_speed))
dev2.set_speed(utils.rpm2rad_per_sec(rotate_speed))
# Set initial position
dev1.preset_position(0)
dev2.preset_position(0)

dev1.move_to_pos(utils.deg2rad(0),(position_speed))
dev2.move_to_pos(utils.deg2rad(0),(position_speed))

    #----------- position control -----------#




sys.path.append("opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO")

dev2_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KUYN-if00-port0'
dev1_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KWQ4-if00-port0'



#camera = cv2.VideoCapture(0)
def take_picture():
    camera = cv2.VideoCapture(0)
    re, img = camera.read()
    img = cv2.resize(img, dsize=(224,224))
    camera.release()
    return img



model = torch.load("model_weight.pth")
print("first load")
img = take_picture()
preprocessed = preprocess(img)
output = model(preprocessed)
output = torch.nn.functional.softmax(output,dim =1).detach().cpu().numpy().flatten()
category_index = output.argmax()
print("end loading")

num_loop =0
while True:
    num_loop +=1
    s = input("press enter to classify. if you cansel, please type 'q':")
    if s == 'q':break
    img = take_picture()
    preprocessed = preprocess(img)
    output = model(preprocessed)
    output = torch.nn.functional.softmax(output,dim =1).detach().cpu().numpy().flatten()
    category_index = output.argmax()
    print(output)
    
    # position control
    if category_index == 0:
        dev1.move_to_pos(utils.deg2rad(90), (utils.deg2rad(position_speed)))
        sleep(4)
    
    elif category_index == 1:
        dev1.move_to_pos(utils.deg2rad(180), (utils.deg2rad(position_speed)))
        sleep(4)
    
    else:
        print("unabailable number.")



    #------- One rotation of divider -------#

    
    # Set speed of motor for divider control
    #dev2.set_speed(utils.rpm2rad_per_sec(rotate_speed))

    # One rotation of divider
    #dev2.move_by_dist(utils.deg2rad(360), None)
    
    dev2.move_to_pos(utils.deg2rad(360),utils.deg2rad(rotate_speed))
    sleep(8)
    dev2.preset_position(0)

    # Move to initial position
    dev1.move_to_pos(utils.deg2rad(0),utils.deg2rad(position_speed))
    sleep(4)

    sleep(2)

dev1.disable_action()
dev2.disable_action()


    

# camera.release()

