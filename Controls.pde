/*
  Keyboard and midi control for testing
*/

// Keyboard controls

void keyPressed() {

  int starIndex = starKeys.indexOf(key);
  if (starIndex >= 0 && starIndex < starManager.voiceCount()) {
    starManager.wakeVoice(starIndex);
  }

  int insectIndex = insectKeys.indexOf(key);
  if (insectIndex >= 0 && insectIndex < insectManager.voiceCount()) {
    insectManager.wakeVoice(insectIndex);
  }
}

void keyReleased() {

  int starIndex = starKeys.indexOf(key);
  if (starIndex >= 0 && starIndex < starManager.voiceCount()) {
    starManager.sleepVoice(starIndex);
  }  

  // Check for voice releases

  int insectIndex = insectKeys.indexOf(key);
  if (insectIndex >= 0 && insectIndex < insectManager.voiceCount()) {
    insectManager.sleepVoice(insectIndex);
  }  
}


//  Midi control

void noteOn(int channel, int pitch, int velocity) {

  int starIndex = Arrays.asList(starMidi).indexOf(pitch);
  if (starIndex >= 0 && starIndex < starManager.voiceCount()) {
    starManager.wakeVoice(starIndex);
  }  

  int insectIndex = Arrays.asList(insectMidi).indexOf(pitch);
  if (insectIndex >= 0 && insectIndex < insectManager.voiceCount()) {
    insectManager.wakeVoice(insectIndex);
  }
  
}

void noteOff(int channel, int pitch, int velocity) {

  int starIndex = Arrays.asList(starMidi).indexOf(pitch);
  if (starIndex >= 0 && starIndex < starManager.voiceCount()) {
    starManager.sleepVoice(starIndex);
  }  

  int insectIndex = Arrays.asList(insectMidi).indexOf(pitch);
  if (insectIndex >= 0 && insectIndex < insectManager.voiceCount()) {
    insectManager.sleepVoice(insectIndex);
  }
}
