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



