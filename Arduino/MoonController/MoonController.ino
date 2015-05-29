#include <Firmata.h>

#define SELF_IDENTIFY 0xa0
#define SET_BRIGHTNESS 0xa1

int minBrightness = 8;
int maxBrightness = 128;

float currentBrightness = minBrightness;
int targetBrightness = minBrightness;

void sysexCallback(byte command, byte argc, byte *argv)
{
  
  //Firmata.sendSysex(0xa2, argc, argv); 
  
  switch (command) {
    case SET_BRIGHTNESS:
    
    
      int activeVoices = argv[0];
      int totalVoices = argv[1];
      
      int value = ((maxBrightness - minBrightness) * ((float)activeVoices / (float)totalVoices)) + minBrightness;
    
      targetBrightness = value;
      
      break;
  }
}

void setup() {

  Firmata.setFirmwareVersion(FIRMATA_MAJOR_VERSION, FIRMATA_MINOR_VERSION);
  Firmata.begin(57600);

  byte returnData[1];
  returnData[0] = (byte) 16;
  Firmata.sendSysex(SELF_IDENTIFY, 1, returnData);

  pinMode(3, OUTPUT);

  Firmata.attach(START_SYSEX, sysexCallback);
}

void loop() {
  while (Firmata.available()) {
    Firmata.processInput();
  }
  
  if (abs(currentBrightness - targetBrightness) < 1) currentBrightness = targetBrightness;
  
  if (currentBrightness < targetBrightness) {
    currentBrightness += .01;
  } else if (currentBrightness > targetBrightness) {
    currentBrightness -= .01;
  }
  
  analogWrite(3, currentBrightness);
}
