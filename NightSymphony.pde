import processing.serial.*;
import org.firmata.*;
import cc.arduino.*;
import ddf.minim.*;
import ddf.minim.ugens.*;
import themidibus.*;
import java.util.Arrays; 

Minim minim;
AudioOutput out;

MidiBus midi;

Metronome metronome;
StarManager starManager;
InsectManager insectManager;

Arduino arduino = null;

void setup() {

  size(640, 480);

  // Sloppy arduino check
  println(Arduino.list());
  if (Arduino.list().length > 4) {
     arduino = new Arduino(this, Arduino.list()[5], 57600);
  }

  // Audio Setup
  minim = new Minim(this);
  out = minim.getLineOut();  

  // Custom Classes
  metronome = new Metronome(120);
  starManager = new StarManager();
  insectManager = new InsectManager();
  
  // Init
  
  starManager.init();
  insectManager.init();
  

  // Midi for testing
  midi = new MidiBus(this, 0, -1);

  // Disable GUI for performance
  //noLoop();

}

void draw()
{  
  background(0);
  stroke(255);
  
  // Update
  
  starManager.update();
  insectManager.update();

  int totalActive = starManager.activeVoiceCount() + insectManager.activeVoiceCount();

  if (totalActive > 0 && !metronome.ticking) metronome.start();
  if (totalActive == 0 && metronome.ticking) metronome.stop();  

  // Stars

  for (int i = 0; i < starManager.voiceCount(); i++) {
    int boxWidth = width / starManager.voiceCount();

    int fillColor = (starManager.getVoice(i).isAwake()) ? 128 : 64;
    fill(fillColor);
    rect(boxWidth * i, 0, boxWidth, boxWidth);
  }
  
  for (int i = 0; i < insectManager.voiceCount(); i++) {
    int boxWidth = width / insectManager.voiceCount();

    int fillColor = (insectManager.getVoice(i).isAwake()) ? 128 : 64;
    fill(fillColor);
    rect(boxWidth * i, boxWidth, boxWidth, boxWidth);
  }  

}

