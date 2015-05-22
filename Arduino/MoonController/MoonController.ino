#include <Firmata.h>

#define SELF_IDENTIFY 0xa0

void setup() {
  
  Firmata.setFirmwareVersion(FIRMATA_MAJOR_VERSION, FIRMATA_MINOR_VERSION);
  Firmata.begin(57600);  
  
  byte returnData[1];
  returnData[0] = (byte) 16;
  Firmata.sendSysex(SELF_IDENTIFY, 1, returnData);  
  
}

void loop() {
  while (Firmata.available()) {
    Firmata.processInput();
  }  
}
