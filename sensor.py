import HD44780 as LCD
import time
import RPi.GPIO as GPIO

lcd = LCD.HD44780('lcdsample.conf')
lcd.init()

def pulse_in(pin, value=GPIO.HIGH, timeout=1.0):
    start_time = time.time()
    not_value = (not value)
    while GPIO.input(pin) == value:
        if time.time() - start_time > timeout:
            return 0
    while GPIO.input(pin) == not_value:
        if time.time() - start_time > timeout:
            return 0
    start = time.time()
    while GPIO.input(pin) == value:
        if time.time() - start_time > timeout:
            return 0
    end = time.time()

    return end - start


def init_sensors(trig, echo, mode=GPIO.BCM):
    GPIO.cleanup()
    GPIO.setmode(mode)
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)


def get_distance(trig, echo, temp=15):
    GPIO.output(trig, GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)
    dur = pulse_in(echo, GPIO.HIGH, 1.0)
    return dur * (331.50 + 0.61 * temp) * 50


if __name__ == "__main__":

    GPIO_TRIG = 26
    GPIO_ECHO = 18
    
    count = 0
    
    init_sensors(GPIO_TRIG, GPIO_ECHO)
    while True:
        ans = round(get_distance(GPIO_TRIG, GPIO_ECHO),1)
        print("距離：{0} cm".format(ans))
        lcd.message(f'    キョリ {ans}cm     ',2)
        time.sleep(0.1)

                