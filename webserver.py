from flask import Flask
import pigpio
import time
import os

app = Flask(__name__)
pi = pigpio.pi()
on = [0]

@app.route('/')
def index():
    on[0] = 0
    pi.set_PWM_dutycycle(17, 255)
    pi.set_PWM_dutycycle(22, 255)
    pi.set_PWM_dutycycle(24, 255)
    return 'ON!'


@app.route('/off')
def off():
    on[0] = 0
    pi.set_PWM_dutycycle(17, 0)
    pi.set_PWM_dutycycle(22, 0)
    pi.set_PWM_dutycycle(24, 0)
    return 'Off!'

@app.route('/color:<red>/<green>/<blue>')
def color(red, green, blue):
    on[0] = 0
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
    on[0] = 1
    red = 255
    green = 0
    blue = 0
    while on[0]==1:
        pi.set_PWM_dutycycle(17, red)
        pi.set_PWM_dutycycle(22, green)
        pi.set_PWM_dutycycle(24, blue)
        if red == 255 and green < 255 and blue == 0:
            green += 1
        elif red <= 255 and red > 0 and green == 255 and blue == 0:
            red -= 1
        elif red == 0 and green == 255 and blue < 255:
            blue += 1
        elif red == 0 and green <= 255 and green > 0 and blue == 255:
            green -= 1
        elif red < 255 and green == 0 and blue == 255:
            red += 1
        elif red == 255 and green == 0 and blue <= 255 and blue > 0:
            blue -= 1
        time.sleep(0.015)
    return 'Rainbow!'

@app.route('/restart')
def restart():
    pid = os.getpid()
    store = "sudo kill " + str(pid) + " | python /home/pi/python-server/webserver.py"  
    print(store)
    os.system(store)
    return 'Restart!'

    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')