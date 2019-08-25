# Simple MicroPython ESP32 Module for BPI:bit/Web:bit by Alan Wang
# https://micropython.org/download
# http://docs.micropython.org/en/latest/esp32/quickref.html#
# http://wiki.banana-pi.org/BPI-Bit
import machine
from machine import Pin, TouchPad, ADC, PWM, I2C, SPI
from neopixel import NeoPixel
import micropython
import math
import uos
import utime
import gc

# MPU9250 (MPU6500 + AK8963): https://github.com/tuupola/micropython-mpu9250
from mpu9250 import MPU9250
from ak8963 import AK8963

# mapping dictionaries
_analogPins = {3:13, 0:25, 4:16, 5:35, 6:12, 7:14, 1:32, 10:26, 11:27, 12:2, 2:33}
_digitalPins = {3:13, 0:25, 4:16, 5:35, 6:12, 7:14, 1:32, 8:16, 9:17, 10:26, 11:27,
               12:2, 2:33, 13:18, 14:19, 15:23, 16:5, 19:22, 20:21}
_ledScreen = {0:4, 1:9, 2:14, 3:19, 4:24,
             5:3, 6:8, 7:13, 8:18, 9:23,
             10:2, 11:7, 12:12, 13:17, 14:22, 
             15:1, 16:6, 17:11, 18:16, 19:21,
             20:0, 21:5, 22:10, 23:15, 24:20}
_colorCodes = {'W':(16, 16, 16), 'R':(48, 0, 0), 'G':(0, 48, 0), 'B':(0, 0, 48),
              'Y':(24, 24, 0), 'C':(0, 24, 24), 'P':(24, 0, 24), '*':(0, 0, 0)}
_tones = {'C3':130.8128, 'C3D3':138.5913, 'D3':146.8324, 'D3E3':155.5635, 'E3':164.8138, 'F3':174.6141,
         'F3G3':184.9972, 'G3':195.9977, 'G3A3':207.6523, 'A3':220.0000, 'A3B3':233.0819, 'B3':246.9417,
         'C4':261.6256, 'C4D4':277.1826, 'D4':293.6648, 'D4E4':311.1270, 'E4':329.6276, 'F4':349.2282,
         'F4G4':369.9944, 'G4':391.9954, 'G4A4':415.3047, 'A4':440.0000, 'A4B4':466.1638, 'B4':493.8833,
         'C5':523.2511, 'C5D5':554.3653, 'D5':587.3295, 'D5E5':622.2540, 'E5':659.2551, 'F5':698.4565,
         'F5G5':739.9888, 'G5':783.9909, 'G5A5':830.6094, 'A5':880.0000, 'A5B5':932.3275, 'B5':987.7666,
         'C6':1046.502, 'C6D6':1108.731, 'D6':1174.659, 'D6E6':1244.508, 'E6':1318.510, 'F6':1396.913,
         'F6G6':1479.978, 'G6':1567.982, 'G6A6':1661.219, 'A6':1760.000, 'A6B6':1864.655, 'B6':1975.533,
         'C7':2093.005,
         '-': 0.0}
_axisName = {'x':0, 'y':1, 'z':2}

# functions

def help():
    print("MicroPython module for BPI:BIT by Alan Wang")
    print("- Online doc/source: github.com/alankrantas/micropython-BPIBIT")
    print("- Board: " + str(uos.uname()[4]))
    print("- Firmware: " + str(uos.uname()[3]))
    print("- CPU: " + str(machine.freq()) + " Hz")
    print("- Memory status:")
    print(micropython.mem_info())
    print("- Uploaded files: ")
    for file in uos.listdir():
        print(file)
    print("--------------------------------------------------")

def getI2C():
    return I2C(scl=Pin(_digitalPins[19]), sda=Pin(_digitalPins[20]), freq=400000)

def pause(delay):
    utime.sleep_ms(delay)

def runningTime():
    return utime.ticks_ms()

def digitalPin(pin):
    if pin in _digitalPins:
        return _digitalPins[pin]
    else:
        return 0

def analogPin(pin):
    if pin in _analogPins:
        return _analogPins[pin]
    else:
        return 0

def digitalReadPin(pin):
    if pin in _digitalPins:
        return Pin(_digitalPins[pin], Pin.IN).value()
    else:
        return 0

def digitalWritePin(pin, value):
    if (value is 0 or value is 1) and pin in _digitalPins:
        Pin(_digitalPins[pin], Pin.OUT).value(value)

def analogReadPin(pin):
    if pin in _analogPins:
        adc = ADC(Pin(_analogPins[pin]))
        adc.atten(ADC.ATTN_11DB)
        return adc.read() // 4
    else:
        return 0

def analogWritePin(pin, value):
    if value >= 0 and value <= 1023 and pin in _analogPins:
        pwm = PWM(Pin(_analogPins[pin]))
        pwm.freq(5000)
        pwm.duty(value)

def onButtonPressed(button):
    if button == 'AB':
        return Pin(_digitalPins[5], Pin.IN).value() is 0 and Pin(_digitalPins[11], Pin.IN).value() is 0
    elif button == 'A':
        return Pin(_digitalPins[5], Pin.IN).value() is 0
    elif button == 'B':
        return Pin(_digitalPins[11], Pin.IN).value() is 0
    else:
        return False

def pinIsTouched(pin):
    if pin in [1, 2]:
        return TouchPad(Pin(_digitalPins[pin])).read() < 350
    else:
        return False

def analogPitch(freq, delay):
    buzzer = PWM(Pin(_analogPins[0], Pin.OUT), freq=round(freq), duty=512)
    if delay > 0:
        if delay > 10:
            pause(delay - 10)
            buzzer.deinit()
            pause(10)
        else:
            pause(delay)
            buzzer.deinit()

def playTone(note, delay):
    if note in _tones:
        buzzer = PWM(Pin(_analogPins[0], Pin.OUT), freq=round(_tones[note]), duty=512)
        if delay > 0:
            if delay > 10:
                pause(delay - 10)
                buzzer.deinit()
                pause(10)
            else:
                pause(delay)
                buzzer.deinit()

def rest(delay):
    playTone('-', delay)

def noTone():
    buzzer = PWM(Pin(_analogPins[0], Pin.OUT), freq=0, duty=512)
    buzzer.deinit()

_lightSensorL = ADC(Pin(36))
_lightSensorL.atten(ADC.ATTN_11DB)
_lightSensorR = ADC(Pin(39))
_lightSensorR.atten(ADC.ATTN_11DB)

def lightLevelL():
    return _lightSensorL.read() // 4

def lightLevelR():
    return _lightSensorR.read() // 4

def lightLevel():
    return (_lightSensorL.read() + _lightSensorR.read()) / 2 // 4

_thermistor = ADC(Pin(34))
_thermistor.atten(ADC.ATTN_11DB)

def temperatureRaw():
    return _thermistor.read() // 4

def temperature():
    # see https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/NTC-0805-103F-3950F.pdf
    vOut = _thermistor.read() / 4095 * 3.3
    rt = 3.3 * 4700 / vOut - 4700
    temp = 3950 / math.log(rt / (10000 * math.exp(-3950 / (273.15 + 25))))
    return temp - 273.15

_mpu9250 = MPU9250(getI2C())

def acceleration(axis):
    if axis in _axisName:
        return _mpu9250.acceleration[_axisName[axis]]
    else:
        return 0

def rotationPitch():
    return (180 / math.pi) * math.atan2(acceleration('y'),
                             math.sqrt(math.pow(acceleration('x'), 2) + math.pow(acceleration('z'), 2)))

def rotationRoll():
    return (180 / math.pi) * math.atan2(acceleration('x'),
                             math.sqrt(math.pow(acceleration('y'), 2) + math.pow(acceleration('z'), 2)))

def gyroscope(axis):
    if axis in _axisName:
        return _mpu9250.gyro[_axisName[axis]] / (180 / math.pi)
    else:
        return 0

def magneticForce(axis):
    if axis in _axisName:
        return _mpu9250.magnetic[_axisName[axis]]
    else:
        return 0

def compassHeading():
    return (180 / math.pi) * math.atan2(magneticForce('y'), magneticForce('x'))

def calibrateCompass():
    print("Calibrating compass: keep turning BPI:BIT for 15 seconds.")
    ak8963 = AK8963(getI2C())
    offset, scale = ak8963.calibrate(count=150, delay=100)
    print("Calibration completed.")
    print("AK8963 offset:")
    print(offset)
    print("AK8963 scale:")
    print(scale)
    _mpu9250 = MPU9250(getI2C(), ak8963=ak8963)

_neoPixel = NeoPixel(Pin(4, Pin.OUT), 25)

def led(index, r, g, b):
    _neoPixel[_ledScreen[index]] = (r, g, b)
    _neoPixel.write()
    
def ledCode(index, code):
    if code in _colorCodes:
        _neoPixel[_ledScreen[index]] = _colorCodes[code]
        _neoPixel.write()

def ledCodeAll(code):
    if code in _colorCodes:
        for i in range(25):
            _neoPixel[_ledScreen[i]] = _colorCodes[code]
        _neoPixel.write()

def ledCodeArray(array):
    for i in range(25):
        if array[_ledScreen[i]] in _colorCodes:
            _neoPixel[i] = _colorCodes[array[_ledScreen[i]]]
    _neoPixel.write()

def lefOff():
    ledCodeAll('*')

def plotBarGraph(value, maxValue, code):
    if value >= 0 and maxValue > 0 and value <= maxValue:
        p = value / maxValue
        valueArray = [0.84, 0.88, 0.92, 0.96, 1.00,
                      0.64, 0.68, 0.72, 0.76, 0.80,
                      0.44, 0.48, 0.52, 0.56, 0.60,
                      0.24, 0.28, 0.32, 0.36, 0.40,
                      0.04, 0.08, 0.12, 0.16, 0.20]
        ledArray = []
        for i in range(25):
            if p >= valueArray[i]:
                ledArray.append(code)
            else:
                ledArray.append('*')
        ledCodeArray(ledArray)

lefOff()
noTone()
gc.enable()
gc.collect()
