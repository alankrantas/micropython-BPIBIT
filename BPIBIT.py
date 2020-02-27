# MicroPython ESP32 Module for BPI:bit/Web:bit by Alan Wang
# https://micropython.org/download
# http://docs.micropython.org/en/latest/esp32/quickref.html#
# http://wiki.banana-pi.org/BPI-Bit
import math, utime, gc
from machine import Pin, TouchPad, ADC, PWM, I2C, SPI
from neopixel import NeoPixel

# MPU9250 (MPU6500 + AK8963): https://github.com/tuupola/micropython-mpu9250
try:
    from mpu9250 import MPU9250
    from ak8963 import AK8963
    _mpu9250 = MPU9250(I2C(scl=Pin(22), sda=Pin(21), freq=400000))
except:
    print("Onboard MPU9250 failed to import driver or initialize")
    _mpu9250 = None

gc.enable()

# mapping dictionaries
_analogPitchPin = 0
_lightSensorL = ADC(Pin(36))
_lightSensorL.atten(ADC.ATTN_11DB)
_lightSensorR = ADC(Pin(39))
_lightSensorR.atten(ADC.ATTN_11DB)
_thermistor = ADC(Pin(34))
_thermistor.atten(ADC.ATTN_11DB)
_neoPixel = NeoPixel(Pin(4, Pin.OUT), 25)
_analogPins = {3:13, 0:25, 4:16, 5:35, 6:12, 7:14, 1:32, 10:26, 11:27, 12:2, 2:33}
_digitalPins = {'BUILTIN_LED':18, 3:13, 0:25, 4:16, 5:35, 6:12, 7:14, 1:32, 8:16, 9:17, 10:26, 11:27, 12:2, 2:33, 13:18, 14:19, 15:23, 16:5, 19:22, 20:21}
_touchpads = {3:13, 6:12, 7:14, 1:32, 11:27, 2:33}
_ledScreen = {0:4, 1:9, 2:14, 3:19, 4:24, 5:3, 6:8, 7:13, 8:18, 9:23, 10:2, 11:7, 12:12, 13:17, 14:22, 15:1, 16:6, 17:11, 18:16, 19:21, 20:0, 21:5, 22:10, 23:15, 24:20}
_colorCodes = {'W':(16, 16, 16), 'R':(48, 0, 0), 'G':(0, 48, 0), 'B':(0, 0, 48), 'Y':(24, 24, 0), 'C':(0, 24, 24), 'P':(24, 0, 24), 'O':(36, 12, 0), 'T':(0, 36, 12), 'V':(12, 0, 36), '*':(0, 0, 0)}
_tones = {'C3':130.8128, 'C3D3':138.5913, 'D3':146.8324, 'D3E3':155.5635, 'E3':164.8138, 'F3':174.6141, 'F3G3':184.9972, 'G3':195.9977, 'G3A3':207.6523, 'A3':220.0000, 'A3B3':233.0819, 'B3':246.9417, 'C4':261.6256, 'C4D4':277.1826, 'D4':293.6648, 'D4E4':311.1270, 'E4':329.6276, 'F4':349.2282, 'F4G4':369.9944, 'G4':391.9954, 'G4A4':415.3047, 'A4':440.0000, 'A4B4':466.1638, 'B4':493.8833, 'C5':523.2511, 'C5D5':554.3653, 'D5':587.3295, 'D5E5':622.2540, 'E5':659.2551, 'F5':698.4565, 'F5G5':739.9888, 'G5':783.9909, 'G5A5':830.6094, 'A5':880.0000, 'A5B5':932.3275, 'B5':987.7666,  'C6':1046.502, 'C6D6':1108.731, 'D6':1174.659, 'D6E6':1244.508, 'E6':1318.510, 'F6':1396.913, 'F6G6':1479.978, 'G6':1567.982, 'G6A6':1661.219, 'A6':1760.000, 'A6B6':1864.655, 'B6':1975.533, 'C7':2093.005, '*': 0.0, ' ': 0.0}
_axisName = {'x':0, 'y':1, 'z':2}
_fonts = {'A':['*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*'],
          'B':['X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*'],
          'C':['*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*'],
          'D':['X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*'],
          'E':['X', 'X', 'X', 'X', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', 'X', '*'],
          'F':['X', 'X', 'X', 'X', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*'],
          'G':['*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', 'X', 'X', 'X', '*', '*', '*', 'X', '*', 'X', 'X', 'X', '*'],
          'H':['X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*'],
          'I':['X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', 'X', '*', '*'],
          'J':['X', 'X', 'X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*'],
          'K':['X', '*', '*', 'X', '*', 'X', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', '*'],
          'L':['X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', 'X', '*'],
          'M':['X', '*', '*', '*', 'X', 'X', 'X', '*', 'X', 'X', 'X', '*', 'X', '*', 'X', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X'],
          'N':['X', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', 'X', '*', 'X', '*', 'X', 'X', '*', '*', 'X', 'X', 'X', '*', '*', '*', 'X'],
          'O':['*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*'],
          'P':['X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*'],
          'Q':['*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*', '*', 'X', 'X', '*'],
          'R':['X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', '*', 'X'],
          'S':['*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', '*', '*', 'X', 'X', '*', '*', '*', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*'],
          'T':['X', 'X', 'X', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*'],
          'U':['X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*'],
          'V':['X', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X', '*', 'X', '*', 'X', '*', '*', '*', 'X', '*', '*'],
          'W':['X', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X', 'X', '*', 'X', '*', 'X', 'X', 'X', '*', 'X', 'X', 'X', '*', '*', '*', 'X'],
          'X':['X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*'],
          'Y':['X', '*', '*', '*', 'X', '*', 'X', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*'],
          'Z':['X', 'X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', 'X', '*'],
          'a':['*', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', 'X', 'X'],
          'b':['X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*'],
          'c':['*', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*'],
          'd':['*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', 'X', 'X', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', 'X', '*'],
          'e':['*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*'],
          'f':['*', '*', 'X', 'X', '*', '*', 'X', '*', '*', '*', 'X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*'],
          'g':['*', 'X', 'X', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', 'X', '*', '*', '*', '*', 'X', '*', '*', 'X', 'X', 'X', '*'],
          'h':['X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*'],
          'i':['X', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*'],
          'j':['*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*'],
          'k':['X', '*', '*', '*', '*', 'X', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', '*'],
          'l':['X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', 'X', '*', '*'],
          'm':['*', '*', '*', '*', '*', 'X', 'X', '*', 'X', 'X', 'X', '*', 'X', '*', 'X', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X'],
          'n':['*', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*'],
          'o':['*', '*', '*', '*', '*', '*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*'],
          'p':['*', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*'],
          'q':['*', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', 'X', '*', '*', '*', '*', 'X', '*'],
          'r':['*', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*'],
          's':['*', '*', '*', '*', '*', '*', '*', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*'],
          't':['*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', 'X', 'X'],
          'u':['*', '*', '*', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', 'X', 'X'],
          'v':['*', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X', '*', 'X', '*', 'X', '*', '*', '*', 'X', '*', '*'],
          'w':['*', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X', 'X', '*', 'X', '*', 'X', 'X', 'X', '*', 'X', 'X'],
          'x':['*', '*', '*', '*', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*'],
          'y':['*', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', 'X', '*', 'X', '*', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*'],
          'z':['*', '*', '*', '*', '*', 'X', 'X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', 'X', 'X', '*'],
          '0':['*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*'],
          '1':['*', '*', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', 'X', '*'],
          '2':['X', 'X', 'X', '*', '*', '*', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', 'X', 'X', '*'],
          '3':['X', 'X', 'X', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*'],
          '4':['*', '*', '*', 'X', '*', '*', '*', 'X', 'X', '*', '*', 'X', '*', 'X', '*', 'X', 'X', 'X', 'X', 'X', '*', '*', '*', 'X', '*'],
          '5':['X', 'X', 'X', 'X', 'X', 'X', '*', '*', '*', '*', 'X', 'X', 'X', 'X', '*', '*', '*', '*', '*', 'X', 'X', 'X', 'X', 'X', '*'],
          '6':['*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', 'X', '*', 'X', 'X', 'X', '*'],
          '7':['X', 'X', 'X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*'],
          '8':['*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', 'X', '*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', 'X', '*', 'X', 'X', 'X', '*'],
          '9':['*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*'],
          ',':['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*'],
          '.':['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          '!':['X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*'],
          ':':['*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          ';':['*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*'],
          '+':['*', '*', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*'],
          '-':['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          '*':['*', '*', '*', '*', '*', 'X', '*', 'X', '*', '*', 'X', 'X', '*', '*', '*', 'X', '*', 'X', '*', '*', '*', '*', '*', '*', '*'],
          '/':['*', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*'],
          '=':['*', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', '*', '*', '*', '*', '*', 'X', 'X', 'X', '*', '*', '*', '*', '*', '*', '*'],
          '_':['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', 'X', 'X', 'X', 'X'],
          '|':['*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*'],
          '\\':['X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X'],
          '`':['X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          '~':['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', 'X', 'X', '*', '*', '*', '*', '*', 'X', 'X', '*', '*', '*', '*', '*', '*'],
          '@':['*', 'X', 'X', 'X', '*', 'X', '*', '*', '*', 'X', 'X', '*', 'X', '*', 'X', 'X', '*', '*', 'X', 'X', '*', 'X', 'X', '*', '*'],
          '#':['*', 'X', '*', 'X', '*', 'X', 'X', 'X', 'X', 'X', '*', 'X', '*', 'X', '*', 'X', 'X', 'X', 'X', 'X', '*', 'X', '*', 'X', '*'],
          '$':['*', 'X', 'X', 'X', '*', 'X', 'X', '*', '*', 'X', '*', 'X', 'X', 'X', '*', '*', '*', '*', 'X', 'X', '*', 'X', 'X', 'X', '*'],
          '%':['X', 'X', '*', '*', 'X', 'X', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', 'X', 'X'],
          '^':['*', 'X', '*', '*', '*', 'X', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          '&':['*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', '*', 'X', '*', '*', 'X', '*', '*', 'X', 'X', '*', 'X'],
          '\'':['X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          '\"':['X', '*', 'X', '*', '*', 'X', '*', 'X', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
          '(':['*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', '*', '*', '*'],
          ')':['X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*'],
          '[':['X', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', '*', '*', '*'],
          ']':['X', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*'],
          '{':['*', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', '*', '*'],
          '}':['X', 'X', '*', '*', '*', '*', 'X', '*', '*', '*', '*', 'X', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', 'X', '*', '*', '*'],
          '<':['*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', '*', '*'],
          '>':['X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', 'X', '*', '*', '*', '*'],
          ' ':['*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*', '*']}
_fontsWidth = {'A':4, 'B':4, 'C':4, 'D':4, 'E':4, 'F':4, 'G':5, 'H':4, 'I':3, 'J':5, 'K':4, 'L':4, 'M':5, 'N':5, 'O':4, 'P':4, 'Q':4, 'R':5, 'S':4, 'T':5, 'U':4, 'V':5, 'W':5, 'X':4, 'Y':5, 'Z':4, 'a':5, 'b':4, 'c':4, 'd':4, 'e':4, 'f':4, 'g':5, 'h':4, 'i':1, 'j':3, 'k':4, 'l':3, 'm':5, 'n':4, 'o':4, 'p':4, 'q':4, 'r':4, 's':4, 't':5, 'u':5, 'v':5, 'w':5, 'x':4, 'y':5, 'z':4, '0':4, '1':4, '2':4, '3':4, '4':5, '5':5, '6':5, '7':5, '8':5, '9':5, ',':1, '.':2, '!':1, ':':1, ';':2, '+':3, '-':3, '*':3, '/':5, '_':5, '=':3, '|':3, '\\':5, '`':2, '~':4, '@':5, '#':5, '$':5, '%':5, '^':3, '&':5, '\'':1, '\"':3, '(':2, ')':2, '[':2, ']':2, '{':3, '}':3, '<':3, '>':3, ' ':3}

gc.collect()

def getI2C(scl=19, sda=20, freq=400000):
    return I2C(scl=Pin(_digitalPins[scl]), sda=Pin(_digitalPins[sda]), freq=freq)

def getSPI(sck=13, miso=14, mosi=15, baudrate=1000000, polarity=1, phase=0):
    return SPI(baudrate=baudrate, polarity=polarity, phase=phase, sck=Pin(_digitalPins[sck]), mosi=Pin(_digitalPins[mosi]), miso=Pin(_digitalPins[miso]))

def getHSPI(baudrate=10000000, polarity=1, phase=0):
    return SPI(1, baudrate=baudrate, polarity=polarity, phase=phase, sck=Pin(_digitalPins[7]), mosi=Pin(_digitalPins[3]), miso=Pin(_digitalPins[6]))

def getVSPI(baudrate=10000000, polarity=1, phase=0):
    return SPI(2, baudrate=baudrate, polarity=polarity, phase=phase, sck=Pin(_digitalPins[13]), mosi=Pin(_digitalPins[15]), miso=Pin(_digitalPins[14]))

def pause(delay):
    utime.sleep_ms(delay)
    
def pauseMicros(delay):
    utime.sleep_us(delay)

def runningTime():
    return utime.ticks_ms()

def runningTimeMicros():
    return utime.ticks_us()

def digitalReadPin(pin):
    return Pin(_digitalPins[pin], Pin.IN).value()

def digitalWritePin(pin, value):
    Pin(_digitalPins[pin], Pin.OUT).value(value)

def analogReadPin(pin):
    adc = ADC(Pin(_analogPins[pin]))
    adc.atten(ADC.ATTN_11DB)
    return adc.read() // 4

def analogWritePin(pin, value, freq=5000):
    pwm = PWM(Pin(_digitalPins[pin]), freq=freq, duty=value)

def servoWritePin(pin, degree):
    actual_degree = int(degree * (122 - 30) / 180 + 30)
    servo = PWM(Pin(_digitalPins[pin]), freq=50, duty=actual_degree)

def servoWritePinOff(pin):
    servo = PWM(Pin(_digitalPins[pin]), freq=50, duty=0)
    servo.deinit()

def onButtonPressed(button):
    button_a = Pin(_digitalPins[5], Pin.IN)
    button_b = Pin(_digitalPins[11], Pin.IN)
    if button == 'AB':
        return button_a.value() == 0 and button_b.value() == 0
    elif button == 'A':
        return button_a.value() == 0
    elif button == 'B':
        return button_b.value() == 0
    else:
        return False

def pinIsTouched(pin, level=350):
    return TouchPad(Pin(_touchpads[pin])).read() < level if pin in _touchpads else False

def analogSetPitchPin(pin):
    _analogPitchPin = pin

def analogPitch(freq, delay):
    delay = round(delay)
    buzzer = PWM(Pin(_digitalPins[_analogPitchPin], Pin.OUT), freq=round(freq), duty=512)
    if delay > 0:
        if delay > 10:
            pause(delay - 10)
            buzzer.deinit()
            pause(10)
        else:
            pause(delay)
            buzzer.deinit()

def playTone(note, delay=0):
    analogPitch(freq=_tones.get(note, 0.0), delay=delay)

def rest(delay=0):
    playTone(note='*', delay=delay)

def noTone():
    buzzer = PWM(Pin(_digitalPins[_analogPitchPin], Pin.OUT), freq=0, duty=512)
    buzzer.deinit()

def lightLevelL():
    return _lightSensorL.read() // 4

def lightLevelR():
    return _lightSensorR.read() // 4

def lightLevel():
    return (_lightSensorL.read() + _lightSensorR.read()) / 2 // 4

def temperatureRaw():
    return _thermistor.read() // 4

def temperature(rntc=5100):
    # see https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/NTC-0805-103F-3950F.pdf
    return 3950 / math.log((3.3 * rntc / (_thermistor.read() / 4095 * 3.3) - rntc) / (10000 * math.exp(-3950 / (273.15 + 25)))) - 273.15

def acceleration(axis=''):
    if _mpu9250:
        if axis == '':
            return abs(_mpu9250.acceleration[_axisName['x']]) + abs(_mpu9250.acceleration[_axisName['y']]) + abs(_mpu9250.acceleration[_axisName['x']])
        else:
            return _mpu9250.acceleration[_axisName[axis]] if axis in _axisName else None
    else:
        return None

def rotationPitch():
    if _mpu9250:
        return (180 / math.pi) * math.atan2(acceleration('y'), math.sqrt(math.pow(acceleration('x'), 2) + math.pow(acceleration('z'), 2)))
    else:
        return None

def rotationRoll():
    if _mpu9250:
        return (180 / math.pi) * math.atan2(acceleration('x'), math.sqrt(math.pow(acceleration('y'), 2) + math.pow(acceleration('z'), 2)))
    else:
        return None

def gyroscope(axis):
    if _mpu9250:
        return _mpu9250.gyro[_axisName[axis]] if axis in _axisName else None
    else:
        return None

def magneticForce(axis=''):
    if _mpu9250:
        if axis == '':
            return abs(_mpu9250.magnetic[_axisName['x']]) + abs(_mpu9250.magnetic[_axisName['y']]) + abs(_mpu9250.magnetic[_axisName['z']])
        else:
            return _mpu9250.magnetic[_axisName[axis]] if axis in _axisName else None
    else:
        return None

def compassHeading():
    if _mpu9250:
        return (180 / math.pi) * math.atan2(magneticForce('y'), magneticForce('x'))
    else:
        return None

def calibrateCompass():
    if _mpu9250:
        i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
        print("Calibrating compass: keep turning BPI:BIT for 15 seconds.")
        ak8963 = AK8963(i2c)
        offset, scale = ak8963.calibrate(count=150, delay=100)
        print("Calibration completed.")
        print("AK8963 offset:")
        print(offset)
        print("AK8963 scale:")
        print(scale)
        _mpu9250 = MPU9250(i2c, ak8963=ak8963)

def led(index, color):
    _neoPixel[_ledScreen[index]] = color
    _neoPixel.write()

def ledAll(color):
    _neoPixel.fill(color)
    _neoPixel.write()

def ledCode(index, code):
    _neoPixel[_ledScreen[index]] = _colorCodes[code]
    _neoPixel.write()

def ledCodeAll(code):
    _neoPixel.fill(_colorCodes[code])
    _neoPixel.write()

def ledCodeArray(array):
    for i in range(25):
        _neoPixel[i] = _colorCodes[array[_ledScreen[i]]]
    _neoPixel.write()

def ledOff():
    ledCodeAll('*')

def plotBarGraph(value, maxValue=1023, code='W'):
    p = value / maxValue
    valueArray = [0.96, 0.88, 0.84, 0.92, 1.00, 0.76, 0.68, 0.64, 0.72, 0.80, 0.56, 0.48, 0.44, 0.52, 0.60, 0.36, 0.28, 0.24, 0.32, 0.40, 0.16, 0.08, 0.04, 0.12, 0.20]
    ledArray = []
    for i in range(25):
        ledArray.append(code if p >= valueArray[i] else '*')
    ledCodeArray(ledArray)

def scrollText(text, delay=150, code='W'):
    ledMain = ['*'] * 25
    ledBuff = ['*'] * 25
    scrolltime = 0
    c = ''
    for l, t in enumerate(text):
        c = t if t in _fonts.keys() else ' '
        for i in range(25):
            ledBuff[i] = code if _fonts[c][i] != '*' else '*'
        scrolltime = 10 if l == len(text) - 1 else _fontsWidth[c] + 1
        for i in range(scrolltime):
            tmp = [ledBuff[0], ledBuff[5], ledBuff[10], ledBuff[15], ledBuff[20]]
            for j in range(5):
                for k in range(5):
                    index = j + k * 5
                    if j < 4:
                        ledMain[index] = ledMain[index + 1]
                        ledBuff[index] = ledBuff[index + 1]
                    else:
                        ledMain[index] = tmp[k]
                        ledBuff[index] = '*'
            ledCodeArray(ledMain)
            pause(delay)

noTone()
ledOff()
