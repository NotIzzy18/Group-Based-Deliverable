from machine import Pin,PWM,ADC

# Declare hardware constants: three servos and two buttons

def translate():
    '''Takes an angle (arg1, int) and translates it into a 16-bit value that
    can be used as a duty factor to move a servo. Returns nothing.'''
    pass

def move():
    '''Moves a servo (arg1, PWM) by arg2 (int) degrees using translate().
    Returns nothing.'''
    pass

def gettarget():
    '''Takes the positions of the potentiometers and turns them into xy coordinates.
    Reads the potentiometers, filters out analogue noise and returns a two-element
    list, being the x and y coordinates of the target. Takes no arguments.'''
    pass

def calc():
    '''Takes a two-element list (arg1) of xy coordinates (probably from gettarget())
    and calculates the angles required to reach that target. Returns a two-element
    list of the angles.'''
    pass

def toggle_wrist():
    '''Toggles the wrist by first querying the wrist servo.
    Takes no arguments and returns nothing.'''
    pass

target=None
while True: # Main loop
    if not target_is_the_same_as_last_reading:
        # Set target using gettarget()
        # calc() the target
        # move() the servos
        pass
