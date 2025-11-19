#import required libraries
import time
from machine import Pin, PWM

#set the output location of the PWM signal 
shoulder    = PWM(Pin(0))
elbow       = PWM(Pin(1))
wrist       = PWM(Pin(2))

#set the frequency of the PWM signal
shoulder.freq(50)
elbow.freq(50)
wrist.freq(50)

#function to translate the degree value to a value that can be read by the servo (from previous lab)
def translate(angle: float) -> int:
    
    if angle > 179:
        angle = 179
    elif angle < 0:
        angle = 0

    #get the puse width
    pulse_width = 500 + (2500 - 500) * angle / 180
    #get the duty cycle as a number between 0-1
    duty_cycle = pulse_width / 20000
    #make that number a numebr between 65535
    global return_value
    return_value = int(duty_cycle * 65535)

    #set the return value to the result
    return return_value 

#function to read and parse the G code file
def read():
    #read the file
    with open("line.gcode", "r") as f:
        #this for loops goes thorugh the file and cleans every line
        for line in f:
            #this removes any unescessary spaces
            line.strip()
            #this turns every element divided by a space into a element in a list
            #this will make them easy to acess later
            command = line.split(" ")
            #this calls the following function which will interperate the information contained in the file
            interpret(command)

            #a time buffer so that the servo does not get overwhelmed and only reads the file (and moves) one line at a time
            time.sleep(2)

#function to interpret commands
def interpret(command):
    #define the command type as the first item in the list for each line
    command_type = command[0].strip()

    #check the command type at the begining of each line
    if (command_type == "G1"):
        #if the command function is G1, then move the shoulder and elbow servo

        #print function to comnicate that is reading the porper kind of movement
        print("G1: MOVE")

        #angles are set and the difference between the shoulder and elbow servos are defined
        #the shoulder is the first angle value and therefore the second value in the list
        angle_shoulder =    (command[1]) [1:]
        #the elbow is the second angle value and therefore the third value in the list
        angle_elbow =       (command[2]) [1:]

        #translated it to a PWM value between 0 and 65535 so that the servo can read it 
        pwm_shoulder = translate(float(angle_shoulder))
        pwm_elbow = translate(float(angle_elbow))

        #then send the pwm to the servos to move them to the location specified in the file
        shoulder.duty_u16(pwm_shoulder)
        elbow.duty_u16(pwm_elbow)

        #for testing, print the difference between the angle the servo thinks its at and the encoder values
        #this will allow me to determine the accuracy of the servo

        #this accuracy can have a set acceptable error value maximum
        #LEDs and the terminal can be used to communicate weather the error value surpasses the maximum acceptable value

    elif (command_type == "M5"):
        #if the command type is M5, then the wrist servo should lift the pencil up

        #print function to comnicate that is reading the porper kind of movement
        print("M5: UP")
        #set the up angle to a value that can raise the pencil but still be safe for the servo
        up_angle = 30
        #translated it to a PWM value between 0 and 65535 so that the servo can read it 
        pwm_wrist = translate(up_angle)
        #sends the translated value to the servo
        wrist.duty_u16(pwm_wrist)

    elif (command_type == "M3"):
        #if the command type is M3, then the wrist servo should put the pencil down on the page

        #print function to comnicate that is reading the porper kind of movement
        print("M3: DOWN")

        #sets the angle the servo should be at to place the pencil down on the paper (in degrees)
        down_angle = 0
        #translated it to a PWM value between 0 and 65535 so that the servo can read it 
        pwm_wrist = translate(down_angle)
        #sends the translated value to the servo
        wrist.duty_u16(pwm_wrist)
    elif (command_type == "M18"):
        #if the command type is M18, then the servo should stop and return to a default posistion
        print("M18: STOP")

        #set the up angle to a value that can raise the pencil but still be safe for the servo
        up_angle = 30

        #translated the default angle values to PWM values between 0 and 65535 so that the servo can read it 
        pwm_shoulder = translate(0)
        pwm_elbow = translate(0)
        pwm_wrist = translate(up_angle)

        #then send the pwm to the servos to move them to the default location
        wrist.duty_u16(pwm_wrist)
        shoulder.duty_u16(pwm_shoulder)
        elbow.duty_u16(pwm_elbow)
    else:
        #if there is a command type that this program cant read, the error will be communicated ot the user
        print("the command type that is being read from the file is not one that this program can read")
        print("the command type that has caused issues is: ", command_type)

#call the read function to read and execute the commands in the file
read()
