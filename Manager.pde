public class Manager {

  int beatCount = 0;
  ArrayList<Voice> voices;
  ArrayList<Sample> samples; 
  boolean randomize = false; 

  Manager() {

    samples = new ArrayList<Sample>();
    voices = new ArrayList<Voice>();  

  }

  void init() {

    if (arduino != null) {
      for (int i = 0; i < this.voiceCount (); i++) {
        arduino.pinMode( this.getVoice(i).port, Arduino.INPUT);
      }
    }
  }

  void update() {

    for (int i = 0; i < this.voiceCount (); i++) {

      if (arduino != null) {
        
        this.getVoice(i).updateFilter( arduino.digitalRead(this.getVoice(i).port) );
        
        if (this.getVoice(i).filterAverage > .05) {
          this.wakeVoice(i); 
        } else {
          this.sleepVoice(i);
        }
        
      }
    }
  }

  void trigger() {

    for (int i = 0; i < voices.size (); i++) {

      // Is the voice awake?
      if (voices.get(i).isAwake()) {
        
        // Has it been awake long enough?
        if (millis() - voices.get(i).wakeTime > 1000) {
        
          // Does it care about this beat?
          if (voices.get(i).notes[beatCount] > 0) {
  
            float balance = voices.get(i).balance;
            if (!randomize) {
              //this.playSample(i, balance);
            } else {
              int index = voices.get(i).notes[beatCount];
              //this.playSample(index, balance);
            }
            
          }
        }
      }
    }

    beatCount = (beatCount + 1) % 8;
  }  

  int voiceCount() {
    return voices.size();
  }

  int activeVoiceCount() {
    int activeVoices = 0;
    for (int i = 0; i < voices.size (); i++) {
      if (voices.get(i).isAwake()) activeVoices++;
    }
    return activeVoices;
  } 

  Voice getVoice(int index) {
    return voices.get(index);
  }  

  void toggleVoice(int index) {
    if (!voices.get(index).isAwake()) {
      wakeVoice(index);
    } else {
      sleepVoice(index);
    }
  }  

  void wakeVoice(int index) {
    if (voices.get(index).isAwake()) return;    
    voices.get(index).awake();

    float balance = voices.get(index).balance;
    this.playSample(index, balance);

    if (randomize) {
      int activeIndex = 0;

      for (int i = 0; i < voices.size (); i++) {
        if (voices.get(i).isAwake()) {
          voices.get(i).setNotes( STARNOTES[this.activeVoiceCount() -1][activeIndex] );
          activeIndex++;
        }
      }
      
    }
  }

  void sleepVoice(int index) {
    if (!voices.get(index).isAwake()) return;
    voices.get(index).sleep();
  }

  void playSample(int index, float balance) {
    float offset = metronome.getPosition();
    samples.get(index).setBalance(balance);
    samples.get(index).trigger(offset);
  };
}

