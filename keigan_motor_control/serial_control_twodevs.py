from time import sleep

from pykeigan import usbcontroller as usbctrl
from pykeigan import utils

dev1_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KWQ4-if00-port0'
dev2_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KUYN-if00-port0'

dev1 = usbctrl.USBController(dev1_path, False)
dev2 = usbctrl.USBController(dev2_path, False)

dev1.enable_action()
dev1.set_curve_type(1)
dev1.set_speed(utils.rpm2rad_per_sec(10))
dev1.preset_position(0)

while True:
    print("Please input 0~3")
    command_input = input()

    if command_input == "0":
        dev1.move_to_pos(utils.deg2rad(0),(utils.deg2rad(720)/4))
        sleep(4)
        dev1.set_led(1, 255, 255, 255)
        dev1.disable_action
        break
    elif command_input == "1":
        dev1.set_led(1, 255, 255, 0)
        dev1.move_to_pos(utils.deg2rad(90), (utils.deg2rad(90)/2))
        sleep(4)
    elif command_input == "2":
        dev1.set_led(1, 0, 255, 255)
        dev1.move_to_pos(utils.deg2rad(180), (utils.deg2rad(90)/2))
        sleep(4)
    elif command_input == "3":
        dev1.set_led(1, 0, 0, 255)
        dev1.move_to_pos(utils.deg2rad(270), (utils.deg2rad(90)/2))
        sleep(4)
    else:
        print("Invalid number. Please re-enter...")
        continue

sleep(2)

dev2.set_led(1, 255, 0, 0)
dev2.enable_action()
dev2.set_speed(utils.rpm2rad_per_sec(20))

dev2.move_by_dist(utils.deg2rad(360), None)
sleep(4)

dev2.set_led(1,255,255,255)
dev2.disable_action()


