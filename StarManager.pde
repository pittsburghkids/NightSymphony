class StarManager extends Manager {

  StarManager() {

    this.randomize = true;
    
    // Intialize samples

    samples.add( new Sample("bells/bells.plastic.ff.C5B5001.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C5B5003.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C5B5005.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C5B5006.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C5B5008.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C5B5010.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C5B5012.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C6B6001.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C6B6003.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C6B6005.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C6B6006.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C6B6008.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C6B6010.wav", 1.0) );
    samples.add( new Sample("bells/bells.plastic.ff.C6B6012.wav", 1.0) );

    // Initialize voices

    voices.add( new Voice(2, 1.00, null) );
    voices.add( new Voice(3,  0.75, null) );
    voices.add( new Voice(4,  0.50, null) );
    voices.add( new Voice(5,  0.25, null) );
    voices.add( new Voice(6,  -0.25, null) );
    voices.add( new Voice(7,  -0.50, null) );
    voices.add( new Voice(8,  -0.75, null) );
    voices.add( new Voice(9,  -1.00, null) );
  }
  
}

