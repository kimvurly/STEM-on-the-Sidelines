#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain = Brain()

# Robot configuration code
brain_inertial = Inertial()
controller = Controller()
motor_1 = Motor(Ports.PORT1, False)
motor_2 = Motor(Ports.PORT2, True)
left_motor_a = Motor(Ports.PORT3, False)
left_motor_b = Motor(Ports.PORT4, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT5, True)
right_motor_b = Motor(Ports.PORT6, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 259.34, 320, 40, MM, 1)


# Wait for sensor(s) to fully initialize
wait(100, MSEC)

def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)



# define variables used for controlling motors based on controller inputs
controller_left_shoulder_control_motors_stopped = True
controller_right_shoulder_control_motors_stopped = True
drivetrain_l_needs_to_be_stopped_controller = False
drivetrain_r_needs_to_be_stopped_controller = False

# define a task that will handle monitoring inputs from controller
def rc_auto_loop_function_controller():
    global drivetrain_l_needs_to_be_stopped_controller, drivetrain_r_needs_to_be_stopped_controller, controller_left_shoulder_control_motors_stopped, controller_right_shoulder_control_motors_stopped, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3 + axis1
            # right = axis3 - axis1
            drivetrain_left_side_speed = controller.axis3.position() + controller.axis1.position()
            drivetrain_right_side_speed = controller.axis3.position() - controller.axis1.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
            # check the buttonL1/buttonL2 status
            # to control motor_1
            if controller.buttonL1.pressing():
                motor_1.spin(FORWARD)
                controller_left_shoulder_control_motors_stopped = False
            elif controller.buttonL2.pressing():
                motor_1.spin(REVERSE)
                controller_left_shoulder_control_motors_stopped = False
            elif not controller_left_shoulder_control_motors_stopped:
                motor_1.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_left_shoulder_control_motors_stopped = True
            # check the buttonR1/buttonR2 status
            # to control motor_2
            if controller.buttonR1.pressing():
                motor_2.spin(FORWARD)
                controller_right_shoulder_control_motors_stopped = False
            elif controller.buttonR2.pressing():
                motor_2.spin(REVERSE)
                controller_right_shoulder_control_motors_stopped = False
            elif not controller_right_shoulder_control_motors_stopped:
                motor_2.stop()
                # set the toggle so that we don't constantly tell the motor to stop when
                # the buttons are released
                controller_right_shoulder_control_motors_stopped = True
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller = Thread(rc_auto_loop_function_controller)

#endregion VEXcode Generated Robot Configuration
myVariable = 0


def when_started1():
   global myVariable
   while True:
       if controller.buttonL1.pressing():
           drivetrain.drive(FORWARD)
       else:
           pass
       wait(5, MSEC)


# Calibrate the Drivetrain
calibrate_drivetrain()


when_started1()



