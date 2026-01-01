# ESP32 Blinky

Make lights go blink. The "hello world" of hardware.

## Requirements

- ESP32 board (or ESP32-CAM)
- USB cable
- Arduino IDE or PlatformIO

## Setup

### Arduino IDE

1. Install ESP32 board package:
   - File > Preferences > Additional Board URLs:
   - Add: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
2. Tools > Board > ESP32 Dev Module
3. Select correct port
4. Upload!

### PlatformIO

```bash
pip install platformio
pio project init --board esp32dev
# Copy blinky.ino to src/main.cpp
pio run --target upload
```

## Blink Modes

Change `currentMode` in the code:

| Mode | Description |
|------|-------------|
| `MODE_BASIC` | Simple 1-second on/off blink |
| `MODE_SOS` | Morse code SOS (... --- ...) |
| `MODE_FADE` | Smooth PWM fade in/out |
| `MODE_HEARTBEAT` | Lub-dub heartbeat pattern |

## Pin Configuration

```cpp
#define LED_PIN 2    // Onboard LED (most ESP32 boards)
#define LED_PIN 4    // ESP32-CAM flash LED
```

## Wiring (External LED)

```
ESP32 GPIO --> 220Ω resistor --> LED (+) --> LED (-) --> GND
```
