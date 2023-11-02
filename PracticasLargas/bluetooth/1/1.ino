/*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por:
 *  Emmanuel Giron Jimenez
 *  Rodrigo García Padilla
 *Última modificación: 2-noviembre-2023
 
*/

//Include bluettoth library
#include "BluetoothSerial.h"

//Include dht sensor library
#include <DHT.h>

const int leds[5] = {14, 27, 26, 25, 33}; //Leds pins number array
int leds_array_length = sizeof(leds)/sizeof(leds[0]); //Calculates the length of leds array

/*
* Buttons pins for activating sending humidity and temperature
*/
#define PinButton_PullUp 4
#define PinButton_PullDown 15

/*
* Variables for controlling button trebble
*/
int count = 0;
long timeCounter = 0;
const int timeThreshold = 150;


//Sensor configuration
#define DHTPIN 32
//Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11
//#define DHTTYPE    DHT22     // DHT 22 (AM2302)
//#define DHTTYPE    DHT21     // DHT 21 (AM2301)
DHT dht(DHTPIN, DHTTYPE);

/*
* Variables used for buffering the temperature and humidity
*/
float temp = 0;
float hum = 0;

//Condition for activating bluetooth
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial BT; //Bluetooth Object


/*Set:
    device as bt in slave mode
    pins of leds array as output pins
    pin PinButton_PullUp as input button
    pin PinButton_PullDown as input button
*/
void setup() {
  Serial.begin(115200); //Initialize serial communication
  BT.begin("ESP32_Vazzvel_Slave"); //Name of device in slave mode
  Serial.println("El dispositivo Bluetooth está listo para emparejarse");
  for (int i = 0; i < leds_array_length ; i++) {//Sets all pins in leds array as output pins
    pinMode(leds[i], OUTPUT);
  }

  pinMode(PinButton_PullUp, INPUT);//Sets the Pull Up switch as input button
  pinMode(PinButton_PullDown, INPUT);//Sets the Pull Up switch as input button
  dht.begin();
}

/*
* By bt receiving: prints the bt received bytes and turns on leds of leds pins array if they means a number on led pin array
* By bt sending: sends the temperature and humidity of dht sensor when pressing temp_button and hum_button
*
* No args
* No return
*/
void loop() {
  
  //Receiving part*************************
  if (BT.available()) // Mientras haya datos por recibir vía bluetooth
  {
    int val = BT.read(); // Lee un byte de los datos recibidos
    Serial.print("Recibido: ");
    Serial.println(val);
   
    if(48 <= val && val <=53){
      turn_on(val-48);
    }
  }
  
  //Emiting part****************
  hum = dht.readHumidity();
  temp = dht.readTemperature();
  
  if (isnan(hum) || isnan(temp)) {//Detect error on sensor values update
    Serial.println("Failed to read from DHT sensor!");
  }else{//Send the humidity and temperature values
  
    int temp_button_PullUp_value = digitalRead(PinButton_PullUp);
    int hum_button_PullDown_value = digitalRead(PinButton_PullDown);

    //Send the humidity if button were pressend after threshold after last button pushing
    if (hum_button_PullDown_value == HIGH) {
      if (millis() > timeCounter + timeThreshold) {
        Serial.print("Humedad:");
        Serial.println(hum);
        BT.print("Humedad:");
        BT.print(int(hum));
        BT.print('.');
        BT.print(int((hum-(int(hum)))*100));
        BT.println('%');
      }
    }
    //Send the temperature if button were pressend after threshold after last button pushing
    if (temp_button_PullUp_value == LOW) {
      if (millis() > timeCounter + timeThreshold) {
        Serial.print("Temperatura:");
        Serial.println(temp);
        BT.print("Temperatura:");
        BT.print(int(temp));
        BT.print('.');
        BT.print(int((temp-(int(temp)))*100));
        BT.println('o');
      }
    }
  }

  delay(1000);

}

/*
 * Turn on led n'th in leds pins number array

  led in'th led to turn on
  No return 
 */
void turn_on(int led){
    // Input correctness check
    if(led> leds_array_length){
        return;
    }
    
    if(led == 0){//Turns off all the leds
      for(int i = 0; i < leds_array_length; i++){
        digitalWrite(leds[i], LOW);
      }
    }else{
      digitalWrite(leds[led-1], HIGH); //Turns on lednth led 
    }
}