# micropython-BPIBIT: A Simple MicroPython ESP32 Module for BPI:bit/Web:bit

![153543457141539355s6op3](https://user-images.githubusercontent.com/44191076/62682966-f88fb280-b9ef-11e9-83e4-47976fa68350.jpg)
![800x423xBPI_bit_interfact JPG pagespeed ic NngFYTGX_e](https://user-images.githubusercontent.com/44191076/62682983-047b7480-b9f0-11e9-8b0e-e7c8cc24b677.jpg)

This is purly a free personal project, I didn't get sponsorship or contact from Banana Pi, Webduino or whoever made this board.

[BPI:bit](http://wiki.banana-pi.org/BPI-Bit) (or Web:bit) is a ESP32 board made in the style of [BBC micro:bit](https://tech.microbit.org/hardware/); the edge connectors allow it can be used on micro:bit accessories.

The goals of this module are

* can be used under standard MicroPython firmware;
* remapped pin numbers so users can access them just like the way on micro:bits;
* most functions are named after their equivalents in micro:bit's MakeCode JavaScript Block editor.

And sorry, no text scrolling/number displaying yet. I'll try to figure it out in the future.

The module has been tested on <b>BPI:bit v1.2</b> and <b>MicroPython for ESP32 v1.11-37</b>.

## Flash MicroPython Firmware and Upload BPIBIT.py

You'll first need to flash firmware of MicroPython for ESP32 onto your BPI:bit:

[Firmware](http://micropython.org/download)

[Flash tool](https://www.espressif.com/en/support/download/other-tools)

I also recommend Thonny as the MicroPython editor:

[Thonny IDE](https://thonny.org/)

Remember to upload the BPIBIT.py onto your BPI:bit.

## Upload MPU-9250 Library

The module use this library to control the onboard MPU-9250 3-axis accelerometer/3-axis gyroscope/3-axis compass:

[MicroPython MPU-9250 (MPU-6500 + AK8963) I2C driver](https://github.com/tuupola/micropython-mpu9250) (Github)

Download the .zip file then upload <b>mpu9250.py</b>, <b>mpu6500.py</b> and <b>ak8963.py</b> onto your BPI:bit in the original name.

## Functions and Example

To use the module, simply import it:

```python
import BPIBIT
```

You can checkout some board information by using

```python
print(BPIBIT.systemInfo())
```

You'll get something like

```
System: ESP32 module with ESP32
MicroPython firmware: v1.11-37-g62f004ba4 on 2019-06-06
CPU: 240000000 Hz
Memory status:
stack: 1008 out of 15360
GC: total: 121088, used: 26816, free: 94272
 No. of 1-blocks: 347, 2-blocks: 64, max blk sz: 264, max free sz: 3263
None
Uploaded files: 
mpu9250.py
mpu6500.py
ak8963.py
```

### Return an I2C Object

```python
i2c = BPIBIT.getI2C()
```

### Pause/Delay/Wait (ms)

```
BPIBIT.pause(500)
```

### System Running Time (ms)

```
timeNow = BPIBIT.runningTime()
```

### Read/Write Pins

Read the signal of Pin 2 (of micro:bit), which would be remapped to GPIO 33 on ESP32:

```python
result = BPIBIT.digitalReadPin(pin=2)
BPIBIT.digitalWritePin(pin=2, value=0)
result = BPIBIT.analogReadPin(pin=2)
BPIBIT.analogWritePin(pin=2, value=1023)
```

You can also query the real pin by using

```python
realGPIO = BPIBIT.digitalPin(pin=2)
realGPIO = BPIBIT.analogPin(pin=2)
```

Available digital pins are 0-16; available analog pins are 0-7, 10-12.

Note: if you tur on ESP32's WiFi, only pin 1, 2 and 5 can b used as analog pins.

### Buttons and Touchpads

To tell if button A, B or both is/are being pressed:

```python
while True:
    print(BPIBIT.onButtonPressed(button='A'))
    BPIBIT.pause(100)
```

Button can be <b>'A'</b>, <b>'B'</b> or <b>'AB'</b>.

ESP32 also supports capacitive touch. However, only Pin 0, 1 and 2 are large enough to touch by finger, and Pin 0 (GPIO 25) does not support capacitive touch.

```python
print(BPIBIT.pinIsTouched(pin=2))
```

### Buzzer and Tone

You can play a tone via the onboard buzzer:

```python
BPIBIT.analogPitch(freq=1047, delay=500)
```

Or use music notes:

```python
BPIBIT.playTone(note='C6', delay=500)
```

The module has built-in notes from C3 (middle C) to C7. C2 sharp/D2 flat is expressed as 'C2D2', F4 sharp/G4 flat is 'F4G4', and so on.

If the delay time is set as 0 the tone won't stop.

You can stop tones by using

```python
BPIBIT.rest()
```

or turn off the buzzer completely (recommend if you need to access Pin 0/GPIO 25 which is shared by the buzzer):

```python
BPIBIT.noTone()
```

### Read Light Level and Temperature

Read average light level from two LDR sensors:

```python
while True:
    print(BPIBIT.lightLevel())
    BPIBIT.pause(100)
```

You can use <b>BPIBIT.lightLevelL()</b> and <b>BPIBIT.lightLevelR()</b> to get reading from a specific side.

Read approximate temperature (celsius) from the NTC thermistor:

```python
while True:
    print(BPIBIT.temperature())
    BPIBIT.pause(100)
```

As an analog sensor, the temperature reading would not be very accurate. The [NTC thermistor](https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/NTC-0805-103F-3950F.pdf) has B-value of 3950 and resistence of 10KΩ on 25 celsius. Also according to [BPI:bit v1.2 hardware](https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/BPI-WEBDUINO-BIT-V1_2.pdf) the thermistor has a 4K7Ω pull-down resistor.

Or you can simply use BPIBIT.temperatureRaw() to get the original analog value.

### Acceleration, Gyroscope and Compass

There are a series of functions related to the MPU-9250:

```python
print(BPIBIT.acceleration('x'))
print(BPIBIT.rotationPitch())
print(BPIBIT.rotationRoll())
print(BPIBIT.gyroscope('y'))
print(BPIBIT.magneticForce('z'))
print(BPIBIT.compassHeading())
BPIBIT.calibrateCompass()
```

Right now the compass calibration takes 15 seconds, in which you'll have to turn your BPI:bit around in all directions.

## NeoPixel LED Display

```python
BPIBIT.led(index=0, r=255, g=255, b=0)
BPIBIT.ledCode(index=5, code='R')
BPIBIT.ledCodeAll(code='G')
BPIBIT.ledOff()
```

Color codes are a few pre-defined colors:

* W = white (R+G+B)
* R = red
* Y = yellow
* G = green
* C = cyan
* B = blue
* P = Purple
* asterisk = black (off)

Since the NeoPixel LEDs at full power can be very bright and hot (3 LEDs on my board are partially burnt because of this), I reduced all light levels of the color codes. You'll have to use <b>BPIBIT.led(r, g, b)</b> to set "normal" light levels.

You can code the display pattern like this:

```python
ledArray = ['P', '*', 'B', '*', 'P',
            '*', 'Y', '*', 'Y', '*',
            '*', 'C', '*', 'C', '*',
            '*', 'G', 'B', 'G', '*',
            '*', 'R', '*', 'R', '*']
BPIBIT.ledCodeArray(array=ledArray)
```

Or use the display as a dynamic bar graph:

```python
BPIBIT.plotBarGraph(value=lightLevel(), maxValue=1023, code='W')
```
