#include <Firmata.h>

#define INPUT_COUNT 6
#define BUFFER_LENGTH 3
#define TARGET_LOOP_TIME 744

#define TRIGGER_CHANGE 0xb0

byte inputPins[INPUT_COUNT] = {
  //3,4,5,6,7,8,9,10,11,12,
  PIN_TO_DIGITAL(A0), PIN_TO_DIGITAL(A1), PIN_TO_DIGITAL(A2),
  PIN_TO_DIGITAL(A3), PIN_TO_DIGITAL(A4), PIN_TO_DIGITAL(A5)
};
byte outputPins[INPUT_COUNT] {
  //NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
  NULL, NULL, NULL,
  NULL, NULL, NULL
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


  Firmata.setFirmwareVersion(FIRMATA_MAJOR_VERSION, FIRMATA_MINOR_VERSION);
  Firmata.attach(START_SYSEX, sysexCallback);
  Firmata.begin(57600);

  for (int i = 0; i < INPUT_COUNT; i++)
  {
    // Input Pins

    pinMode(inputPins[i], INPUT);

    // Setup Inputs

    inputs[i].pinNumber = inputPins[i];
    inputs[i].ledPin = outputPins[i];
    inputs[i].pressed = false;
    for (int j = 0; j < BUFFER_LENGTH; j++) {
      inputs[i].buffer[j] = 0;
    }

  }


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
// Check pins and update filter buffer
//

void updateBuffers() {

  for (int i = 0; i < INPUT_COUNT; i++) {
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

  byte returnData[3];

  for (int i = 0; i < INPUT_COUNT; i++) {

    if (inputs[i].pressed) {
      if (inputs[i].bufferSum < releaseThreshold) {
        inputs[i].pressed = false;

        returnData[0] = (byte) i;
        returnData[1] = (byte) inputs[i].pinNumber;
        returnData[2] = (byte) 0;

        Firmata.sendSysex(TRIGGER_CHANGE, 3, returnData);

        inputs[i].fadeTarget = 0;
      }

    }
    else if (!inputs[i].pressed) {

      if (inputs[i].bufferSum > pressThreshold) { // input becomes pressed
        inputs[i].pressed = true;

        returnData[0] = (byte) i;
        returnData[1] = (byte) inputs[i].pinNumber;
        returnData[2] = (byte) 1;

        Firmata.sendSysex(TRIGGER_CHANGE, 3, returnData);

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





void sysexCallback(byte command, byte argc, byte*argv)
{
  switch(command){
  case 0x01: // LED Blink Command
    if(argc < 3) break;
    byte blink_pin;
    byte blink_count;
    int delayTime;
    blink_pin = argv[0];
    blink_count = argv[1];
    delayTime = argv[2] * 100;

    pinMode(blink_pin, OUTPUT);
    byte i;
    for(i = 0; i < blink_count; i++){
      digitalWrite(blink_pin, true);
      delay(delayTime);
      digitalWrite(blink_pin, false);
      delay(delayTime);
    }
    Firmata.sendSysex(command, argc, argv); // callback
    break;
  }
}
