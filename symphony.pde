import processing.serial.*;
import org.firmata.*;
import cc.arduino.*;
import ddf.minim.*;
import ddf.minim.ugens.*;

Arduino arduino;
boolean useArduino = true;

Minim minim;
AudioOutput out;

Clock clock;
Swarm swarm;

String keys = "qwertyuiopasdfghjklzxcvb";

void setup() {

  size(640, 480);

  // Audio Setup
  minim = new Minim(this);
  out = minim.getLineOut();  

  // Custom Classes
  clock = new Clock(2.0);
  swarm = new Swarm();

  // Arduino Setup

  if (useArduino) {
    println(Arduino.list());
    arduino = new Arduino(this, Arduino.list()[0], 57600);

    for (int i = 0; i < swarm.insectCount (); i++) {
      arduino.pinMode(swarm.getInsect(i).port, Arduino.INPUT);
    }
  }
  // Disable GUI for performance
  //noLoop();
}

void draw()
{  
  background(0);

  for (int i = 0; i < swarm.insectCount (); i++) {
    if (useArduino) {
      if (arduino.digitalRead(swarm.getInsect(i).port) == Arduino.HIGH) {
        swarm.wakeInsect(i);
      } else {
        swarm.sleepInsect(i);
      }
    }

    stroke(255);
    if (swarm.getInsect(i).awake) {
      fill(255, 128, 128);
    } else {
      fill(0);
    }
    rect(0, i * (height / swarm.insectCount()), width, (height / swarm.insectCount()));
  }

  float x = clock.getPosition() * width;
  line(x, 0, x, height);
}

void keyPressed() {
  // Toggle an insect based on key press
  int index = keys.indexOf(key);
  if (index >= 0 && index < swarm.insectCount()) {
    swarm.toggleInsect(index);
  }
}

