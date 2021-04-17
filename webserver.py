from flask import Flask
import pigpio
import time
import math

app = Flask(__name__)
pi = pigpio.pi()

@app.route('/')
def index():
    pi.set_PWM_dutycycle(17, 255)
    pi.set_PWM_dutycycle(22, 255)
    pi.set_PWM_dutycycle(24, 255)
    return 'On!'

@app.route('/off')
def off():
    pi.set_PWM_dutycycle(17, 0)
    pi.set_PWM_dutycycle(22, 0)
    pi.set_PWM_dutycycle(24, 0)
    return 'Off!'

@app.route('/color:<red>/<green>/<blue>')
def color(red, green, blue):
    on = 0
    red = int(red)
    green = int(green)
    blue = int(blue)
    if red > 255:
        red = 255
    if green > 255:
        green = 255
    if blue > 255:
        blue = 255
    pi.set_PWM_dutycycle(17, red)
    pi.set_PWM_dutycycle(22, green)
    pi.set_PWM_dutycycle(24, blue)
    return 'Color!'


@app.route('/rainbow')
def rainbow():
    red = 255
    green = 0
    blue = 0
    while 1==1:
        pi.set_PWM_dutycycle(17, red)
        pi.set_PWM_dutycycle(22, green)
        pi.set_PWM_dutycycle(24, blue)
        if red == 255 and green <= 255 and blue == 0:
            green += 1
        elif red <= 255 and red > 0 and green == 255 and blue == 0:
            red -= 1
        elif red == 0 and green == 255 and blue <= 255:
            blue += 1
        elif red == 0 and green <= 255 and green > 0 and blue == 255:
            green -= 1
        elif red <= 255 and green == 0 and blue == 255:
            red += 1
        elif red == 255 and green == 0 and blue <= 255 and blue > 0:
            blue -= 1
        print(red+", "+green+", "+blue)
    return 'Rainbow!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')