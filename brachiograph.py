from machine import Pin,PWM,ADC
from time import sleep as wait

# Hardware constants
S1=PWM(Pin(0)) # Shoulder
S2=PWM(Pin(1)) # Elbow
S3=PWM(Pin(2)) # Wrist
B1=None # Up/down toggle
B2=None # Shutdown

def translate(angle:float) -> int:
    '''Translate an angle to the duty factor required to assume it.'''
    MIN=1638
    MAX=8192
    deg=(MAX-MIN)/180
    angle=max(0,min(180,angle))
    return int(angle*deg+MIN)

def move(servo:PWM,deg:int) -> None:
    '''Move a servo (arg1) by arg2 degrees.'''
    servo.duty_u16(translate(deg))
    return

def gettarget() -> list:
    '''Turn the potentiometers' positions into useable xy coordinartes by filtering out noise.'''
    raw=[ADC(Pin(27)),ADC(Pin(26))] # [left,right]
    # TODO: Filter out noise: min is 384, max is 65535
    return

def calc(target:list) -> list:
    '''Calculate the servo angles required the reach the target (arg1).'''
    # Inverse kinematics to be done here
    return [0,1]

def toggle_wrist() -> None:
    '''Toggle the wrist.'''
    # TODO: - Query the wrist servo
    #       - If up (30deg), move down (0deg), and vice versa
    return

target=None # Init so the if doesn't throw an error before calc() is used
while True:
    if not target==gettarget(): # Act only if there's been a change since last reading
        target=gettarget() # Potentiometer positions list is taken to form the coordinates of the target
        reqangles=calc(target)
        move(S1,reqangles[0]) # Move the first servo to its target
        move(S2,reqangles[1])
