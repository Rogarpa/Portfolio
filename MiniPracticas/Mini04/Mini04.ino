 /*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por:
 *  Emmanuel Giron Jimenez
 *  Rodrigo García Padilla
 *Última modificación: 01-octubre-2023
 
*/



const int leds[5] = {14, 27, 26, 25, 33}; //Leds pins number array
int leds_array_length = sizeof(leds)/sizeof(leds[0]); //Calculates the length of leds array

// Sensor
#define PinLDR 34 //LDR sensor pin
#define sensor_resolution 12 //Sensor resolution bits

/*Set:
    pins of leds array as output pins
    
  * No args
  * No return
*/
void setup() {
  for (int i = 0; i < leds_array_length ; i++) {//Sets all pins in leds array as output pins
    pinMode(leds[i], OUTPUT);
  }
}

/*
 * Turns until lednth led according to LDR sensor value.
      
 * No args
 * No return
 */
void loop() {
  int max_sensor_value = pow(2,sensor_resolution)-1;//Max value of sensor
  int led_raised = (int)(analogRead(PinLDR)*leds_array_length/max_sensor_value); //Sensor led range
  turn_on_until(led_raised);
  delay(10);
}

/*
 * Turn on until lednth led in leds array

  args:
    led lednth led to turn on
  No return 
 */
void turn_on_until(int led){
  
  //Check for input correctness
  if(led>leds_array_length){
    return;
  }
  //Turns off all leds
  for (int i = 0; i < leds_array_length; i++) {
    digitalWrite(leds[i], LOW);
  }
  //Turns on until lednth led 
  for (int i = 0; i < led; i++) {
    digitalWrite(leds[i], HIGH);
  }
}