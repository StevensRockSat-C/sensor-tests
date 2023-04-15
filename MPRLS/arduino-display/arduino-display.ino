/**
 * Display the pressures of the MPRLS' onto the screen for calibration
 */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include "SSD1306.h"
#include <Adafruit_INA219.h>
#include <Adafruit_MPRLS.h>

#define TCAADDR 0x70

SSD1306 display;

Adafruit_MPRLS mpr1 = Adafruit_MPRLS();
Adafruit_MPRLS mpr2 = Adafruit_MPRLS();
Adafruit_MPRLS mpr3 = Adafruit_MPRLS();
Adafruit_MPRLS mpr4 = Adafruit_MPRLS();
Adafruit_MPRLS mpr5 = Adafruit_MPRLS();

int countTry = 0;

//The ESP8266 recognizes different pins than what is labelled on the WeMos D1 
#if defined(d1)  //Defines Wemos D1 R1 pins to GPIO pins
  #define D0 3
  #define D1 1
  #define D2 16
  #define D3 5
  #define D4 4
  #define D8 0
  #define D9 2
  #define D5 14
  #define D6 12
  #define D7 13
  #define D10 15 
  #define D11 13 // SAME AS D5-D7, https://forum.arduino.cc/t/wemos-d1-pins/523831/17
  #define D12 12
  #define D13 14
#endif 

void tcaselect(uint8_t i) {
  if (i > 7) return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void setup() {

  Wire.begin();
  
  tcaselect(5);
  // Initialize the display and display some text
  display.value(0x3C, D4, D3);  // SDA SCL
  display.init(); // !!Causes some sort of buffer/memory error
  display.flipScreenVertically(); // Needed when pin-outs are on top.
  //display.mirrorScreen();
  display.drawString(0, 0, "Mashallah!"); // Runs once since in setup
  display.setFont(ArialMT_Plain_10); // ArialMT_Plain_10, ArialMT_Plain_16, ArialMT_Plain_24
  display.display();

  drawToScreen("Trying MPRLS 1");
  tcaselect(0);
  // Connect to the MPRLS
  while (!mpr1.begin()) {
    countTry++;
    drawToScreen("Failed find MPRLS 1\n" + String(countTry));
    delay(200);
    tcaselect(0);
  }

  drawToScreen("Trying MPRLS 2");

  tcaselect(1);
  // Connect to the MPRLS
  while (!mpr2.begin()) {
    countTry++;
    drawToScreen("Failed find MPRLS 2\n" + String(countTry));
    delay(200);
    tcaselect(1);
  }

  tcaselect(2);
  // Connect to the MPRLS
  while (!mpr3.begin()) {
    countTry++;
    drawToScreen("Failed find MPRLS 3\n" + String(countTry));
    delay(200);
    tcaselect(2);
  }

  tcaselect(3);
  // Connect to the MPRLS
  while (!mpr4.begin()) {
    countTry++;
    drawToScreen("Failed find MPRLS 4\n" + String(countTry));
    delay(200);
    tcaselect(3);
  }

  tcaselect(4);
  // Connect to the MPRLS
  while (!mpr5.begin()) {
    countTry++;
    drawToScreen("Failed find MPRLS 5\n" + String(countTry));
    delay(200);
    tcaselect(4);
  }

  drawToScreen("Ready");
  
}

void loop() {
  // Read from the MPRLS for the pressure sensor's values
  tcaselect(0);
  float pressure_hPa_1 = mpr1.readPressure();
  tcaselect(1);
  float pressure_hPa_2 = mpr2.readPressure();
  tcaselect(2);
  float pressure_hPa_3 = mpr3.readPressure();
  tcaselect(3);
  float pressure_hPa_4 = mpr4.readPressure();
  tcaselect(4);
  float pressure_hPa_5 = mpr5.readPressure();

  // Draw the values to the screen
  drawToScreen("1: " + String(pressure_hPa_1) + "  2: " + String(pressure_hPa_2) + "\n" + 
               "3: " + String(pressure_hPa_3) + "  4: " + String(pressure_hPa_4) + "\n" + 
               "5: " + String(pressure_hPa_5));

  // Read twice a second
  delay(500);
}

// Draw to the SSD1306
void drawToScreen(String words) {
  tcaselect(5);
  display.clear();
  display.drawString(0, 0, words);
  display.display();
}
