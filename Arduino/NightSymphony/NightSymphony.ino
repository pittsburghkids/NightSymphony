#include <Firmata.h>

#define INPUT_COUNT 6
#define BUFFER_LENGTH 3
#define TARGET_LOOP_TIME 744

#define SELF_IDENTIFY 0xa0
#define TRIGGER_CHANGE 0xb0


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
float fadeDownStep = .1;

typedef struct {
  byte pinNumber;

  byte ledPin;

  float fadeValue = 0;
  float fadeTarget = 0;

  byte buffer[BUFFER_LENGTH];
  byte bufferSum;
  boolean pressed;
  boolean active;
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
    inputs[i].pressed = false;
    for (int j = 0; j < BUFFER_LENGTH; j++) {
      inputs[i].buffer[j] = 0;
    }

    // Do we need a delay here?
     
    if (digitalRead(inputPins[i]) == LOW) {
      inputs[i].active = true;
    } else {
      inputs[i].active = false;
    }

  }

  // DIP Setup

  for (int i = 0; i < 4; i++) {
    pinMode(dipPins[i], INPUT);
    digitalWrite(dipPins[i], HIGH);
  }
  
  // Self Identify

  identify();
}

void loop() {

  while (Firmata.available()) {
    Firmata.processInput();
  }

  updateBuffers();
  updateStates();
  updateIndices();
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
    if (inputs[i].active == false) continue;
    
    byte currentByte = inputs[i].buffer[byteIndex];

    int currentValue = digitalRead(inputs[i].pinNumber);
    //currentValue = !currentValue;

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

    if (inputs[i].active == false) continue;
    
    if (inputs[i].pressed) {
      if (inputs[i].bufferSum < releaseThreshold) {
        inputs[i].pressed = false;

        returnData[0] = (byte) address();
        returnData[1] = (byte) i;
        returnData[2] = (byte) inputs[i].pinNumber;
        returnData[3] = (byte) 0;

        Firmata.sendSysex(TRIGGER_CHANGE, 4, returnData);

        inputs[i].fadeTarget = 0;
      }

    }
    else if (!inputs[i].pressed) {

      if (inputs[i].bufferSum > pressThreshold) { // input becomes pressed
        inputs[i].pressed = true;

        returnData[0] = (byte) address();
        returnData[1] = (byte) i;
        returnData[2] = (byte) inputs[i].pinNumber;
        returnData[3] = (byte) 1;

        Firmata.sendSysex(TRIGGER_CHANGE, 4, returnData);

        inputs[i].fadeTarget = 255;

      }
    }

    if (inputs[i].ledPin != NULL) {
      if (inputs[i].fadeValue != inputs[i].fadeTarget) {
        if (inputs[i].fadeValue < inputs[i].fadeTarget) {
          inputs[i].fadeValue = constrain(inputs[i].fadeValue + fadeUpStep, 0, 255);
          analogWrite(inputs[i].ledPin, inputs[i].fadeValue);
        }

        if (inputs[i].fadeValue > inputs[i].fadeTarget) {
          inputs[i].fadeValue = constrain(inputs[i].fadeValue - fadeDownStep, 0, 255);
          analogWrite(inputs[i].ledPin, inputs[i].fadeValue);
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
// Make sure each loop lasts at least TARGET_LOOP_TIME
//

void forceDelay() {

  loopTime = micros() - previousTime;
  if (loopTime < TARGET_LOOP_TIME) {
    delayMicroseconds(TARGET_LOOP_TIME - loopTime);
  }

  previousTime = micros();

}


