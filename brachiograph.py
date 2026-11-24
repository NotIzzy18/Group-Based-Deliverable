from machine import Pin,PWM,ADC
import math

# Hardware constants
S1=PWM(Pin(0)) # Shoulder
S2=PWM(Pin(1)) # Elbow
S3=PWM(Pin(2)) # Wrist
S3.freq(50)    # Servos need 50 Hz
B1=Pin(22,Pin.IN,Pin.PULL_UP) # Up/down toggle (GP22, same as already pushed)
B2=Pin(13) # Reset to 0,0
B3=Pin(12) # Shutdown
WRIST_UP=30   # degrees (confirmed by testing on our jig)
WRIST_DOWN=0  # degrees

wrist_flag=False # Set by the button, handled in the main loop
last_press=0     # For debounce


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
    return raw

def calc(target:list) -> list:
    '''Calculate the servo angles required the reach the target (arg1).'''
    # Inverse kinematics to be done here
    La = 155 # length from shoulder to elblow = 155 mm
    Lb = 155 # length from elbow to wrist = 155 mm
    
    end_position_x = float(target[0])
    end_position_y = float(target[1])
    
    print(end_position_x)
    print(end_position_y)
    
    shoulder_position = [-50.0, 139.5] # coordinates of shoulder position if origin is bottom left corner of page
    
    end_position = math.sqrt(((shoulder_position[0] - end_position_x)**2.0) + (shoulder_position[1] - end_position_y)**2.0)
    xaxis_end_position = math.sqrt(((shoulder_position[0] - end_position_x)**2.0) + (end_position_y)**2.0)
    
    angle_bac = math.acos(((La)**2 + (end_position)**2 - (Lb)**2)/(2*La*end_position)) # b = elbow; a = shoulder; c = wrist
    angle_acb = math.asin(((La)*(math.sin(angle_bac)))/(Lb)) # b = elbow; a = shoulder; c = wrist
    angle_yac = math.acos(((shoulder_position[1])**2 + (end_position)**2 - (xaxis_end_position)**2)/(2*(shoulder_position[1])*(end_position))) # y = y-axis (vertical); a = shoulder; c = wrist
    
    alpha = math.degrees(angle_bac) + math.degrees(angle_yac) # alpha = servo position of shoulder
    beta = math.degrees(angle_bac) + math.degrees(angle_acb) # beta = servo position of elbow
    
    return [alpha,beta] # The required angles

def toggle_wrist() -> None:
    '''Toggle the wrist.'''
    duty=S3.duty_u16()
    if abs(duty-translate(WRIST_UP))<abs(duty-translate(WRIST_DOWN)):
        move(S3,WRIST_DOWN) # If up, move down
    else:
        move(S3,WRIST_UP)   # If down, move up
    return

# Button handler (below toggle_wrist)
def b1_pressed(pin) -> None:
    '''Interrupt handler for B1. Only sets a flag: no servo moves inside an interrupt.'''
    global wrist_flag,last_press
    now=time.ticks_ms()
    if time.ticks_diff(now,last_press)>200: # Ignore bounces within 200 ms
        last_press=now
        wrist_flag=True
    return

B1.irq(trigger=Pin.IRQ_FALLING,handler=b1_pressed)

#  Start with the pen UP so it doesn't mark the page (before the while True loop)
move(S3,WRIST_UP)


target=None # Init so the if doesn't throw an error before calc() is used
# if wrist_flag:
#  wrist_flag=False
# toggle_Wrist()
while True:
    if not target==gettarget(): # Act only if there's been a change since last reading
        target=gettarget() # Potentiometer positions list is taken to form the coordinates of the target
        reqangles=calc(target)
        move(S1,reqangles[0]) # Move the first servo to its target
        move(S2,reqangles[1])
   
