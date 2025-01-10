from time import sleep

from pykeigan import usbcontroller as usbctrl
from pykeigan import utils

dev1_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KUYN-if00-port0'
dev2_path = '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_DM00KWQ4-if00-port0'

def serial_control_motors(index, position_speed = 90, rotate_speed = 20):

    #------------ initialization ------------#

    # USBController instance initialization
    dev1 = usbctrl.USBController(dev1_path, False)
    dev2 = usbctrl.USBController(dev2_path, False)

    # Enable motor for position control
    dev1.enable_action()
    # Set how to acceleration
    dev1.set_curve_type(1)
    # Set speed of motor for position control
    dev1.set_speed(utils.rpm2rad_per_sec(rotate_speed))
    # Set initial position
    dev1.preset_position(0)


    #----------- position control -----------#

    # position control
    if index == 0:
        dev1.move_to_pos(utils.deg2rad(90), (utils.deg2rad(position_speed)))
        sleep(4)
    
    elif index == 1:
        dev1.move_to_pos(utils.deg2rad(180), (utils.deg2rad(position_speed)))
        sleep(4)
    
    else:
        print("unabailable number.")

    # Move to initial position
    dev1.move_to_pos(utils.deg2rad(0),(position_speed))
    sleep(4)
    # Disable motor for position control
    dev1.disable_action

    sleep(2)


    #------- One rotation of divider -------#

    # Enable motor for divider control
    dev2.enable_action()
    # Set speed of motor for divider control
    dev2.set_speed(utils.rpm2rad_per_sec(rotate_speed))

    # One rotation of divider
    dev2.move_by_dist(utils.deg2rad(360), None)
    sleep(4)

    # Disable motor for divider control
    dev2.disable_action()

if __name__ == "__main__":
    # categories = ["can", "pet"]
    category_index = 0
    position_speed = 90 # [deg/sec]
    rotate_speed = 20 # [rpm]

    serial_control_motors(category_index, position_speed, rotate_speed)