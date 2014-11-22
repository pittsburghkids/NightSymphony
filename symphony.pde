import processing.serial.*;
import ddf.minim.*;
import cc.arduino.*;

Arduino arduino;
Minim minim;
AudioPlayer cricket, cicada, mantis, spittle, bee, mosquito;

float threshold = 200; // Out of 1023

void setup() {
  size(640, 360);

  // Arduino Setup

  println(Arduino.list());

  // Change port here based on list above
  arduino = new Arduino(this, Arduino.list()[2], 57600);

  // Audio Setup

  minim = new Minim(this);

  cricket = minim.loadFile("cricket.wav");
  cicada = minim.loadFile("cicada.wav");
  mantis = minim.loadFile("mantis.wav");
  spittle = minim.loadFile("spittle.wav");
  bee = minim.loadFile("bee.wav");
  mosquito = minim.loadFile("mosquito.wav");
  
  cricket.loop();
  cicada.loop();
  mantis.loop();  
  spittle.loop();
  bee.loop();
  mosquito.loop();
  
}

void draw() {
  background(4, 79, 111);
  fill(84, 145, 158);
  stroke(255);
  
  for (int i = 0; i <= 5; i++) {
    rect((width/6.0) * i, height - (height * (arduino.analogRead(i)/1023.0)), width/6.0, height);
  }
  
  if (arduino.analogRead(0) > threshold) cricket.mute(); else cricket.unmute();
  if (arduino.analogRead(1) > threshold) cicada.mute(); else cicada.unmute();
  if (arduino.analogRead(2) > threshold) mantis.mute(); else mantis.unmute();
  if (arduino.analogRead(3) > threshold) spittle.mute(); else spittle.unmute();
  if (arduino.analogRead(4) > threshold) bee.mute(); else bee.unmute();
  if (arduino.analogRead(5) > threshold) mosquito.mute(); else mosquito.unmute();
  
  stroke(255,0,0);
  float thresholdHeight = height - (threshold/1023.0 * height);
  line (0, thresholdHeight, width, thresholdHeight );
  
  delay(250);
  
}

