# micropython-BPIBIT: A MicroPython ESP32 Module for BPI:bit/Web:bit

![153543457141539355s6op3](https://user-images.githubusercontent.com/44191076/62682966-f88fb280-b9ef-11e9-83e4-47976fa68350.jpg)
![800x423xBPI_bit_interfact JPG pagespeed ic NngFYTGX_e](https://user-images.githubusercontent.com/44191076/62682983-047b7480-b9f0-11e9-8b0e-e7c8cc24b677.jpg)

This is a MicroPython module designed for the BPI:bit/Web:bit, using [BBC micro:bit pin numbers](https://microbit.org/guide/hardware/pins/) and provide various easy-to-use functions.

> This module only works for MicroPython firmware v1.17 for ESP32. Since v1.18 the PWM frequency range has changed so the note playing would be mostly useless.


## Install Module

Upload these onto your board:

* BPIBIT.py
* mpu9250.py
* mpu6500.py
* ak8963.py

The library for the onboard MPU-9250 is from this repo: [MicroPython MPU-9250 (MPU-6500 + AK8963) I2C driver](https://github.com/tuupola/micropython-mpu9250). Without this driver the BPIBIT module still works, but all the accelerometer/gyroscope/compass functions would not work and only return None.

### Blinky LED

Blink the tiny red LED behind the board:

```python
import BPIBIT

while True:
    BPIBIT.digitalWritePin('BUILTIN_LED', 1)
    BPIBIT.pause(500)
    BPIBIT.digitalWritePin('BUILTIN_LED', 0)
    BPIBIT.pause(500)  # or BPIBIT.pauseMicros(500000)
```

### System Running Time

```python
import BPIBIT

while True:
    print(BPIBIT.runningTime())
    # print(BPIBIT.runningTimeMicros())
    BPIBIT.pause(100)
```

### Read/Write GPIOs

```python
result = BPIBIT.digitalReadPin(pin=2)  # read digital signal of pin 2
result = BPIBIT.analogReadPin(pin=2)  # read analog signal of pin 2
BPIBIT.digitalWritePin(pin=2, value=1)  # write digital signal to pin 2
BPIBIT.analogWritePin(pin=2, value=1023)  # write analog signal (PWM) to pin 2
```

All ESP32 pins in this module are remapped to [micro:bit pin numbers](https://microbit.org/guide/hardware/pins/). For example, pin 2 is actually pin 33 on ESP32. It's easier to use micro:bit accessories this way.

All digital pins can be used to write analog signals; on the other hand, only pin 1 and 2 can be used to read analog signals (0-1023).

### Servo Control

```python
import BPIBIT

while True:
    BPIBIT.servoWritePin(pin=2, degree=0)
    BPIBIT.pause(1000)
    BPIBIT.servoWritePin(pin=2, degree=180)
    BPIBIT.pause(1000)
```

### Buttons/Touchpads

```python
import BPIBIT

while True:
    print(BPIBIT.onButtonPressed(button='A'))  # if button A is being pressed
    BPIBIT.pause(100)
```

Parameter "button" can be <b>'A'</b>, <b>'B'</b> or <b>'AB'</b> (both).

ESP32 also supports capacitive touch; on BPI:bit pin 1, 2, 3, 6, 7, 11 are available. However, without external touchpads only Pin 1 and 2 are large enough to be touched by finger, and Pin 0 (GPIO 25) does not support capacitive touch.

```python
import BPIBIT

while True:
    print(BPIBIT.pinIsTouched(pin=2))  # set pin 2 as touchpad and return pressing status
    BPIBIT.pause(100)
```

### Buzzer and Tone

```python
BPIBIT.analogPitch(freq=1047, delay=0)  # set buzzer to play 1047 Hz, no stop
BPIBIT.playTone(note='C6', delay=500)  # set buzzer to play note C6 (1047 Hz) for 500 ms
BPIBIT.rest(500)  # rest 500 ms
BPIBIT.noTone()  # turn off buzzer
```

The module has a built-in note library ranged from C3 to C7. C3 sharp/D3 flap is written as 'C3D3', and so on. If you input a wrong note, no sound will be played for it.

Below is a short music example:

```python
import BPIBIT

tempo = 400

BPIBIT.playTone('D4', tempo)
BPIBIT.playTone('G4', tempo * 2)
BPIBIT.playTone('A4B4', tempo)
BPIBIT.playTone('D5', tempo * 2)
BPIBIT.playTone('G5', tempo)
BPIBIT.playTone('A5B5', tempo * 1.5)
BPIBIT.playTone('A5', tempo * 0.5)
BPIBIT.playTone('G5', tempo)
BPIBIT.playTone('A5', tempo * 2)
BPIBIT.playTone('D5', tempo)
BPIBIT.playTone('D5', tempo * 1.5)
BPIBIT.playTone('C5', tempo * 0.5)
BPIBIT.playTone('E5', tempo)
BPIBIT.playTone('D5', tempo * 1.5)
BPIBIT.playTone('C5', tempo * 0.5)
BPIBIT.playTone('E5', tempo)
BPIBIT.playTone('D5', tempo * 4)
BPIBIT.rest(tempo)
BPIBIT.playTone('D4', tempo)
BPIBIT.playTone('G4', tempo * 2)
BPIBIT.playTone('A4B4', tempo)
BPIBIT.playTone('D5', tempo * 2)
BPIBIT.playTone('F5', tempo)
BPIBIT.playTone('G5A5', tempo * 1.5)
BPIBIT.playTone('G5', tempo * 0.5)
BPIBIT.playTone('F5', tempo)
BPIBIT.playTone('G5', tempo * 2)
BPIBIT.playTone('G4', tempo)
BPIBIT.playTone('G4', tempo * 1.5)
BPIBIT.playTone('F4G4', tempo * 0.5)
BPIBIT.playTone('A4', tempo)
BPIBIT.playTone('G4', tempo * 1.5)
BPIBIT.playTone('F4G4', tempo * 0.5)
BPIBIT.playTone('A4B4', tempo)
BPIBIT.playTone('G4', tempo * 4)
BPIBIT.noTone()
```

### Read Light Level

```python
import BPIBIT

while True:
    print(BPIBIT.lightLevel())  # returns 0-1023
    BPIBIT.pause(100)
```

BPIBIT.lightLevel() returns the average value of the two LDRs. You can read either by using <b>BPIBIT.lightLevelL()</b> or <b>BPIBIT.lightLevelR()</b>.

### Read Temperature

```python
import BPIBIT

while True:
    c = BPIBIT.temperature()  # read temperature in Celsius
    f = c * 9 / 5 + 32  # convert to Fahrenheit
    print('c =', c, '/ f =', f)
    BPIBIT.pause(100)
```

The temperature sensor is analog so the reading may not be very accurate and would be affected by the board itself.

<b>BPIBIT.temperatureRaw()</b> would return the analog value of the thermistor (0-1023).

### Acceleration, Gyroscope and Compass

```python
import BPIBIT

while True:
    pitch = BPIBIT.rotationPitch()
    roll = BPIBIT.rotationRoll()
    heading = BPIBIT.compassHeading()
    print('Pitch =', pitch, '/ roll =', roll, '/ heading = ', heading)
    BPIBIT.pause(100)
```

These function would only return None if the MPU-9250 cannot be initialized.

```python
value = BPIBIT.acceleration('x')  # get acceleration on x axis
value = BPIBIT.rotationPitch()  # get pitch angles
value = BPIBIT.rotationRoll()  # get roll angles
value = BPIBIT.gyroscope('y')  # get angular velocity on x axis
value = BPIBIT.magneticForce('z')  # get magnetic force on x axis
value = BPIBIT.compassHeading()  # get compass heading
BPIBIT.calibrateCompass()  # calibrate compass
```

The axis parameter can be <b>'x'</b>, <b>'y'</b>, <b>'z'</b> or <b>''</b> (absolute value of all axis combined).

Compass calibration takes 15 seconds. Turn your BPI:bit around at all directions and away from other magnetic fields ifpossible.

### 5x5 NeoPixel LED Display

```python
BPIBIT.led(0, (64, 64, 0))  # set LED 0 to (64, 64, 0)
BPIBIT.ledAll((0, 32, 32))  # set all LEDs to (0, 32, 32)
BPIBIT.ledCode(5, code='R')  # set LED 5 to red
BPIBIT.ledCodeAll(code='G')  # set all LEDs to green
BPIBIT.ledOff()  #Turn off all LEDs
```

The LED indexes are 0 (right-bottom corner) to 24 (left-top corner). Parameter <b>'code'</b> are pre-defined color codes:

* 'W' = white
* 'R' = red
* 'O' = orange
* 'Y' = yellow
* 'G' = green
* 'T' = turquoise
* 'C' = cyan
* 'B' = blue
* 'V' = violet
* 'P' = Purple
* '*' (asterisk) = black (off)

When using color codes, the brightness are reduced to protect the NeoPixels (so they won't be easily damaged). If you really want to light them up, use <b>BPIBIT.led()</b> and <b>BPIBIT.ledAll()</b> to set the raw value (each color 0~255).

### Display LED Pattern 

```python
import BPIBIT

ledArray = ['B', 'B', 'B', 'R', 'R',
            'B', 'W', 'B', 'R', 'R',
            'B', 'B', 'B', 'R', 'R',
            'R', 'R', 'R', 'R', 'R',
            'R', 'R', 'R', 'R', 'R']
            
BPIBIT.ledCodeArray(array=ledArray)
```

### LED Progress Bar Graph

```python
import BPIBIT

while True:
    v = BPIBIT.lightLevel()
    BPIBIT.plotBarGraph(value=v, maxValue=1023, code='Y')
    BPIBIT.pause(100)
```

### Scroll Text

```python
import BPIBIT

colors = ['W', 'R', 'O', 'Y', 'G', 'T', 'C', 'B', 'V', 'P']

while True:
    for c in colors:
        BPIBIT.scrollText('Hello BPI:bit', delay=100, code=c)  # will wait until scrolling is over
        BPIBIT.pause(500)
```

### I2C

```python
# get software I2C
i2c = BPIBIT.getI2C(scl=19, sda=20)
```

### SPI

```python
# get software SPI
spi = BPIBIT.getSPI(sck=13, miso=14, mosi=15, baudrate=100000, polarity=1, phase=0)

# hardware SPI 1: sck=7, miso=6, mosi=3
hspi = BPIBIT.getHSPI(baudrate=10000000, polarity=1, phase=0)

# hardware SPI 2: sck=13, miso=14, mosi=15
vspi = BPIBIT.getHSPI(baudrate=10000000, polarity=1, phase=0)
```

### Garbage Collection

The module enables auto memory garbage collection on import.
