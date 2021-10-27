import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
import time
import numpy


odrv0_serial = "20793595524B"  # Previously Xavier
odrv1_serial = "20673593524B"  # Previously Yannie


odrv0 = odrive.find_any(serial_number=odrv0_serial)
odrv1 = odrive.find_any(serial_number=odrv1_serial)

axis = odrv1.axis1

def move(dist = 5):
    axis.controller.input_pos = 0
    time.sleep(2)

    axis.controller.input_pos = dist

def move2(t = 1):
    startpos = axis.encoder.pos_estimate

    axis.controller.input_vel = 3
    time.sleep(t)
    axis.controller.input_vel = -3
    time.sleep(t)
    axis.controller.input_pos = startpos


start_liveplotter(lambda:[axis.encoder.pos_estimate, axis.controller.input_pos])


axis.requested_state =  AXIS_STATE_FULL_CALIBRATION_SEQUENCE

while axis.current_state != AXIS_STATE_IDLE:
    pass
time.sleep(1)

axis.controller.config.vel_limit = 20
axis.controller.config.enable_overspeed_error = False

axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
axis.controller.config.input_mode = INPUT_MODE_PASSTHROUGH

axis.controller.input_pos = 1

time.sleep(1)


print(axis.controller.input_pos)
print(axis.controller.pos_setpoint)
print(axis.encoder.pos_estimate)





while True:
    print(f"""
    vel_gain (v) = {axis.controller.config.vel_gain}
    pos_gain (p) = {axis.controller.config.pos_gain}
    vel_integrator_gain (i) = {axis.controller.config.vel_integrator_gain}""")

    text = input()

    try:

        if text == "d":
            axis.controller.config.vel_gain = .16
            axis.controller.config.pos_gain = 20
            axis.controller.config.vel_integrator_gain = .32


        elif text[0:2] == 'm2':

            val = float(text.split(" ")[1])
            print(f"moving vel {val}")
            move2(float(val))

        elif text[0] == 'm':

            val = float(text.split(" ")[1])
            print(f"moving {val}")
            move(float(val))


            
        else:
            target, val = text.split(" ")
            val = float(val)

            if target == "v":
                axis.controller.config.vel_gain = val
            elif target == "p":
                axis.controller.config.pos_gain = val
            elif target == "i":
                axis.controller.config.vel_integrator_gain = val
            

        
    except Exception as e:
        print(f"ERROR: {e}")

    

# odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
# odrv0.axis0.motor.config.pre_calibrated = True
# odrv0.axis0.config.startup_encoder_offset_calibration = True
# odrv0.axis0.config.startup_closed_loop_control = True
# odrv0.save_configuration()
# odrv0.reboot()





# start_liveplotter(lambda:[odrv0.axis0.encoder.pos_estimate, odrv0.axis0.controller.pos_setpoint])

print("done!")



