class Clock implements Instrument
{

  boolean ticking = false;
  int lastTick = 0;
  float duration;

  Clock (float clockDuration) {
    duration = clockDuration; 
    out.setTempo( 60 / duration );
  }

  void start() {
    ticking = true;
    lastTick = millis(); 
    out.playNote( 0, 1f, this);
  }

  void stop() {
    ticking = false;
  }

  void noteOn( float dur )
  {
    // Trigger active insects
    swarm.trigger();
  }

  void noteOff() {

    // Continue clock if there are insects active    
    if (swarm.activeCount > 0) {
      start();
    } else {
      stop();
    }
  }

  float getPosition() {
    return ( (millis() - clock.lastTick) / (duration * 1000.0) );
  }
  
}

