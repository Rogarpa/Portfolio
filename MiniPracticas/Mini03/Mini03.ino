/*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por:
 *  Emmanuel Giron Jimenez
 *  Rodrigo García Padilla
 *Última modificación: 30-septiembre-2023
 
*/



const int leds[5] = {14, 27, 26, 25, 33}; //Leds pins' number array
int leds_array_length = sizeof(leds)/sizeof(leds[0]); //Calculates the length of leds array
#define PinBotton_PullUp 4 //Continue on loop of leds button
#define PinBotton_PullDown 15 //Turning off and resetting leds button
int count = 0; //Counter for leds loop
long timeCounter = 0; //Last time since pressed button
const int timeThreshold = 150; //Threshold time for pushing button



/*Set:
    pins of leds array as output pins
    PinBotton_PullUp as input button
    PinBotton_PullUp as input button
    
*/
void setup() {
  for (int i = 0; i < leds_array_length ; i++) {//Sets all pins in leds array as output pins
    pinMode(leds[i], OUTPUT);
  }

  pinMode(PinBotton_PullUp, INPUT);//Sets the Pull Up switch as input button
  pinMode(PinBotton_PullDown, INPUT);//Sets the Pull Down switch as input button
}

/*
 * Turning on into cycle incrementally the leds in leds array,
 * according to PinBotton_PullUp pushings with timeThreshold time spacings.
 */
void loop() {
  int in_up = digitalRead(PinBotton_PullUp);
  int in_down = digitalRead(PinBotton_PullDown);
  if (in_up == LOW) {
    if (millis() > timeCounter + timeThreshold) {//Accept button push, if the button hasn't been pushed before last accepted pushed
      continue_cycle();//Keep turning on of leds on loop
      timeCounter = millis();
    }
  }
  if(in_down == HIGH){
    reset_cycle();
  }
}

/*
 * Continue with the led turning on according to count, turning on the countth led,
 * and turning off all the leds in leds pins array if all has been turned on.

  No args
  No return 
 */
void continue_cycle(){
  
  /*
   * If all leds has been turned on
   */
  if(count == leds_array_length){
    reset_cycle();
    
  /*
   * Turns on next led
   */
  }else{
    digitalWrite(leds[count], HIGH);
    count++;
  }
}


/*
 * Restart to the initial state::
      -Turning off all the leds.
      -Resetting the counter to inital state.
 * No args
 * No return
 */
void reset_cycle(){
  count = 0;
  for (int i = 0; i < leds_array_length; i++) {
  digitalWrite(leds[i], LOW);
  }
}
