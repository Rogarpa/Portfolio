/*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por:
 *  Emmanuel Giron Jimenez
 *  Rodrigo García Padilla
 *Última modificación: 30-agosto-2023
 
*/

#define LED_BLINKING 14 //The output pin where the led should be placed.
#define MAIN_DELAY 8 //The frecuency detected by the human eye is 60hz, so the period in seconds is T = 1/f, 
                        //and due that the ddelay is the half of the period of turning on and off, the value obtained 
                        //is this one


/*Set:
    LED_BLINKING  as output pin
    
*/
  
void setup() {
  pinMode(LED_BLINKING , OUTPUT);
}

/*
 * Turn on, and off LED_BLINKING with a delay of MAIN_DELAY.
 */
void loop() {
  digitalWrite(LED_BLINKING, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(MAIN_DELAY);                       // wait for the MAIN_DELAY
  digitalWrite(LED_BLINKING, LOW);    // turn the LED off by making the voltage LOW
  delay(MAIN_DELAY);                       // wait for the MAIN_DELAY
}
