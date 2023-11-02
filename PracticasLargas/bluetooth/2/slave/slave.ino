/*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por: M. en I. Valente Vázquez Velázquez
 *Última modificación: 1-enero-2023
 *https://sites.google.com/ciencias.unam.mx/introduccion-iot-fc/inicio
*/

//Include bluettoth library
#include "BluetoothSerial.h"

//Condition for activating bluetooth
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#define LED 14 //Leds pins number array

BluetoothSerial BT; //Bluetooth Object

/*Set:
    device as bt in slave mode
    pin LED as output led
*/
void setup() {
  Serial.begin(115200); //Initialize serial communication
  BT.begin("ESP32_Vazzvel_Slave"); //Name of device in slave mode
  Serial.println("El dispositivo Bluetooth está listo para emparejarse");
  pinMode(LED, OUTPUT);
}

/*
* Prints the received string and if detect an H of Humdity turn on LED
* elsewhere if detect T letter of Temperature string turn of LED
*
* No args
* No return
*/
void loop() {
  if (BT.available()) //While bt receiving data on qeue
  {
    int val = BT.read(); //Read a byte of data qeue
    
    if(val == 'T'){ //If detect H char turn on led
      Serial.print("High");
      digitalWrite(LED, HIGH); 
    }
    
    if(val == 'H'){ //If detect T char turn off led
      Serial.print("Low");
      digitalWrite(LED, LOW);
    }
    
    Serial.print((char)val); //Print received byte
  }

}
