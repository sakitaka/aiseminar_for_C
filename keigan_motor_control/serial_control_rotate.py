import argparse
import sys
import pathlib
from time import sleep

from pykeigan import usbcontroller as usbctrl
from pykeigan import utils

dev_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KWQ4-if00-port0'

dev = usbctrl.USBController(dev_path, False)

dev.enable_action()
dev.set_speed(utils.rpm2rad_per_sec(5))

dev.set_led(1, 0, 200, 0)
dev.run_forward()

sleep(10)

dev.set_led(1, 200, 0, 0)
dev.run_reverse()

sleep(10)

dev.set_led(1, 200, 0, 0)
dev.stop_motor()

dev.set_led(1, 100, 100, 100)
dev.free_motor()