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

// Descargar el .ZIP de la página: https://github.com/shurillu/CTBot .Programa -> Incluir Librería -> Añadir blibloteca .ZIP... -> Agregar el .ZIP que se descargo.
#include "CTBot.h" //Herramientas -> Administrar Biblotecas -> buscar e instalar "CTBot" y tambien buscar e instalar "ArduinoJson". 

// Define pin del potenciometro.
#define pinPot 35
// Define pin de la fotorresistencia.
#define pinPhoto 34
// Define los pins de los 5 leds.
#define pinLED1 14 
#define pinLED2 27
#define pinLED3 26
#define pinLED4 25
#define pinLED5 33

CTBot myBot; // Crea un objeto para interactuar con el bot de Telegram.

// Detalles de la red Wi-Fi y el token de autenticación del bot de Telegram.
String ssid = "Totalplay-A9AA";  // Reemplazar con tu SSID de Wi-Fi.
String pass = "A9AAB22FkEScavpX"; // Reemplazar con tu contraseña de Wi-Fi.
String token = "6644135453:AAHANQ76hljp7Gqnqdh1X49UKHxdokyBHfY"; // Reemplazar con el token de tu bot de Telegram. 

// Definir estado de los leds.
int led1State = LOW;
int led2State = LOW;
int led3State = LOW;
int led4State = LOW;
int led5State = LOW;
// Estado de la alarma. 
boolean state = false;
// Definir el umbral.
int umbral = 100000;
int id = 0;
boolean esperarUbral = false;  // Variable para controlar si se espera el umbral.

void setup() {
  Serial.begin(115200); // Inicia la comunicación serial.
  Serial.print("Comenzando TelegramBot...  ");
  pinMode(pinPot, INPUT); //potenciometro
  pinMode(pinPhoto, INPUT); // Configura el pin del sensor como entrada.
  pinMode(pinLED1, OUTPUT);  // Configura el pin del LED como salida.
  pinMode(pinLED2, OUTPUT);  // Configura el pin del LED como salida.
  pinMode(pinLED3, OUTPUT);  // Configura el pin del LED como salida.
  pinMode(pinLED4, OUTPUT);  // Configura el pin del LED como salida.
  pinMode(pinLED5, OUTPUT);  // Configura el pin del LED como salida.  
  digitalWrite(pinLED1, led1State); // Inicializa el LED en estado apagado.
  digitalWrite(pinLED2, led2State); // Inicializa el LED en estado apagado.
  digitalWrite(pinLED3, led2State); // Inicializa el LED en estado apagado.
  digitalWrite(pinLED4, led2State); // Inicializa el LED en estado apagado.
  digitalWrite(pinLED5, led2State); // Inicializa el LED en estado apagado.
  
  myBot.wifiConnect(ssid, pass); // Conecta a la red Wi-Fi especificada.
  myBot.setTelegramToken(token); // Establece el token de autenticación para el bot de Telegram.
  delay(2000); // Espera un momento para que la conexión se establezca.

  // Verifica si la conexión con el bot de Telegram se ha establecido correctamente.
  if (myBot.testConnection())
    Serial.println("Conectado con Bot");
  else
    Serial.println("Error en la conexión");
}

void loop() {
  TBMessage msg; // Crea un objeto para almacenar los mensajes entrantes de Telegram.
  int sensor = analogRead(pinPhoto); // Lee el valor actual del sensor.
  
  // Verifica si hay un nuevo mensaje para el bot de Telegram.
  if (myBot.getNewMessage(msg)) {
    if (msg.text.equalsIgnoreCase("/start")) {
      // Si el comando es "/start", responde con un mensaje de bienvenida e instrucciones.
      Serial.print("Nueva interacción de: ");
      Serial.println(msg.sender.username);
      myBot.sendMessage(msg.sender.id, "Para encender los LEDs:\nMandar /1: si quieres encender el LED nº 1.\nMandar /2: si quieres encender el LED nº 2.\nMandar /3: si quieres encender el LED nº 3.\nMandar /4: si quieres encender el LED nº 4.\nMandar /5: si quieres encender el LED nº 5.\nSi quieres apagar los leds encendidos, volver a mandar el valor del led prendido.\n\nSi quieres el valor actual del potenciómetro, manda /Dato\nSi quieres activar la alarma, manda /Alarma (tendras que establecer un umbral para la alarma).\nSi quieres desactivar la alarma, manda /Alto");
    }
    else if (msg.text.equalsIgnoreCase("/Alarma")){
      // Si el comando es "/Alarma", activa la alarma y guarda el ID del chat.
      state = true;
      id = msg.sender.id;
      String mensaje = "Alarma activada.";
      myBot.sendMessage(msg.sender.id, mensaje);
      Serial.println(mensaje);
       String mensaje1 = "Proporciona el umbral con el que la alarma se activará:";
      myBot.sendMessage(msg.sender.id, mensaje1);

      esperarUbral = true;  // Establece la bandera de espera para el umbral.
        
    }
    else if (msg.text.equalsIgnoreCase("/Alto")){
      // Si el comando es "/Alto", desactiva la alarma.
      state = false;
      id = msg.sender.id;
      String mensaje = "Alarma desactivada";
      myBot.sendMessage(msg.sender.id, mensaje);
      Serial.println(mensaje);
      id = 0; // Restablece el ID del chat ya que la alarma está desactivada.
      umbral = 100000;
    }
    else if (msg.text.equalsIgnoreCase("/Dato")) {
      // Si el comando es "/Dato", envía el valor actual del sensor al usuario.
      Serial.print("Monitoreo del potenciometro: ");
      int sensor1 = analogRead(pinPot); // Lee el valor actual del sensor.
      Serial.println(sensor1); // Imprime el valor del sensor en el monitor serial.
      String mensaje1 = (String)"El valor actual es: " + (String)sensor1;
      myBot.sendMessage(msg.sender.id, mensaje1); // Envía el valor del sensor al chat de Telegram.
      Serial.println("Dato enviado");
    }
    else if (msg.text.equalsIgnoreCase("/1")) {
  // Si el mensaje es "1", alterna el estado del LED1
  led1State = (led1State == LOW) ? HIGH : LOW;
  digitalWrite(pinLED1, led1State);
  String mensaje1 = (led1State == HIGH) ? "Led 1 encendido" : "Led 1 apagado";
  myBot.sendMessage(msg.sender.id, mensaje1);

  // Imprime el estado del LED en el puerto serie
  if (led1State == HIGH) {
    Serial.println("LED 1: ON");
  } else {
    Serial.println("LED 1: OFF");
  }
    }
    else if (msg.text.equalsIgnoreCase("/2")) {
  // Si el mensaje es "2", alterna el estado del LED2
  led2State = (led2State == LOW) ? HIGH : LOW;
  digitalWrite(pinLED2, led2State);
  String mensaje1 = (led2State == HIGH) ? "Led 2 encendido" : "Led 2 apagado";
  myBot.sendMessage(msg.sender.id, mensaje1);

  // Imprime el estado del LED en el puerto serie
  if (led2State == HIGH) {
    Serial.println("LED 2: ON");
  } else {
    Serial.println("LED 2: OFF");
  }
    }
    else if (msg.text.equalsIgnoreCase("/3")) {
  // Si el mensaje es "3", alterna el estado del LED13
  led3State = (led3State == LOW) ? HIGH : LOW;
  digitalWrite(pinLED3, led3State);
  String mensaje1 = (led3State == HIGH) ? "Led 3 encendido" : "Led 3 apagado";
  myBot.sendMessage(msg.sender.id, mensaje1);

  // Imprime el estado del LED en el puerto serie
  if (led3State == HIGH) {
    Serial.println("LED 3: ON");
  } else {
    Serial.println("LED 3: OFF");
  }
    }
    else if (msg.text.equalsIgnoreCase("/4")) {
  // Si el mensaje es "14", alterna el estado del LED4
  led4State = (led4State == LOW) ? HIGH : LOW;
  digitalWrite(pinLED4, led4State);
  String mensaje1 = (led4State == HIGH) ? "Led 4 encendido" : "Led 4 apagado";
  myBot.sendMessage(msg.sender.id, mensaje1);

  // Imprime el estado del LED en el puerto serie
  if (led4State == HIGH) {
    Serial.println("LED 4: ON");
  } else {
    Serial.println("LED 4: OFF");
  }
    }
    else if (msg.text.equalsIgnoreCase("/5")) {
  // Si el mensaje es "5", alterna el estado del LED5
  led5State = (led5State == LOW) ? HIGH : LOW;
  digitalWrite(pinLED5, led5State);
  String mensaje1 = (led5State == HIGH) ? "Led 5 encendido" : "Led 5 apagado";
  myBot.sendMessage(msg.sender.id, mensaje1);

  // Imprime el estado del LED en el puerto serie
  if (led5State == HIGH) {
    Serial.println("LED 5: ON");
  } else {
    Serial.println("LED 5: OFF");
  }
    } else if (esperarUbral) {
      // Si estamos esperando el umbral, intenta interpretar el mensaje como un umbral.
      int umbral1 = msg.text.toInt();
      if (umbral1 > 0) {
        umbral = umbral1;
        Serial.println(umbral);
        esperarUbral = false;  // Reinicia la bandera de espera para el umbral.
        myBot.sendMessage(msg.sender.id, "Umbral establecido correctamente.");
      } else {
        myBot.sendMessage(msg.sender.id, "El umbral debe ser un número entero positivo. Intenta de nuevo.");
      }
    }
    
    else {
      // Si el mensaje recibido no coincide con ninguno de los comandos anteriores, envía un mensaje de error.
      myBot.sendMessage(msg.sender.id, "Mensaje no válido, intenta de nuevo con: /start");
    }
  }
  
  if (sensor > umbral) {
        Serial.println(sensor);
        String mensaje = "¡¡Alarma encendida!! El nivel aumentó a: " + String(sensor);
        myBot.sendMessage(msg.sender.id, mensaje);
      }

    
  delay(50);
}
