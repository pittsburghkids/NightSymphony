public class InsectManager extends Manager {

  InsectManager() {

    this.randomize = false;

    // Initialize voices and samples
  
  /*
    samples.add( new Sample("insects/cricket_1.wav", .5) );
    voices.add( new Voice(57, 1.00, new int[] {
      1, 0, 1, 1, 1, 0, 1, 0
    } 
    ) );

    samples.add( new Sample("insects/cricket_2.wav", .5) ); 
    voices.add( new Voice(58, -1.00, new int[] {
      1, 1, 0, 1, 1, 1, 0, 1
    } 
    ) );

  */

    samples.add( new Sample("insects/cicada_1.wav", .5) ); 
    voices.add( new Voice(2, 3, 1.00, new int[] {
      1, 0, 0, 0, 1, 0, 0, 1
    } 
    ) );

  /*

    samples.add( new Sample("insects/cicada_2.wav", .5) );
    voices.add( new Voice(61, -1.00, new int[] {
      0, 0, 1, 0, 1, 0, 1, 0
    } 
    ) );    
    
    samples.add( new Sample("insects/dragonfly_1.wav", .5) );
    voices.add( new Voice(56, 1.00, new int[] {
      1, 0, 1, 0, 1, 1, 0, 0
    } 
    ) );
    
    samples.add( new Sample("insects/dragonfly_2.wav", .5) );   
    voices.add( new Voice(59, -1.00, new int[] {
      0, 1, 0, 0, 0, 0, 1, 1
    } 
    ) );



    samples.add( new Sample("insects/mosquito.wav", .5) );
    voices.add( new Voice(60, 1.00, new int[] {
      0, 0, 1, 0, 0, 0, 1, 0
    } 
    ) );

    samples.add( new Sample("insects/moth.wav", .5) );
    voices.add( new Voice(55, -1.00, new int[] {
      1, 0, 0, 0, 1, 0, 1, 0
    } 
    ));
    
    */
    
  }
}

