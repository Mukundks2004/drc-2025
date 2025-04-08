import RPi.GPIO as GPIO
import time

# Define GPIO pins for motor control
LEFT_MOTOR_PIN = 17
RIGHT_MOTOR_PIN = 18

# Set up GPIO mode and pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_MOTOR_PIN, GPIO.OUT)
GPIO.setup(RIGHT_MOTOR_PIN, GPIO.OUT)

# Set up PWM for motor control (50Hz frequency)
LEFT_MOTOR_PWM = GPIO.PWM(LEFT_MOTOR_PIN, 50)
RIGHT_MOTOR_PWM = GPIO.PWM(RIGHT_MOTOR_PIN, 50)

LEFT_MOTOR_PWM.start(0)  # Initially, 0% speed
RIGHT_MOTOR_PWM.start(0)  # Initially, 0% speed

def move_forward(speed=50):
    LEFT_MOTOR_PWM.ChangeDutyCycle(speed)  # Adjust speed (0 to 100)
    RIGHT_MOTOR_PWM.ChangeDutyCycle(speed)

def move_backward(speed=50):
    LEFT_MOTOR_PWM.ChangeDutyCycle(-speed)  # Reverse direction (negative)
    RIGHT_MOTOR_PWM.ChangeDutyCycle(-speed)

def stop_motors():
    LEFT_MOTOR_PWM.ChangeDutyCycle(0)  # Stop the motor
    RIGHT_MOTOR_PWM.ChangeDutyCycle(0)

def cleanup():
    LEFT_MOTOR_PWM.stop()
    RIGHT_MOTOR_PWM.stop()
