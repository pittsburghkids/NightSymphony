import pyfirmata
import pygame
import serial
import time
import glob

#
# Sound Setup
# 

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
pygame.mixer.set_num_channels(18);

#
# Voices
# 

class Voice():
  def __init__(self, id, samplePath):
    self.samplePath = samplePath
    self.channel = pygame.mixer.Channel(id);
    self.sample = pygame.mixer.Sound(samplePath);
  def play(self):
    print self.samplePath
    self.channel.play(self.sample);
  def isPlaying(self):
    return self.channel.get_busy();

voices = {}

voices[(0,0)] = Voice(0, 'samples/bells/bells.plastic.ff.C6B6006.wav')
voices[(0,1)] = Voice(1, 'samples/insects/moth.wav')
voices[(0,2)] = Voice(2, 'samples/bells/bells.plastic.ff.C6B6001.wav')

voices[(1,0)] = Voice(3, 'samples/bells/bells.plastic.ff.C6B6005.wav')
voices[(1,1)] = Voice(4, 'samples/insects/spittle.wav')
voices[(1,2)] = Voice(5, 'samples/bells/bells.plastic.ff.C6B6003.wav')
voices[(1,3)] = Voice(6, 'samples/bells/bells.plastic.ff.C5B5011.wav')

voices[(2,0)] = Voice(7, 'samples/insects/cricket_1.wav')
voices[(2,1)] = Voice(8, 'samples/insects/cricket_2.wav')

voices[(3,0)] = Voice(9, 'samples/bells/bells.plastic.ff.C5B5010.wav')
voices[(3,1)] = Voice(10, 'samples/insects/dragonfly.wav')
voices[(3,2)] = Voice(11, 'samples/insects/mosquito_1.wav')
voices[(3,3)] = Voice(12, 'samples/insects/bee.wav')
voices[(3,4)] = Voice(13, 'samples/insects/mosquito_2.wav')

voices[(4,0)] = Voice(14, 'samples/insects/mosquito_3.wav')
voices[(4,1)] = Voice(15, 'samples/insects/cidada.wav')
voices[(4,2)] = Voice(16, 'samples/bells/bells.plastic.ff.C5B5008.wav')
voices[(4,3)] = Voice(17, 'samples/bells/bells.plastic.ff.C5B5006.wav')

moonBoard = 2;

#
# Board Containers
#


boards = list()

#
# Board Setup
# 

class CustomBoard(pyfirmata.Board):
  def __init__(self, port, layout=None, baudrate=57600, name=None, timeout=None):
    self.sp = serial.Serial(port, baudrate, timeout=timeout)
    self.name = name
    self.isMoon = False;
    if not self.name:
      self.name = port    

    self._command_handlers = {}

    self.add_cmd_handler(0xb0, self._handle_trigger)
    self.add_cmd_handler(0xa0, self._handle_identify)
    self.add_cmd_handler(0xa2, self._handle_echo)     

    def __str__(self):
        return "Board {0.name} on {0.sp.port}".format(self)

  def _handle_identify(self, *data):
    address = data[0];
    print "Board Identified: " + str(address)
    print self

    if address == moonBoard:
      print "Moon detected"
      self.isMoon = True;

  def _handle_echo(self, *data):
    print "ECHO"
    print data

  def _handle_trigger(self, *data):
    print self

    address = data[0];
    id = data[2];
    pin = data[4];
    status = data[6];
    print data
    if (status == 1 and (address,id) in voices):
      voices[address,id].play();

#
# Board Detection
# 

print "Detecting Boards"

ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/cu.usbmodem*')
for port in ports:
  newBoard = CustomBoard(port, None)
  print newBoard

  boards.append(newBoard);

#
# Main Loop
#

activeVoiceCount = 0
lastActiveVoiceCount = 0

while True:

  # Process Voices

  activeVoiceCount = 0

  for key, voice in voices.iteritems():
    if voice.isPlaying():
      activeVoiceCount += 1

  # Process Board Data

  for board in boards:

    # Process input

    while board.bytes_available():
      board.iterate();

    # Handle the moon

    if board.isMoon:
      if (activeVoiceCount != lastActiveVoiceCount):
        dataOut = bytearray([activeVoiceCount, len(voices)])
        boards[0].send_sysex(0xa1, dataOut)     
    
    # Quick sleep

    time.sleep(0.001);  

  lastActiveVoiceCount = activeVoiceCount
