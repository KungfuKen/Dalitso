# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
from gpiozero import Buzzer
from time import sleep
# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
number = 0 #stores users guess
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = None
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    pass


# Setup Pins
def setup():
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # Setup regular GPIO
    chanList = [3, 5, 11, 13, 15, 33]
    GPIO.setup(chanList, GPIO.OUT)
    # Setup PWM channels
    GPIO.setup(32, GPIO.OUT)
    p = GPIO.PWM(32, 100)
    # Setup debouncing and callbacks
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(18, GPIO.RISING, callback=btn_increase_pressed())
    try:
        GPIO.wait_for_edge(16, GPIO.RISING, callback=btn_guess_pressed())
    except KeyboardInterrupt:
        GPIO.cleanup()
    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = eeprom.read_byte(0b00)
    # Get the scores
    scores = read_block(1, 12)
    # convert the codes back to ascii
    for i in scores
        scores += cha(i)
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
    count, score = fetch_scores()
    # include new score
    write_block(1, score)
    # sort
    # update total amount of scores
    write_byte(0, count)
    # write new scores
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3))


# Increase button pressed
def btn_increase_pressed():
    # Increase the value shown on the LEDs
    number += 1
    if number = 1; GPIO.output(11, True)
    if number = 2; GPIO.output(11, False) GPIO.output(11, True)
    if number = 3; GPIO.output(11, True)  GPIO.output(12, True)
    if number = 4; GPIO.output(11, False) GPIO.output(12, False) GPIO.output(13, True) 
    if number = 5; GPIO.output(11, True)  GPIO.output(12, False) GPIO.output(13, True)
    if number = 6; GPIO.output(11, False)  GPIO.output(12, True) GPIO.output(13, True)
    if number = 7; GPIO.output(11, True)  GPIO.output(12, True) GPIO.output(13, True)
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    accuracy_leds()
    trigger_buzzer()
    pass


# Guess button
def btn_guess_pressed():
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    GPIO.cleanup()
    menu()
    # Compare the actual value with the user value displayed on the LEDs
    value =  generate_number() 
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    if value == number;
    # - Disable LEDs and Buzzer
        GPIO.output(32, False)
        GPIO.output(33, False)
    # - tell the user and prompt them for a name
        name = input("Winner! Enter your name")
    # - fetch all the scores
    fetch_scores() 
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    save_scores()
    pass


# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    pmw = GPIO.PMW(32, 100)
    pmw.start(0)
    # - The % brightness should be directly proportional to the % "closeness"
    closeness = 0;
    ans = generate_number
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    if ans > number
        closeness = ans/number*100
    if ans < number
        closeness = ((8-number)/(8-ans))*100
    pmw.ChangeDutyCycle(closeness)
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    buzzer = Buzzer(33)
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    ans = generate_number
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    if abs(ans - number) == 3
        buzzer.beep(0.5, 0.5)
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    if abs(ans - number) == 2
        buzzer.beep(0.25, 0.25)
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    if abs(ans - number) == 1
        buzzer.beep(0.125, 0.125) 
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
