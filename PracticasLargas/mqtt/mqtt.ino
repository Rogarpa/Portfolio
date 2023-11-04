/*
  Universidad Nacional Autónoma de México
  Facultad de Ciencias
  Licenciatura en Ciencias de la Computación
  Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas

  Escrito por:
  García Padrilla Rodrigo 
  Giron Jimenez Emmanuel
  Última modificación: 04-Noviembre-2023
*/

//Bibliotecas (Herramientas -> Administrar Biblotecas... -> buscardor "EspMQTTClient")
#include "EspMQTTClient.h"
//Incluir librería del sensor de temperatura y humedad (Herramientas -> Administrar Biblotecas... -> buscardor "DHT sensor library") 
#include "DHT.h"

//Definimos pines
#define pinLED1 14
#define pinLED2 27
#define pinLED3 26
#define pinLED4 25
#define pinLED5 33
#define PinBotton_PullUp 4
#define PinBotton_PullDown 15

//Definir los pines a los que está conectado el sensor DHT
#define DHTPIN 32
#define DHTTYPE DHT11
//Defino pin de la fotoresistencia
#define PinLDR 34 


//Variables de configuración del objeto MQTT cliente
const char* ssid = "Totalplay-A9AA";
const char* password = "A9AAB22FkEScavpX";
const char* broker = "test.mosquitto.org";
const char* nameClient = "ESP32_prueba"; //Cambiar nombre
const int port = 1883;

//topicos
String T_LEDS = "ClaseIoT/Giron/Leds";
String T_TEMP = "ClaseIoT/Giron/DHT/Temperatura";
String T_HUME = "ClaseIoT/Giron/DHT/Humedad";
String T_POT = "ClaseIoT/Giron/Pot";

//Variables globales
long timeDHT = millis();

// Variables que representaran la ultima actualizacion
float ultiHume = 0.0; //lastHumidity
float ultiTem = 0.0; //lastTemperature

// Variables para rastrear la última actualización de la potencia y de DHT
long lastPotUpdate = 0; 
static long lastDHTUpdate = 0;

//Objeto cliente
DHT dht(DHTPIN, DHTTYPE);
EspMQTTClient client(ssid, password, broker, nameClient, port);

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(pinLED1, OUTPUT);
  pinMode(pinLED2, OUTPUT);
  pinMode(pinLED3, OUTPUT);
  pinMode(pinLED4, OUTPUT);
  pinMode(pinLED5, OUTPUT);

   //Configurar los botones como entradas
  pinMode(PinBotton_PullUp, INPUT);
  pinMode(PinBotton_PullDown, INPUT);  
  pinMode(PinLDR, INPUT); //Declarar al pin LDR como entrada

  if (!client.isConnected()) {
    Serial.println("Conectado con el broker!");
  }
  else {
    Serial.println("No Conectado, revise su conexión");
  }
  delay(5000);
}


void onConnectionEstablished() {
  //Prender y apagar LEDs
  client.subscribe(T_LEDS, [](const String & payload) {
    if (payload == "1") { //prendemos led 1
      digitalWrite(pinLED1, HIGH);
      Serial.println("Led 1: encendido");
    }
    else if (payload == "2") { //prendemos led 2
      digitalWrite(pinLED2, HIGH);
      Serial.println("Led 2: Encendido");
    }
    else if (payload == "3") { //prendemos led 3
      digitalWrite(pinLED3, HIGH);
      Serial.println("Led 3: Encendido");
    }
    else if (payload == "4") { //prendemos led 4
      digitalWrite(pinLED4, HIGH);
      Serial.println("Led 4: Encendido");
    }
    else if (payload == "5") { //prendemos led 5
      digitalWrite(pinLED5, HIGH);
      Serial.println("Led 5: Encendido");
    }
    else if (payload == "0") { //se apagan todos los leds prendidos
      digitalWrite(pinLED1, LOW);
      digitalWrite(pinLED2, LOW);
      digitalWrite(pinLED3, LOW);
      digitalWrite(pinLED4, LOW);
      digitalWrite(pinLED5, LOW);
      Serial.println("Leds apagados");
    }
    else {
      Serial.println("Dato no válido");
    }
  });
}

void loop() {
  client.loop();
  long currentMillis = millis();
  
  
  if (currentMillis - lastDHTUpdate >= 2500) { 
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (!isnan(h) && !isnan(t)) {
      ultiHume = h;
      ultiTem = t;
    } else {
      Serial.println("Failed to read from DHT sensor!");
    }
    lastDHTUpdate = currentMillis;
  }
  
    //Publica la humedad y temperatur
    if (digitalRead(PinBotton_PullUp) == 0) { //Al cambiar el valor de PullUp, se publica la humedad en el topico ClaseIoT/Giron/DHT/Humedad
      client.publish(T_HUME, String(ultiHume));
      Serial.print("Humedad: ");
      Serial.print(ultiHume);
      Serial.println(" %.");
      delay(500);
    }
    if (digitalRead(PinBotton_PullDown) == 1) { // Al cambiar el valor del PushDown, se publica la temperatura en el topico ClaseIoT/Giron/DHT/Temperatura
      client.publish(T_TEMP, String(ultiTem));
      Serial.print("Temperatura: ");
      Serial.print(ultiTem);
      Serial.println(" °C.");
      delay(500);
    }

      // Publica el voltaje de la fotorresistencia cada 5 segundos
  if (currentMillis - lastPotUpdate >= 5000) {
    int sensor = analogRead(PinLDR); 
    float voltage = 3.3 / 4096 * sensor; // Calculo del voltaje
    client.publish(T_POT, String(voltage)); 
    String potMessage = "Voltage: " + String(voltage) + ".";
    Serial.println(potMessage);
    delay(500); 
    lastPotUpdate = currentMillis; // Actualiza el tiempo de la última actualización de potencia
  }
}
