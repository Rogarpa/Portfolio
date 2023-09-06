/*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por:
 *  Emmanuel Giron Jimenez
 *  Rodrigo García Padilla
 *Última modificación: 04-septiembre-2023
 
*/


#define MAIN_DELAY 32 //Modifies the velocity of the led travel
const int leds[5] = {14, 27, 26, 25, 33};//Leds pins' number array
int blinking_direction = 1; //Manages the traveling direction 

/*Set:
    pins of leds array as output pins
    
*/

//We set the pins in leds array as output, that will be used as leds output.
void setup() {
  for (int i = 0; i < 5 ; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

/*
 * Traveling with one on led the leds array, with a delay of MAIN_DELAY.
 */
void loop() {
  for (int i = ((blinking_direction == 1)? 0:4); 0<= i && i < 5; i = i+blinking_direction) {
    digitalWrite(leds[i], HIGH);// turn the LED on (HIGH is the voltage level)
    digitalWrite(leds[i-blinking_direction], LOW); // turn the LED off (HIGH is the voltage level)
    delay(MAIN_DELAY);// wait for the MAIN_DELAY
  }
  blinking_direction = (-1)* blinking_direction; //changes the blinking direction through the leds array
}
