# micropython-BPIBIT: A MicroPython ESP32 Module for BPI:bit/Web:bit (給 BPI:bit/Web:bit 使用的 MicroPython ESP32 模組)

![153543457141539355s6op3](https://user-images.githubusercontent.com/44191076/62682966-f88fb280-b9ef-11e9-83e4-47976fa68350.jpg)
![800x423xBPI_bit_interfact JPG pagespeed ic NngFYTGX_e](https://user-images.githubusercontent.com/44191076/62682983-047b7480-b9f0-11e9-8b0e-e7c8cc24b677.jpg)

This is a MicroPython module for [BPI:bit](http://wiki.banana-pi.org/BPI-Bit), which is a [BBC micro:bit](https://tech.microbit.org/hardware/)-like ESP32 board compatible with most micro:bit accessories.

這是針對 BPI:bit 而寫的 MicroPython 模組；BPI:bit 是個仿 BBC micro:bit 形式的 ESP32 開發板, 與大部分的 micro:bit 擴充板相容。

This is also a free personal project with no sponsorship whatsoever. It's not meant to be a commercial product either.

這也是由本人無償開發的專案，沒拿過廠商任何贊助，也不是要當成商業產品。

This module has been tested on <b>BPI:bit v1.4</b> and <b>MicroPython ESP32 firmware v1.11</b>.

此模組的測試平台為 BPI:bit v1.4 版，MicroPython ESP32 韌體版本 v1.11。

## Install Module (安裝模組)

You need to flash your BPI:bit with MicroPython ESP32 firmware and upload the following files onto your board:

你得替你的 BPI:bit 燒錄 MicroPython ESP32 韌體，並上傳下列檔案到板子上：

* BPIBIT.py or (或) BPIBIT_LITE.py
* mpu9250.py
* mpu6500.py
* ak8963.py

The library for the onboard MPU-9250 3-axis accelerometer/3-axis gyroscope/3-axis compass is from this Github repo:

板子上的 MPU-9250 三軸加速計/陀螺儀/羅盤所使用的函式庫來自以下 Github repo:

[MicroPython MPU-9250 (MPU-6500 + AK8963) I2C driver](https://github.com/tuupola/micropython-mpu9250)

### Import Module (匯入模組)

```python
import BPIBIT
```

or (或)

```python
import BPIBIT_LITE as BPIBIT
```

BPIBIT_LITE is basically BPIBIT minus text scrolling functions and font library, which takes less memory.

BPIBIT_LITE 基本上就是 BPIBIT 拿掉文字捲動功能與內建字元庫的版本，占的記憶體較少。

### Pause (停頓)

```python
BPIBIT.pause(500) # pause 500 ms (停頓 500 毫秒)
BPIBIT.pauseMicros(500) # pause 500 ms (停頓 500 微秒)
```

### System Running Time (系統開機時間)

```python
timeNow = BPIBIT.runningTime() # system time in ms (系統開機後時間-毫秒)
timeNow = BPIBIT.runningTimeMicros() # system time in us (系統開機後時間-微秒)
```

### Read/Write GPIOs (讀寫腳位)

```python
result = BPIBIT.digitalReadPin(pin=2) # read digital signal of pin 2 (讀取 Pin 2 數位信號)
result = BPIBIT.analogReadPin(pin=2) # read analog signal of pin 2 (讀取 Pin 2 類比信號)
BPIBIT.digitalWritePin(pin=2, value=1) # write digital signal to pin 2 (對 Pin 2 寫入數位信號)
BPIBIT.analogWritePin(pin=2, value=1023) # write analog signal (PWM) to pin 2 (對 Pin 2 寫入類比信號, 或 PWM)
```

All ESP32 pin numbers in this module are remapped to [micro:bit pins](https://microbit.org/guide/hardware/pins/). For example, pin 2 is actually pin 33 on ESP32. It's easier to use micro:bit accessories this way.

在本 module 中，ESP32 的腳位號碼是以 micro:bit 的腳位號碼來對應的。例如，Pin 2 其實是 ESP32 的 Pin 33。這樣一來，使用 micro:bit 擴充板就會比較容易。

All digital pins can be used to write analog signals. 

所有數位腳位都能用來輸出類比訊號。

Avaliable pins to read analog signals are pin 0-7, 10-12. However when the board turns on WiFi, only pin 1, 2 and 5 can be used to read analog signals. Pin 5/11 are connected to A/B buttons. See [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/) for more details.

可用來讀取類比信號的腳位為 Pin 0-7 及 10-12。但板子打開 WiFi 時, 只有 Pin 1、2、5 可以用於讀取類比信號。Pin 5/11 已經接在 A/B 鈕。更多資訊請參見上面的連結 ESP32 Pinout Reference。

### Servo Control (伺服馬達控制)

```python
while True:
    BPIBIT.servoWritePin(pin=2, degree=0) # turn servo on pin 2 to 0 degrees (把 Pin 2 的伺服馬達轉到 0 度)
    BPIBIT.pause(1000)
    BPIBIT.servoWritePin(pin=2, degree=180) # turn servo on pin 2 to 0 degrees (把 Pin 2 的伺服馬達轉到 180 度)
    BPIBIT.pause(1000)
```

### Buttons/Touchpads (按鈕/電容按鈕)

To tell if button A, B or both is/are being pressed:

```python
while True:
    print(BPIBIT.onButtonPressed(button='A')) # pressing status of button A (A 鈕按下狀態)
    BPIBIT.pause(100)
```

BPIBIT.onButtonPressed() return True/False. Parameter "button" can be <b>'A'</b>, <b>'B'</b> or <b>'AB'</b> (both).

BPIBIT.onButtonPressed() 會回傳 True/False。參數「button」可設為 <b>'A'</b>，<b>'B'</b> 或 <b>'AB'</b> (同時按)。

ESP32 also supports capacitive touch; on BPI:bit pin 1, 2, 3, 6, 7, 11 are available. However, without external touchpads only Pin 1 and 2 are large enough to be touched by finger, and Pin 0 (GPIO 25) does not support capacitive touch.

ESP32 也支援電容觸碰按鈕；在 BPI:bit 上可用腳位為 Pin 1, 2, 3, 6, 7, 11。不過，若不使用外部觸控板，只有腳位 1 和 2 大到能用手指觸摸。腳位 0 (GPIO 25) 不支援電容觸碰按鈕功能。

```python
print(BPIBIT.pinIsTouched(pin=2)) # set pin 2 as touchpad and return pressing status (設 Pin 2 為觸碰按鈕並傳回按下狀態)
```

### Buzzer and Tone (蜂鳴器和音樂)

```python
BPIBIT.analogPitch(freq=1047, delay=0) # set buzzer to play 1047 Hz, no stop (讓蜂鳴器播放頻率 1047 Hz, 持續播放)
BPIBIT.playTone(note='C6', delay=500) # set buzzer to play note C6 (1047 Hz) for 500 ms (讓蜂鳴器播放音符 C6, 即 1047 Hz, 持續 500 毫秒)
BPIBIT.rest(500) # rest 500 ms (休止 500 毫秒)
BPIBIT.noTone() # turn off buzzer (關閉蜂鳴器)
```

The module has a built-in note library ranged from C3 to C7. C3 sharp/D3 flap is 'C3D3', and so on.

此 module 內建有音符頻率表，範圍從 C3 音到 C7 音。升 C3 或降 D3 音的表示法為 C3D3，以此類推。

### Read Light Level (讀取亮度)

```python
while True:
    print(BPIBIT.lightLevel()) # read LDR light level (從光敏電阻讀取亮度值)
    BPIBIT.pause(100)
```

BPIBIT.lightLevel() returns 0-1023, which is average value of the two LDRs. You can read value from either side by using <b>BPIBIT.lightLevelL()</b> or <b>BPIBIT.lightLevelR()</b>.

BPIBIT.lightLevel() 會回傳值 0-1023，為左右光敏電阻的平均值。你可以用 <b>BPIBIT.lightLevelL()</b> 或 <b>BPIBIT.lightLevelR()</b> 來取得左右光敏電阻的感光值。

### Read Temperature (讀取溫度)

```python
print(BPIBIT.temperature() # read temperature value in celsius (讀取溫度值, 攝氏)
```

The onboard [NTC thermistor](https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/NTC-0805-103F-3950F.pdf) has B-value of 3950 and resistence of 10KΩ at 25 celsius. Also according to [BPI:bit v1.4 hardware](https://github.com/BPI-STEAM/BPI-BIT-Hardware/blob/master/docs/BPI-WEBDUINO-BIT-V1_4.pdf) the thermistor has a 5.1KΩ resistor in the voltage divider circuit.

板子上的熱敏電阻 B 值為 3950，而根據 v1.4 版硬體規格圖，此電阻的分壓電路搭配的是 5.1KΩ 電阻。 

As an analog sensor, the temperature reading may not be very accurate.The reading also may be lower than expected before the board warm up.

既然這是類比感測器，讀數可能不會那麼精確。在板子本身溫度升高之前，讀數也有可能比預期的低。

<b>BPIBIT.temperatureRaw()</b> would return the analog value of the thermistor (0-1023).

<b>BPIBIT.temperatureRaw()</b> 則會回傳熱敏電阻的原始類比值 (0-1023)。

### Acceleration, Gyroscope and Compass (加速計、陀螺儀與羅盤)

```python
value = BPIBIT.acceleration('x') # get acceleration on x axis (取得 X 軸加速度)
value = BPIBIT.rotationPitch() # get pitch angles (取得俯仰角)
value = BPIBIT.rotationRoll() # get roll angles (取得左右轉動角)
value = BPIBIT.gyroscope('y') # get angular velocity on x axis (取得 X 軸角速度)
value = BPIBIT.magneticForce('z') # get magnetic force on x axis (取得 X 軸磁場強度)
value = BPIBIT.compassHeading() # get compass heading (取得羅盤方位)
BPIBIT.calibrateCompass() # calibrate compass (校準羅盤)
```

The axis parameter can be <b>'x'</b>, <b>'y'</b>, <b>'z'</b> or <b>''</b> (absolute value of all axis combined).

軸參數可以是 <b>'x'</b>、<b>'y'</b>、<b>'z'</b> 或 <b>''</b> (三軸絕對值合併).

Compass calibration takes 15 seconds. Turn your BPI:bit around at all directions and away from other magnetic fields ifpossible.

羅盤校準需 15 秒。在這段期間把 BPI:bit 往各方向轉動，並盡量避開外部磁場。

### 5x5 NeoPixel LED Display

```python
BPIBIT.led(0, (64, 64, 0)) # set LED 0 to (64, 64, 0) (設 0 號 LED 為黃色)
BPIBIT.ledAll((0, 32, 32)) # set all LEDs to (0, 32, 32) (設所有 LED 為青色)
BPIBIT.ledCode(5, code='R') # set LED 5 to red (設 0 號 LED 為紅色)
BPIBIT.ledCodeAll(code='G') # set all LEDs to green (設所有 LED 為綠色)
BPIBIT.ledOff() #Turn off all LEDs (關閉所有 LED)
```

The LED indexes are 0 (right-bottom corner) to 24 (left-top corner).

LED 編號為 0 (右下角) 至 24 (左上角)。

Parameter <b>'code'</b> are pre-defined color codes:

參數 <b>'code'</b> 是一系列已定義好的顏色代碼:

* 'W' = white (白)
* 'R' = red (紅)
* 'O' = orange (橘)
* 'Y' = yellow (黃)
* 'G' = green (綠)
* 'T' = turquoise (藍綠)
* 'C' = cyan (青)
* 'B' = blue (藍)
* 'V' = violet (藍紫)
* 'P' = Purple (紫)
* '*' (asterisk) = black (off) (黑, 不亮)

Since NeoPixel LEDs in full power can be very bright and hot - and potentially get damaged - the color codes are set with lowered brightness. If you really wish to light them up, use <b>BPIBIT.led()</b> and <b>BPIBIT.ledAll()</b>.

由於 NeoPixel LEDs 全開時會很亮和很燙，並有可能因此燒壞，故顏色代碼設在較低的亮度。如果真的想要讓 LED 更亮，使用 <b>BPIBIT.led()</b> 和 <b>BPIBIT.ledAll()</b>。

### Display LED Pattern (顯示 LED 圖案)

```python
ledArray = ['B', 'B', 'B', 'R', 'R',
            'B', 'W', 'B', 'R', 'R',
            'B', 'B', 'B', 'R', 'R',
            'R', 'R', 'R', 'R', 'R',
            'R', 'R', 'R', 'R', 'R']
BPIBIT.ledCodeArray(array=ledArray)
```

### LED Progress Bar Graph (LED 燈條圖)

The bar graph can be used to show a value (parameter 'value')'s relative level compared to its max value (parameter 'maxValue'):

燈條圖可用來顯示一個值（參數'value'）相對於最大值（參數'maxValue'）的程度:

```python
while True:
    BPIBIT.plotBarGraph(value=BPIBIT.lightLevel(), maxValue=1023, code='Y')
    BPIBIT.pause(100)
```

### Scroll Text (捲動文字)

The module has a built-in ASCII fonts library (not included in BPIBIT_LITE). You can scroll a text across the LED display by the specific color code and scroll speed.

此模組內建有 ASCII 字元庫 (BPIBIT_LITE 未包括這項功能)。你能讓一段文字在 LED 螢幕上捲動，並指定顏色代碼及捲動速度。

```python
BPIBIT.scrollText("Hello World, BPI:bit!", delay=150, code='G')
```

### I2C

```python
# software I2C (軟體 I2C)
i2c = BPIBIT.getI2C(scl=19, sda=20)
```

### SPI

```python
# software SPI (軟體 SPI)
spi = BPIBIT.getSPI(sck=13, miso=14, mosi=15, baudrate=100000, polarity=1, phase=0)

# hardware SPI 1 (not avalible in BPIBIT_LITE): sck=7, miso=6, mosi=3 (硬體 SPI 1, BPIBIT_LITE 沒有這項功能)
hspi = BPIBIT.getHSPI(baudrate=10000000, polarity=1, phase=0)

# hardware SPI 2 (not avalible in BPIBIT_LITE): sck=13, miso=14, mosi=15 (硬體 SPI 2, BPIBIT_LITE 沒有這項功能)
vspi = BPIBIT.getHSPI(baudrate=10000000, polarity=1, phase=0)
```

### Garbage Collection (GC)

The module enables auto memory garbage collection on import.

此模組在匯入後會啟用自動 GC (garbage collection) 記憶體垃圾回收。
