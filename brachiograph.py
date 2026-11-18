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
    La = 155 # length from shoulder to elblow = 155 mm
    Lb = 155 # length from elbow to wrist = 155 mm
    
    end_position_x = float(end_position_x)
    end_position_y = float(end_position_y)
    
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
    
    resulting_angles = [alpha, beta]
    
    return (resulting_angles)

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
