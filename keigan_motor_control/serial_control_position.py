import argparse
import sys
import os
import pathlib
from time import sleep

from concurrent.futures import ThreadPoolExecutor

from pykeigan import usbcontroller as usbctrl
from pykeigan import utils

def on_motor_measurement_cb(measurement):
    print("\033[2;2H\033[2K")
    print('measurement {} '.format(measurement))
    sys.stdout.flush()

def on_motor_log_cb(log):
    print("\033[5;2H\033[2K")
    sys.stdout.flush()
    print('log {} '.format(log))
    sys.stdout.flush()

dev_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KWQ4-if00-port0'
# dev2_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KUYN-if00-port0'

dev = usbctrl.USBController(dev_path, False)
dev.on_motor_measurement_value_cb = on_motor_measurement_cb
dev.on_motor_log_cb = on_motor_log_cb

# relative position control

dev.set_led(2,255,255,0)
sleep(3)
dev.enable_action()
dev.set_speed(utils.rpm2rad_per_sec(10))#rpm-> rad/sec

dev.move_by_dist(utils.deg2rad(180),None)#Degree-> rad
sleep(5)
dev.move_by_dist(utils.deg2rad(-180),None)
sleep(5)
dev.move_by_dist(utils.deg2rad(360),utils.rpm2rad_per_sec(15))#rpm-> rad/sec
sleep(6)


# absolute position control

dev.set_curve_type(1)
dev.set_led(2,0,255,255)
dev.set_speed(utils.rpm2rad_per_sec(30))
dev.preset_position(0)#現在位置の座標を0に設定
dev.move_to_pos(utils.deg2rad(90),(utils.deg2rad(90)/3))
sleep(4)
dev.move_to_pos(utils.deg2rad(180),(utils.deg2rad(90)/3))
sleep(4)
dev.move_to_pos(utils.deg2rad(360),(utils.deg2rad(180)/3))
sleep(4)
dev.move_to_pos(utils.deg2rad(720),(utils.deg2rad(360)/3))
sleep(4)
dev.move_to_pos(utils.deg2rad(0),(utils.deg2rad(720)/4))
sleep(5)
dev.set_led(2, 255, 50, 255)
dev.set_curve_type(0)#Turn off Motion control
dev.move_to_pos(utils.deg2rad(90),(utils.deg2rad(90)/0.5))
sleep(2)
dev.move_to_pos(utils.deg2rad(180),(utils.deg2rad(90)/0.5))
sleep(2)
dev.move_to_pos(utils.deg2rad(90),(utils.deg2rad(90)/0.5))
sleep(2)
dev.move_to_pos(utils.deg2rad(360),(utils.deg2rad(270)/1))
sleep(2)

dev.set_led(1,255,255,0)
dev.disable_action()