/*
  This is a tricky way to create a metronome using a
  Minim "instrument" that triggers itself.
*/

class Metronome implements Instrument
{
  boolean ticking = false;
  int lastTick = 0;
  float duration;

  int measure = -1;
  int beat = -1;

  Metronome (float bpm) {
    duration = 60 / bpm; 
    out.setTempo( bpm );
  }
  
  // Metronome management

  void start() {
    ticking = true;
    tick();
    
    measure = -1;
    beat = -1;
  }

  void stop() {
    ticking = false;
  }

  void tick() {
    lastTick = millis(); 
    out.playNote( 0, 1f, this);
  }

  // Trigger sound managers and track beats/measures

  void noteOn( float dur )
  {  
    beat = (beat + 1) % 4;
    if (beat == 0) measure++;   
    
    insectManager.trigger();
    starManager.trigger();   
  }
  
  // Schedule a new note if we're still ticking

  void noteOff() {
    if (ticking) tick();
  }

  // Returns a percentage for where we are in a beat

  float getPosition() {
    return ( (millis() - metronome.lastTick) / (duration * 1000.0) );
  }
  
}

