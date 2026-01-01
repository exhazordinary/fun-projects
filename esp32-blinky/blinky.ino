/*
 * ESP32 Blinky - LED blink patterns
 *
 * Supports multiple modes:
 * - Basic blink
 * - SOS Morse code
 * - PWM fade in/out
 * - Heartbeat pattern
 *
 * Works with onboard LED (GPIO 2) or ESP32-CAM flash LED (GPIO 4)
 */

#define LED_PIN 2       // Onboard LED on most ESP32 boards
// #define LED_PIN 4    // Uncomment for ESP32-CAM flash LED

#define LEDC_CHANNEL 0
#define LEDC_FREQ 5000
#define LEDC_RESOLUTION 8

// Timing constants (milliseconds)
#define DOT_DURATION 200
#define DASH_DURATION 600
#define SYMBOL_GAP 200
#define LETTER_GAP 600
#define WORD_GAP 1400

enum BlinkMode {
  MODE_BASIC,
  MODE_SOS,
  MODE_FADE,
  MODE_HEARTBEAT
};

BlinkMode currentMode = MODE_BASIC;

void setup() {
  Serial.begin(115200);

  if (currentMode == MODE_FADE) {
    // Setup PWM for fading
    ledcSetup(LEDC_CHANNEL, LEDC_FREQ, LEDC_RESOLUTION);
    ledcAttachPin(LED_PIN, LEDC_CHANNEL);
  } else {
    pinMode(LED_PIN, OUTPUT);
  }

  Serial.println("ESP32 Blinky Started!");
  Serial.println("Modes: BASIC, SOS, FADE, HEARTBEAT");
}

void loop() {
  switch (currentMode) {
    case MODE_BASIC:
      basicBlink();
      break;
    case MODE_SOS:
      sosMorse();
      break;
    case MODE_FADE:
      fadeBlink();
      break;
    case MODE_HEARTBEAT:
      heartbeat();
      break;
  }
}

// Simple on/off blink
void basicBlink() {
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(1000);
}

// Morse code helper functions
void dot() {
  digitalWrite(LED_PIN, HIGH);
  delay(DOT_DURATION);
  digitalWrite(LED_PIN, LOW);
  delay(SYMBOL_GAP);
}

void dash() {
  digitalWrite(LED_PIN, HIGH);
  delay(DASH_DURATION);
  digitalWrite(LED_PIN, LOW);
  delay(SYMBOL_GAP);
}

// SOS: ... --- ...
void sosMorse() {
  // S: ...
  dot(); dot(); dot();
  delay(LETTER_GAP - SYMBOL_GAP);

  // O: ---
  dash(); dash(); dash();
  delay(LETTER_GAP - SYMBOL_GAP);

  // S: ...
  dot(); dot(); dot();
  delay(WORD_GAP);
}

// Smooth PWM fade in and out
void fadeBlink() {
  // Fade in
  for (int duty = 0; duty <= 255; duty++) {
    ledcWrite(LEDC_CHANNEL, duty);
    delay(10);
  }

  // Fade out
  for (int duty = 255; duty >= 0; duty--) {
    ledcWrite(LEDC_CHANNEL, duty);
    delay(10);
  }

  delay(200);
}

// Heartbeat pattern: lub-dub
void heartbeat() {
  // First beat (lub)
  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);
  delay(100);

  // Second beat (dub)
  digitalWrite(LED_PIN, HIGH);
  delay(100);
  digitalWrite(LED_PIN, LOW);

  // Pause between heartbeats
  delay(700);
}
