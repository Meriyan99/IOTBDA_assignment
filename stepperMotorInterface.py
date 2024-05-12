# -------------- Stepper motor control with raspberry pi ----------------------------------
# -------------- IT19175058 -----------------------
# -------------- Mariyam M.S.S --------------------

# ---------------------------- IMPORTS --------------------------------------------------------
# import library for the operation of sensor
import Adafruit_DHT

# import time
import time

# import RPi.GPIO module
import RPi.GPIO as GPIO

# import file to read temperature
from SenseTemp import observeTemp



# Specify mode
GPIO.setmode(GPIO.BCM)

# Avoid printing warnings
GPIO.setwarnings(False)



# --------------------------- VARIABLE INITIALIZATION ------------------------------------------------------------------

sensor = Adafruit_DHT.DHT11   # Type of sensor used
temp_pin = 4                  # Physical pin number where the sensor is connected to 
ControlPin = [7,11,13,15]     # Physical pin numbers where the 'IN' pins of stepper motor are connected to


initial_temp = 0.0      # Set initial temp values as 0
num_of_round = 1        # Variable to identify the loop number
initial_effect = 'No effect'    # Set initial feel of climate as 'No effect'
initial_rotate = 0.0    # Set initial revolution value to 0



# --------------------------------------- FUNCTION TO GET THE REVOLUTION BASED ON TEMPERATURE ---------------------------------------
def get_angle(cur_temp):
    if cur_temp < 20:
        revolutions = float(1/12)   # if temp is less than 20, rotate 30 degrees
        effect = 'Cold'         # if temp is less than 20, climate feel is cold
    elif cur_temp >= 20 and cur_temp < 30:  
        revolutions = float(1/4)    # if temp is between 20 - 30, rotate 90 degrees
        effect = 'Warm'         # if temp is between 20 - 30, climate feel is warm
    else:
        revolutions = float(1/3)   # if temp is greater than 30, rotate 120 degrees
        effect = 'Hot'         # if temp is greater than 30, climate feel is hot
       
    return revolutions,effect



# --------------------------------------- FUNCTION TO GET THE DIRECTION OF ROTATION ---------------------------------------
def get_dir(prev_temp, cur_temp):
    if prev_temp < cur_temp: # For increase in temperature range direction is clockwise
        direction = 1
    else:
        direction = -1       # For decrease in temperature range direction is anti-clockwise
    
    return direction



# --------------------------------------- FUNCTION TO GET THE ROTATE THE ACTUATOR ---------------------------------------
def func_actuate(revolutions,rotate_dir):
    
    for pin in ControlPin:
        # Setting output pin
        GPIO.setup(pin,GPIO.OUT)
        GPIO.output(pin,False)

    # set sequence number for steps
    step_seq_num = 0
    
    # speed of the indicator
    rotation_speed = 0.001

    
    # rotation angle        
    rotate = int(revolutions * 4096)    # 360 = 4096 steps

    # resolutions
    seq = [ [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1],
    ]

    # default direction and speed of rotation if the direction not specified properly
    if rotate_dir != 1 and rotate_dir != -1:
        rotate_dir = 1
        rotation_speed = float(rotation_speed)

    # movement of indicator
    for i in  range(0,(rotate+1)):
        for pin in range(0,4):
            pattern_pin = ControlPin[pin]
            if seq[step_seq_num][pin] == 1:
                GPIO.output(pattern_pin, True)
            else:
                GPIO.output(pattern_pin,False)

        step_seq_num += rotate_dir
        if(step_seq_num >= 8):
            step_seq_num = 0
        elif step_seq_num < 0:
            step_seq_num = 7

        time.sleep(rotation_speed)
        



# --------------------------------------- MAIN STARTING POINT OF IMPLEMETATION ---------------------------------------
while True:
    # humidity, temperature = Adafruit_DHT.read_retry(sensor, temp_pin)  # Get the reading from the sensors
    humidity, temperature = observeTemp(sensor, temp_pin)
    
    # If no readings observed print an error message
    if humidity is None and temperature is None:
        print("Failed to get a reading! Please check the configurations")
    # If readings observed
    else:
        # print the number of loop
        print('=============== '+str(num_of_round)+' ==================')
        # increment the loop number by 1
        num_of_round = num_of_round + 1

        # Print sensed temperature
        print("Sensed Temperature = {0:0.1f}*C".format(temperature))
        # Print previous temperature
        print("Previous Temperature = {0:0.1f}*C".format(initial_temp))

        # If temperature does not change do nothing
        if initial_temp == temperature:
            print('No change in temperature')
            print('No change in actuator movement')
        # If temperature change
        else:
            # Get the revolution and climate feel
            angle, climate = get_angle(temperature)

            # Get the direction
            direction = get_dir(initial_temp,temperature)

            print('Change in temperature')
            print('Climate Feel is ', climate)
            
            # Check if the change is within the same range
            if initial_rotate != angle:
                func_actuate(angle,direction) # If not in the same range call function to rotate the stepper motor
                print('Change in actuator movement')  
        
        initial_temp = temperature # Change the previous temperature value to last sensed temperature value
        initial_rotate = angle     # Change the previous revolution value to last revolution value
        
    time.sleep(3)
        