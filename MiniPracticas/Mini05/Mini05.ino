/*
 *Universidad Nacional Autónoma de México
 *Facultad de Ciencias
 *Licenciatura en Ciencias de la Computación
 *Seminario de Ciencias de la Computación A: Introducción al Internet de las Cosas
 *
 *Escrito por:
 *  Emmanuel Giron Jimenez
 *  Rodrigo García Padilla
 *Última modificación: 08-septiembre-2023
 
*/

/*Defines emulation pins*/
#define PinPWM 14 //Pin for emulate on led PWM sin wave
#define PinDAC 26 //Pin for emulate on led analog sin wave
#define PinADC1 12 //Pin for reading PWM sin wave emulation
#define PinADC2 13 //Pin for reading analog sin wave emulation





/*Defines PWM variables*/
const int freq = 1000; //Frecuency on hz
const int ChanelPWM = 0; //Channel between 0-15
const int resolution = 8; //Resolution bits

/*
* Sets:
* The pins for emulation
*
* No args
* No return
*/
void setup() {
  pinMode(PinPWM, OUTPUT); //PWM as output
  ledcSetup(ChanelPWM, freq, resolution); //Configuring PWM channel
  ledcAttachPin(PinPWM, ChanelPWM); //Link channel to PinPWM

  /*PinDAC configuration*/
  pinMode(PinDAC, OUTPUT);

  /*Readers of emulation on PinADC1 and PinADC2*/
  pinMode(PinADC1, INPUT);
  pinMode(PinADC2, INPUT);
}

/*Emulates sin wave in PinPWM and PinDAC leds
*
* No args
* No return
*/
void loop() {
    for (int i = 0; i < 360; i++) {
    /*
    *Sin function transformed to on 0-255 range, and transforming i into radians.
    *Displacing it 127 and transforming it amplitude into 128
    */
    float sin_mod = 128 * sin(i * M_PI / 180) + 127;
    
    /*
    *Emulates sin_mod function into PinDAC
    */
    ledcWrite(ChanelPWM, sin_mod); 
    
    /*
    *My especific led turning on threshold, is the analog value when it starts shinning on (0-255).
    Emulates the sin function on PinDAC
      Transformating the sin_mod into sin*k+t to be displayed correctly on PinDAC, where:
      k is the constant that sets sin range (0-255) into led turning on range (t to 255)
      t is the led turning on threshold
    That displace the sin_mod function to turning on led threshold and fits its amplitude between 
    this threshold and maximum PinDAC writing value (255).
    */
    int turning_on_led_threshold = 196;
    dacWrite(PinDAC, (sin_mod*(255-turning_on_led_threshold)/255)+turning_on_led_threshold);
    delayMicroseconds(10000);

    
    float v1 = analogRead(PinADC1); //Reads the PWM sin_mod wave emulation
    float v2 = analogRead(PinADC2); //Reads the analog sin_mod wave emulation
    delayMicroseconds(10000);
    
    // Prints the readings of PWM and analog emulation on serial
    Serial.print("S1:");
    Serial.print(v1);
    Serial.print(",");
    Serial.print("S2:");
    Serial.println(v2);    
  }
}

