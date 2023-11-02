 /*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por:
 *  Emmanuel Giron Jimenez
 *  Rodrigo García Padilla
 *Última modificación: 03-noviembre-2023
 
*/

// ENABLE_DEBUG settings
#ifdef ENABLE_DEBUG
   #define DEBUG_ESP_PORT Serial
   #define NODEBUG_WEBSOCKETS
   #define NDEBUG
#endif 

// Wifi for ESP librarie
#include <Arduino.h>
#if defined(ESP8266)
  #include <ESP8266WiFi.h>
#elif defined(ESP32) || defined(ARDUINO_ARCH_RP2040)
  #include <WiFi.h>
#endif

// Sinric libraries
#include "SinricPro.h"
#include "SinricProSwitch.h"
#include "SinricProDimSwitch.h"


// Usernames and keys
#define WIFI_SSID         "Clase_IoT"
#define WIFI_PASS         "0123456789"

#define APP_KEY1           "8e1f718d-538f-4c71-94e4-89320548aea2"
#define APP_SECRET1        "03449b3d-dff2-479c-b535-994a1ee005d6-7e673b79-553a-4364-943b-9f400e6eabb7"

#define SWITCH_ID_1       "653ef606107b9ca18fad541f"
#define SWITCH_ID_2       "653eee09107b9ca18fad511e"
#define SWITCH_ID_3       "653f0cac63039b95af2334cf"

#define RELAYPIN_1        14
#define RELAYPIN_2        27
#define RELAYPIN_3        26

#define BAUD_RATE         115200                // Change baudrate to your need

/*Defines PWM variables*/
const int freq = 1000; //Frecuency on hz
const int ChanelPWM = 0; //Channel between 0-15
const int resolution = 8; //Resolution bits

//Callback functions section-----------------------------------------------------------------
/*
* Power on/off RELAYPIN_1 if device switch state is on/off
* args:
*   const String &deviceId deviceId
*   bool &state actual state of switch
* return:
*   request handled succesfully
*/
bool onPowerState1(const String &deviceId, bool &state) {
 Serial.printf("Device 1 turned %s", state?"on":"off");
 digitalWrite(RELAYPIN_1, state ? HIGH:LOW);
 return true; 
}

/*
* Power on/off RELAYPIN_2 if device switch state is on/off
* args:
*   const String &deviceId deviceId
*   bool &state actual state of switch
* return:
*   request handled succesfully
*/
bool onPowerState2(const String &deviceId, bool &state) {
 Serial.printf("Device 2 turned %s", state?"on":"off");
 digitalWrite(RELAYPIN_2, state ? HIGH:LOW);
 return true; 
}

/*
* Power on/off RELAYPIN_3 if device switch state is on/off 
* args:
*   const String &deviceId deviceId
*   bool &state actual state of switch
* return:
*   request handled succesfully
*/
bool onPowerState3(const String &deviceId, bool &state) {
 Serial.printf("Device 3 turned %s", state?"on":"off");
 ledcWrite(ChanelPWM, state ? 255:0); 
 return true; 
}

/*
* Sets power level of ChanelPWM on dim device power level
*  args:
*   const String &deviceId deviceId
*   bool &powerLevel actual state of dim switch
* return:
*   request handled succesfully
*/
bool onPowerLevel3(const String &deviceId, int &powerLevel) {
  Serial.printf("Device %s powerlevel %d\r\n", deviceId.c_str(), powerLevel);
  ledcWrite(ChanelPWM, ((double)powerLevel*2.55)); 
  return true; 
}


/*
* Sets power level of ChanelPWM on dim device to absolutePowerLevel adding the powerDelta tunning
*  args:
*   const String &deviceId deviceId
*   bool &powerDelta power increment of dim switch
* return:
*   request handled succesfully
*/
int absolutePowerLevel;
 
bool onAdjustPowerLevel3(const String &deviceId, int &powerDelta) {
  absolutePowerLevel += powerDelta;  // calculate absolute power level
  Serial.printf("Device %s brightness changed about %i to %d\r\n", deviceId.c_str(), powerDelta, absolutePowerLevel);
  Serial.print("absolutePowerLevel:");
  Serial.println(absolutePowerLevel);
  ledcWrite(ChanelPWM, ((double)absolutePowerLevel*2.55)); //converts from int in [0-100] to double in [0-255] range
  return true; 
}


/*
* Setup WiFi connection for WIFI_SSID and WIFI_PASS network
* No args
* return:
*   request handled succesfully
*/
void setupWiFi() {
  Serial.printf("\r\n[Wifi]: Connecting");

  #if defined(ESP8266)
    WiFi.setSleepMode(WIFI_NONE_SLEEP); 
    WiFi.setAutoReconnect(true);
  #elif defined(ESP32)
    WiFi.setSleep(false); 
    WiFi.setAutoReconnect(true);
  #endif

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.printf(".");
    delay(250);
  }

  Serial.printf("connected!\r\n[WiFi]: IP-Address is %s\r\n", WiFi.localIP().toString().c_str());
}

/*
* Setup SinricPro connection 
* No args
* No return
*/
void setupSinricPro() {
  //led pinout setup
  pinMode(RELAYPIN_1, OUTPUT);
  pinMode(RELAYPIN_2, OUTPUT);
  setupPWMLed();
  
  //switch devices setup
  SinricProSwitch& mySwitch1 = SinricPro[SWITCH_ID_1];
  SinricProSwitch& mySwitch2 = SinricPro[SWITCH_ID_2];
  mySwitch1.onPowerState(onPowerState1);
  mySwitch2.onPowerState(onPowerState2);
  
  //dim switch setup
  SinricProDimSwitch& mySwitch3 = SinricPro[SWITCH_ID_3];
  mySwitch3.onPowerState(onPowerState3);
  mySwitch3.onPowerLevel(onPowerLevel3);
  mySwitch3.onAdjustPowerLevel(onAdjustPowerLevel3);
  
  // setup SinricPro app keys
  SinricPro.onConnected([](){ Serial.printf("Connected to SinricPro\r\n"); }); 
  SinricPro.onDisconnected([](){ Serial.printf("Disconnected from SinricPro\r\n"); });
   
  SinricPro.begin(APP_KEY1, APP_SECRET1);
}
/*
* Attachs output led RELAYPIN_3 to setted ChanelPWM
* No args
* No return
*/
void setupPWMLed() {
  pinMode(RELAYPIN_3, OUTPUT); //PWM as output
  ledcSetup(ChanelPWM, freq, resolution); //Configuring PWM channel
  ledcAttachPin(RELAYPIN_3, ChanelPWM); //Link channel to PinPWM
}

/*
* Sets:
* Wifi
* SinricPro
* PWMLed
*
* No args
* No return
*/
void setup() {
  Serial.begin(BAUD_RATE); Serial.printf("\r\n\r\n");
  setupWiFi();
  setupSinricPro();
}

/*
* Allows Sinric to listen callback functions permanently
* No args
* No return
*/
void loop() {
  SinricPro.handle();
}
