class Insect {

  // Properties
  Sampler sampler;
  MultiChannelBuffer sampleBuffer;
  ADSR adsr;  
  Balance balance;
  int sampleCount = 0;
  boolean awake = false;
  int port;
  int stopVotes= 0;

  //Constructor
  Insect(int insectPort, String filename) {

    port = insectPort;
    
    // Load the sample into memory
    sampleBuffer = new MultiChannelBuffer( 1, 1024 );
    float sampleRate = minim.loadFileIntoBuffer( filename, sampleBuffer );
    sampleCount = sampleBuffer.getBufferSize ( );

    // Create the sampler and patch through balance and adsr
    sampler = new Sampler( sampleBuffer, sampleRate, 1 );
    adsr = new ADSR( 1.0, 0.5, 0.05, 0.75, 0.5 );
    balance = new Balance(random(-1, 1));
    sampler.patch( balance );
    balance.patch( adsr );
  }

  // Only called by the global clock
  void trigger() {
    // Reset and trigger if active   
    if (awake) {
      sampler.begin.setLastValue(0);
      sampler.trigger();
    }
  }

  // Only called by user interaction
  void play(float offset) {
    stopVotes= 0;
    if (this.awake) return;
    
    // Offset to match global clock and play 
    sampler.begin.setLastValue(offset * sampleCount);
    sampler.trigger();

    // Start the attack envelope
    adsr.unpatch(out);
    adsr.noteOn();
    adsr.patch(out);

    // Flag insect as active
    this.awake = true;
    println("START");
  }

  // Only called by user interaction 
  boolean stop() {
    if (!this.awake) return true;
    
    stopVotes++;
    if(stopVotes == 4){
      stopVotes= 0;
      // Start the release envelope
      adsr.unpatchAfterRelease( out );
      adsr.noteOff();

      // Flag insect as inactive 
      this.awake = false;
      println("STOP");
      return true;
    }
    return false;
  }
}

