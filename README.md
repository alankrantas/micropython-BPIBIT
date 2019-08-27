# micropython-BPIBIT: A Simple MicroPython ESP32 Module for BPI:bit/Web:bit (BETA)

![153543457141539355s6op3](https://user-images.githubusercontent.com/44191076/62682966-f88fb280-b9ef-11e9-83e4-47976fa68350.jpg)
![800x423xBPI_bit_interfact JPG pagespeed ic NngFYTGX_e](https://user-images.githubusercontent.com/44191076/62682983-047b7480-b9f0-11e9-8b0e-e7c8cc24b677.jpg)

This is a free personal project, I didn't get sponsorship or contact from Banana Pi, Webduino or whoever made this board.

[BPI:bit](http://wiki.banana-pi.org/BPI-Bit) (or Web:bit) is a ESP32 board made in the style of [BBC micro:bit](https://tech.microbit.org/hardware/); the edge connectors allow it to be used on micro:bit accessories.

The objectives of this module are

* can be used under standard MicroPython ESP32 firmware, which can be integrated with lots of MicroPython libraries;
* pins can be referenced via micro:bit pin numbers, which is easier to remember and will be mapped to corresponding ESP32 pins;
* most functions are also named after their equivalents in micro:bit's MakeCode JavaScript Block editor.

And sorry, no text scrolling/number displaying. I'll try to figure it out in the future. MicroPython also currently does not support Bluetooth-related functions.

This module has been tested on <b>BPI:bit v1.2</b> and <b>MicroPython for ESP32 v1.11-37</b>.

## Flash MicroPython Firmware and Upload BPIBIT.py

You'll first need to flash [firmware](http://micropython.org/download) of MicroPython for ESP32 by using [flash tool](https://www.espressif.com/en/support/download/other-tools) onto your BPI:bit. I also recommend [Thonny IDE](https://thonny.org/) as the MicroPython editor and library uploader.

First download the firmware .bin file, standard version, without SPIRAM support, then set the flash tool as below (select the COM or communication port which your board is connected):

![flash](https://user-images.githubusercontent.com/44191076/63651786-74795100-c78b-11e9-864d-d4435f677fa6.jpg)

In Thonny you must go to Tools -> Options and set interpreter to MicroPython:

![thonny1](https://user-images.githubusercontent.com/44191076/63651827-d46ff780-c78b-11e9-87b3-638976919beb.jpg)

When the board is successfully linked you'll see the message below in REPL: (If not, try to reconnect the board and click Stop/Restart several times.)

![thonny2](https://user-images.githubusercontent.com/44191076/63651882-60821f00-c78c-11e9-9625-995681e883e5.jpg)

Finally open BPIBIT.py in Thonny and upload it onto your board:

![thonny3](https://user-images.githubusercontent.com/44191076/63651913-9aebbc00-c78c-11e9-8e17-45fcae7b95df.jpg)

## Upload MPU-9250 Library

The module requires this library to control the onboard MPU-9250 3-axis accelerometer/3-axis gyroscope/3-axis compass:

[MicroPython MPU-9250 (MPU-6500 + AK8963) I2C driver](https://github.com/tuupola/micropython-mpu9250) (Github)

Download the .zip file, unzip then upload <b>mpu9250.py</b>, <b>mpu6500.py</b> and <b>ak8963.py</b> onto your BPI:bit in their original name.

## Functions and Example

To use the module, simply import it:

```python
import BPIBIT
```

You can checkout basic board information by using

```python
BPIBIT.help()
```

You'll get something in the REPL like

```
MicroPython module for BPI:BIT by Alan Wang
- Online doc/source: github.com/alankrantas/micropython-BPIBIT
- Board: ESP32 module with ESP32
- Firmware: v1.11-37-g62f004ba4 on 2019-06-06
- CPU: 240000000 Hz
- Memory status:
stack: 1008 out of 15360
GC: total: 121088, used: 26528, free: 94560
 No. of 1-blocks: 333, 2-blocks: 55, max blk sz: 264, max free sz: 3593
None
- Uploaded files: 
boot.py
BPIBIT.py
mpu6500.py
mpu9250.py
ak8963.py
```

### Pause/Delay/Wait (ms)

```python
BPIBIT.pause(500)
```

### Get System Running Time (ms)

```python
timeNow = BPIBIT.runningTime()
```

### Read/Write Pins

Read the signal of Pin 2 (of micro:bit), which would be remapped to GPIO 33 on ESP32:

```python
result = BPIBIT.digitalReadPin(pin=2)
result = BPIBIT.analogReadPin(pin=2)
BPIBIT.digitalWritePin(pin=2, value=1)
BPIBIT.analogWritePin(pin=2, value=1023)
```

You can also query the real pin number by using

```python
from machine import Pin

realGPIO = BPIBIT.digitalPin(pin=2)
pin = Pin(realGPIO, PIN.OUT)
```

Available digital pins for output/input are 0-16 (of micro:bit); available analog pins for innput are 0-7, 10-12 (of micro:bit). Analog pins for output (PWM) are as same as digital ones. Of course, Pin 5 and 11 are already connected to button A/B and the buzzer is on Pin 0.

Note: if you tur on ESP32's WiFi, only pin 1, 2 and 5 can be used as analog pins. See [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/) for more details.

### Servo Control

Control a servo from one of the digital pins via PWM, which can be set to 0-180 degrees. Note: the actual turning range may not be precisely 180 degrees.

```python
while True:
    BPIBIT.servoWritePin(pin=2, degree=0)
    BPIBIT.pause(1000)
    BPIBIT.servoWritePin(pin=2, degree=180)
    BPIBIT.pause(1000)
```

### Buttons and Touchpads

To tell if button A, B or both is/are being pressed:

```python
while True:
    print(BPIBIT.onButtonPressed(button='A'))
    BPIBIT.pause(100)
```

Return True/False. Button can be <b>'A'</b>, <b>'B'</b> or <b>'AB'</b> (both).

ESP32 also supports capacitive touch. However, only Pin 0, 1 and 2 are large enough to touch by finger, and Pin 0 (GPIO 25) does not support capacitive touch. Hence in this module only pin 1 and 2 supports capacitive touch.

```python
print(BPIBIT.pinIsTouched(pin=2))
```

### Buzzer and Tone

You can play a tone of specific frequency via the onboard buzzer:

```python
BPIBIT.analogPitch(freq=1047, delay=500)
```

Or use music notes:

```python
BPIBIT.playTone(note='C6', delay=500)
```

The module has built-in notes from <b>C3</b> (middle C) to <b>C7</b>. <b>C2 sharp/D2 flat</b> is expressed as <b>'C2D2'</b>, <b>F4 sharp/G4 flat</b> is <b>'F4G4'</b>, and so on.

If the delay time set as <b>0</b> the tone won't stop.

You can stop tones by using

```python
BPIBIT.rest()
```

or turn off the buzzer completely (recommend if you need to access Pin 0/GPIO 25 which is shared by the buzzer):

```python
BPIBIT.noTone()
```

### Read Light Level and Temperature

Read average light level from two LDRs (light dependent resistors):

```python
while True:
    print(BPIBIT.lightLevel())
    BPIBIT.pause(100)
```

Return value 0-1023. You can use <b>BPIBIT.lightLevelL()</b> and <b>BPIBIT.lightLevelR()</b> to get reading from either side.

Read approximate temperature (celsius) from the NTC thermistor:

```python
while True:
    print(BPIBIT.temperature())
    BPIBIT.pause(100)
```

As an analog sensor, the temperature reading would not be very accurate. The [NTC thermistor](https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/NTC-0805-103F-3950F.pdf) has B-value of 3950 and resistence of 10KΩ on 25 celsius. Also according to [BPI:bit v1.2 hardware](https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/BPI-WEBDUINO-BIT-V1_2.pdf) the thermistor has a 4K7Ω resistor in the voltage divider circuit.

Or you can simply use <b>BPIBIT.temperatureRaw()</b> (return 0-1023) to get the original analog value.

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

The parameter for <b>acceleration()</b>, <b>gyroscope()</b> and <b>magneticForce()</b> is <b>'x'</b>, <b>'y'</b> or <b>'z'</b>. If you omit the parameter in acceleration and magneticForce functions you'll get total absolute sum from all 3 axis (the strength of acceleration/magnetic force).

Compass calibration takes 15 seconds, in which you'll have to turn your BPI:bit around at all directions and better away from magnetic fields.

### 5x5 NeoPixel LED Display

```python
BPIBIT.led(index=0, r=255, g=255, b=0)
BPIBIT.ledCode(index=5, code='R')
BPIBIT.ledCodeAll(code='G')
BPIBIT.ledOff()
```

"Color codes" are a set of pre-defined colors:

* 'W' = white
* 'R' = red
* 'Y' = yellow
* 'G' = green
* 'C' = cyan
* 'B' = blue
* 'P' = Purple
* '*' (asterisk) = black (off)

Note: since the NeoPixel LEDs at full power can be very bright and hot (3 LEDs on my board are partially damaged because of this), <b>all led's light levels are greatly reduced under color codes</b>. You'll have to use <b>BPIBIT.led(r, g, b)</b> to set brighter light levels.

You can code the display pattern like

```python
ledArray = ['P', '*', 'B', '*', 'P',
            '*', 'Y', '*', 'Y', '*',
            '*', 'C', '*', 'C', '*',
            '*', 'G', 'B', 'G', '*',
            '*', 'R', '*', 'R', '*']
BPIBIT.ledCodeArray(array=ledArray)
```

### LED Progress Bar Graph

You can also use the display as a dynamic progress bar graph in a specific color:

```python
while True:
    BPIBIT.plotBarGraph(value=BPIBIT.lightLevel(), maxValue=1023, code='W')
    BPIBIT.pause(100)
```

If you omit the parameter "code" the default LED color would be white ('W').

### I2C

For I2C devices, it's as same as micro:bit: SCL to Pin 19 (ESP32's GPIO 22) and SDA to Pin 20 (ESP32's GPIO 21). You can get a I2C object quickly as below:

```python
i2c = BPIBIT.getI2C()
```

### SPI

There are 3 types of SPI: software SPI on any 3 pins, and two hardware SPI channels on specific pins. Hardware SPI can run faster than software ones, however the actual speed you use is depending on the SPI device(s). See [here](http://docs.micropython.org/en/latest/esp32/quickref.html#software-spi-bus) and [here](http://docs.micropython.org/en/latest/library/machine.SPI.html#machine-spi) for more information.

```python
# software SPI
spi = BPIBIT.getSPI(sck=0, miso=1, mosi=2)
spi = BPIBIT.getSPI(sck=0, miso=1, mosi=2, baudrate=100000, polarity=1, phase=0)

# hardware SPI 1: sck=7, miso=6, mosi=3 of micro:bit pins
hspi = BPIBIT.getHSPI()
hspi = BPIBIT.getHSPI(baudrate=10000000, polarity=1, phase=0)

# hardware SPI 2: sck=13, miso=14, mosi=15 of micro:bit pins
vspi = BPIBIT.getHSPI()
vspi = BPIBIT.getHSPI(baudrate=10000000, polarity=1, phase=0)
```

### Garbage Collection (GC)

The module enables auto garbage collection on start.
