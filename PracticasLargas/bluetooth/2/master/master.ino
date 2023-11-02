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

//Client variable (slave device for connecting)
String clientName = "ESP32_Vazzvel_Slave"; 
bool connected;

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

/*Set:
    device as bt in master mode
    pin PinButton_PullUp as input button
    pin PinButton_PullDown as input button
    bt connection with clientName
*/
void setup() {
  Serial.begin(115200); //Initialize serial communication
  BT.begin("ESP32_Vazzvel_Master", true); //Name of device in master mode
  Serial.println("El dispositivo Bluetooth está en modo maestro.\n Conectando con el anfitrión ...");

  pinMode(PinButton_PullUp, INPUT);//Sets the Pull Up switch as input button
  pinMode(PinButton_PullDown, INPUT);//Sets the Pull Up switch as input button
  dht.begin();

  connected = BT.connect(clientName); //Initialize the bluetooth connection
  
  //Checks for successfull connection
  if (connected) {
    Serial.println("¡Conectado exitosamente!");
  } else {
    while (!BT.connected(10000)) {
      Serial.println("No se pudo conectar. \n Asegúrese de que el dispositivo remoto esté disponible y dentro del alcance, \n luego reinicie la aplicación.");
    }
  }
}

/*
* Sends the temperature and humidity of dht sensor when pressing temp_button and hum_button
*
* No args
* No return
*/
void loop() {
  //Emiting part
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
