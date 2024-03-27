/**
 * Measures the current from the Ashcroft G2 while it's isolated in the vacuum tank
 */

#include "SSD1306.h"
#include <Adafruit_INA219.h>

SSD1306 display;
Adafruit_INA219 currentSensor;

float shuntvoltage = 0;
float busvoltage = 0;
float current_mA = 0;
float loadvoltage = 0;
float power_mW = 0;

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

void setup() {
  // Initialize the display and display some text
  display.value(0x3C, D4, D3);  // SDA SCL
  display.init(); // !!Causes some sort of buffer/memory error
  display.flipScreenVertically(); // Needed when pin-outs are on top.
  //display.mirrorScreen();
  display.drawString(0, 0, "Mashallah!"); // Runs once since in setup
  display.setFont(ArialMT_Plain_10); // ArialMT_Plain_10, ArialMT_Plain_16, ArialMT_Plain_24
  display.display();

  // Connect to the INA219
  while (!currentSensor.begin()) {
    countTry++;
    drawToScreen("Failed find INA219\n" + String(countTry));
    delay(200);
  }

  Serial.begin(115200);
  delay(10000);

  Serial.println("time (mS),shunt (mV),bus (V),current (mA),power (mW),load (V),");
  // We want the highest precision reading
  //currentSensor.setCalibration_16V_400mA();
}

void loop() {
  // Read from the INA219 for the pressure sensor's values
  shuntvoltage = currentSensor.getShuntVoltage_mV();
  busvoltage = currentSensor.getBusVoltage_V();
  current_mA = currentSensor.getCurrent_mA();
  power_mW = currentSensor.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);

  // Draw the values to the screen
  drawToScreen("sh:" + String(shuntvoltage) + "mV bus:" + String(busvoltage) + "V\ncur:" + String(current_mA) + "mA\npow:" + String(power_mW) + "mW\nload:" + String(loadvoltage) + "V");
  Serial.println(String(millis()) + "," + String(shuntvoltage) + "," + String(busvoltage) + "," + String(current_mA) + "," + String(power_mW) + "," + String(loadvoltage) + ",");

  // Read 5 times a second
  delay(200);
}

// Draw to the SSD1306
void drawToScreen(String words) {
  display.clear();
  display.drawString(0, 0, words);
  display.display();
}
