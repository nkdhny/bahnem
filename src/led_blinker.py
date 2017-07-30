import RPi.GPIO as GPIO
import time

LED = 4

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED, GPIO.OUT)
blinker = GPIO.PWM(LED, 1)
print "Start blinking with freq = 1Hz"
blinker.start(50)
time.sleep(5)
print "Start blinking with freq = 10Hz"
blinker.ChangeFrequency(10)
time.sleep(5)
print "Start blinking with freq = 1000Hz"
blinker.ChangeFrequency(1000)
time.sleep(5)
print "LED off"
blinker.stop()
