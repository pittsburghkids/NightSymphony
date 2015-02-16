class Sample {
 
  Sampler sampler;
  MultiChannelBuffer sampleBuffer;
  Balance balance;
  int sampleCount = 0;
  
  Sample(String filename, float amplitude) {
    
    println(filename);
    
    // Load the sample into memory
    sampleBuffer = new MultiChannelBuffer( 1, 1024 );
    float sampleRate = minim.loadFileIntoBuffer( filename, sampleBuffer );
    sampleCount = sampleBuffer.getBufferSize ( );

    // Create the sampler and patch through balance
    sampler = new Sampler( sampleBuffer, sampleRate, 2 );
    balance = new Balance(0);
    sampler.patch( balance );
    balance.patch( out );    
    
    sampler.amplitude.setLastValue(amplitude);
    
  }
  
  void trigger(float offset) {
    sampler.trigger();
  }
  
  void rewind() {
    sampler.begin.setLastValue(0);
  }
  
  void setBalance(float newBalance) {
    balance.balance.setLastValue(newBalance);
  }
  
}
