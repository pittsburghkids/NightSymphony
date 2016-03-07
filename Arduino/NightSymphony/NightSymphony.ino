#include <Firmata.h>

#define INPUT_COUNT 6
#define BUFFER_LENGTH 3
#define TARGET_LOOP_TIME 744

#define SELF_IDENTIFY 0xa0
#define TRIGGER_CHANGE 0xb0
#define SET_BRIGHTNESS 0xa1
#define HEARTBEAT 0xa3

#define MOON 5

byte dipPins[4] {
  PIN_TO_DIGITAL(A4), PIN_TO_DIGITAL(A3), PIN_TO_DIGITAL(A2), PIN_TO_DIGITAL(A1)
};

byte inputPins[INPUT_COUNT] = {
  8, 4, PIN_TO_DIGITAL(A5),
  12, 7, 2
};
byte outputPins[INPUT_COUNT] {
  10, 6, 3,
  11, 9, 5
};

float fadeUpStep = .2;
float fadeDownStep = .2;

float maxBrightness = 96;
float minBrightness = 6;

typedef struct {
  byte pinNumber;

  byte ledPin;

  float currentBrightness = 0;
  float releasedBrightness = 0;
  float pressedBrightness = 0;

  byte buffer[BUFFER_LENGTH];
  byte bufferSum;
  boolean pressed;

  unsigned long pressedTime;
  unsigned long releasedTime;

}
Input;

//
// Indexes
//

int bitIndex = 0;
int byteIndex = 0;

//
// Timing
//

unsigned long loopTime = 0;
unsigned long previousTime = 0;

//
// Thresholds
//

int pressThreshold = int(13.2 + 1.5);
int releaseThreshold = int(13.2 - 1.5);

// Inputs

Input inputs[INPUT_COUNT];

// Moon

float minMoonBrightness = 20;
//float maxMoonBrightness = 255;

float currentMoonBrightness = 0;
float targetMoonBrightness = minMoonBrightness;
unsigned long lastMoonFadeTime = 0;

// Heartbeat
unsigned long lastBeatTime= 0;

// Sysex Hanlder

void sysexCallback(byte command, byte argc, byte *argv)
{

  //Firmata.sendSysex(0xa2, argc, argv);

  switch (command) {
    
    case SET_BRIGHTNESS:
      targetMoonBrightness = currentMoonBrightness + 16.0;
      if (targetMoonBrightness > 320.0) targetMoonBrightness= 320.0;
      break;
      
    case SELF_IDENTIFY:
      identify();
      break;
  }
}

// Setup

void setup()
{
  pinMode(13, OUTPUT);

  Firmata.setFirmwareVersion(FIRMATA_MAJOR_VERSION, FIRMATA_MINOR_VERSION);
  Firmata.begin(57600);

  for (int i = 0; i < INPUT_COUNT; i++)
  {
    // Input Pins

    pinMode(inputPins[i], INPUT);
    digitalWrite(inputPins[i], HIGH);

    // Setup Inputs

    inputs[i].pinNumber = inputPins[i];
    inputs[i].ledPin = outputPins[i];
    inputs[i].pressed = digitalRead(inputs[i].pinNumber);

    for (int j = 0; j < BUFFER_LENGTH; j++) {
      //inputs[i].buffer[j]= 0x00;
      if(inputs[i].pressed) inputs[i].buffer[j]= 0xFF;
      else inputs[i].buffer[j]= 0x00;
    }

    if(inputs[i].pressed) inputs[i].bufferSum= 24; // max bufferSum, no idea why.
    else inputs[i].bufferSum= 0;
  }

  // DIP Setup

  for (int i = 0; i < 4; i++) {
    pinMode(dipPins[i], INPUT);
    digitalWrite(dipPins[i], HIGH);
  }

  // Sysex

  Firmata.attach(START_SYSEX, sysexCallback);
  
}

void loop() {

  while (Firmata.available()) {
    Firmata.processInput();
  }

  if (address() == MOON) lightMoon();
  else{
    updateBuffers();
    updateStates();
    updateIndices();
  }

  // send heartbeat every 2 sec to let python know we're not dead
  if (millis() > lastBeatTime + 2000){
    // heartbeat consists of identification message
    heartbeat();
    lastBeatTime= millis();
  }
  
  forceDelay();
}

//
// Self-Identify
//

void identify() {
  byte returnData[1];

  returnData[0] = (byte) address();

  Firmata.sendSysex(SELF_IDENTIFY, 1, returnData);
}

void heartbeat(){
  byte returnData[1];

  returnData[0] = (byte) address();

  Firmata.sendSysex(HEARTBEAT, 1, returnData);
}

//
// Get DIP address
//

int address() {
  int address = 0;
  for (int i = 0; i < 4; i++) {
    address = (address << 1) | !digitalRead(dipPins[i]);
  }
  return address;
}

//
// Check pins and update filter buffer
//

void updateBuffers() {

  for (int i = 0; i < INPUT_COUNT; i++) {

    byte currentByte = inputs[i].buffer[byteIndex];

    int currentValue = digitalRead(inputs[i].pinNumber);

    inputs[i].bufferSum -= (currentByte >> bitIndex) & 0x01;
    inputs[i].bufferSum += currentValue;

    if (currentValue) {
      currentByte |= (1 << bitIndex);
    }
    else {
      currentByte &= ~(1 << bitIndex);
    }

    inputs[i].buffer[byteIndex] = currentByte;
  }

}

//
// Look at thresholds and send key presses if needed
//

void updateStates() {

  byte returnData[4];

  for (int i = 0; i < INPUT_COUNT; i++) {

    // check for release
    if (inputs[i].pressed) {
      if (inputs[i].bufferSum < releaseThreshold) {
        inputs[i].pressed = false;
        inputs[i].releasedTime = millis();
        inputs[i].releasedBrightness = inputs[i].currentBrightness;

        // python doesn't need to know about releases
        //returnData[0] = (byte) address();
        //returnData[1] = (byte) i;
        //returnData[2] = (byte) inputs[i].pinNumber;
        //returnData[3] = (byte) 0;

        //Firmata.sendSysex(TRIGGER_CHANGE, 4, returnData);
      }
    }
    
    // check for press
    else if (!inputs[i].pressed) {
      if (inputs[i].bufferSum > pressThreshold) { // input becomes pressed
        inputs[i].pressed = true;
        inputs[i].pressedTime = millis();
        inputs[i].pressedBrightness = inputs[i].currentBrightness;

        returnData[0] = (byte) address();
        returnData[1] = (byte) i;
        returnData[2] = (byte) inputs[i].pinNumber;
        returnData[3] = (byte) 1;

        Firmata.sendSysex(TRIGGER_CHANGE, 4, returnData);
      }
    }

    // update LED brightness
    if (inputs[i].ledPin != NULL) {
      
      if (inputs[i].pressed) {       
        unsigned long elapsed = millis() - inputs[i].pressedTime;

        if (elapsed < 10) {
          int value = map( elapsed, 0, 10, inputs[i].pressedBrightness, maxBrightness);
          inputs[i].currentBrightness = value;
          analogWrite(inputs[i].ledPin, value);
        } else if (elapsed < 750) {
          int value = map( elapsed, 10, 750, maxBrightness, minBrightness);
          inputs[i].currentBrightness = value;
          analogWrite(inputs[i].ledPin, value);
        } else {
          inputs[i].currentBrightness = minBrightness;
          analogWrite(inputs[i].ledPin, minBrightness);
        }

      } else {
        unsigned long elapsed = millis() - inputs[i].releasedTime;

        if (elapsed < 250) {
          int value = map( elapsed, 0, 250, inputs[i].releasedBrightness, 0.0);
          inputs[i].currentBrightness = value;
          analogWrite(inputs[i].ledPin, value);
        } else {
          inputs[i].currentBrightness = 0;
          analogWrite(inputs[i].ledPin, 0);
        }
      }
    }
  }
}

//
// Update buffer indices
//

void updateIndices() {
  bitIndex++;

  if (bitIndex == 8) {
    bitIndex = 0;
    byteIndex++;
    if (byteIndex == BUFFER_LENGTH) {
      byteIndex = 0;
    }
  }
}

//
// Moon uses all ports to drive LEDs
//


void lightMoon() {
  // fade target
  if (millis() > lastMoonFadeTime + 10){
      targetMoonBrightness -= 0.25;
      if (targetMoonBrightness < minMoonBrightness) targetMoonBrightness= minMoonBrightness;
      lastMoonFadeTime= millis();
    }

  // chase target if not close enough
  if (abs(currentMoonBrightness - targetMoonBrightness) > 1.0) {
    if (currentMoonBrightness > targetMoonBrightness) {
      currentMoonBrightness -= 0.5;
    } else {
      currentMoonBrightness += 0.025;
    }  
  }
  
  setMoonBrightness( constrain( currentMoonBrightness, minMoonBrightness, 255 ) );
  
}

void setMoonBrightness(int b){
  for (int i = 0; i < INPUT_COUNT; i++) {
      analogWrite(inputs[i].ledPin,  b);
  }
}

//
// Make sure each loop lasts at least TARGET_LOOP_TIME microseconds
//

void forceDelay() {

  loopTime = micros() - previousTime;
  if (loopTime < TARGET_LOOP_TIME) {
    delayMicroseconds(TARGET_LOOP_TIME - loopTime);
  }

  previousTime = micros();

}


