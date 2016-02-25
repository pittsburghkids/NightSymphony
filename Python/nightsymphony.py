import pyfirmata
import pygame
import serial
import time
import glob
from sys import argv
import os

#
# Sound Setup
# 

pygame.mixer.pre_init(44100, -16, 2, 512)
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
    self.triggered = False;
  def play(self):
      #print self.samplePath
    self.channel.play(self.sample);
    self.triggered = True;
  def isPlaying(self):
    return self.channel.get_busy();

voices = {}

voices[(0,5)] = Voice(0, 'samples/bells/bells.plastic.ff.C6B6006.wav')
voices[(0,0)] = Voice(1, 'samples/insects/moth.wav')
voices[(0,3)] = Voice(2, 'samples/bells/bells.plastic.ff.C6B6005.wav')
voices[(0,4)] = Voice(3, 'samples/insects/spittle.wav')

voices[(1,2)] = Voice(4, 'samples/bells/bells.plastic.ff.C6B6001.wav')
voices[(1,0)] = Voice(5, 'samples/bells/bells.plastic.ff.C6B6003.wav')
voices[(1,1)] = Voice(6, 'samples/bells/bells.plastic.ff.C5B5011.wav')

voices[(2,0)] = Voice(7, 'samples/insects/cricket_1.wav')
voices[(2,1)] = Voice(8, 'samples/insects/cricket_2.wav')

voices[(3,4)] = Voice(9, 'samples/bells/bells.plastic.ff.C5B5010.wav')
voices[(3,5)] = Voice(10, 'samples/insects/dragonfly.wav')
voices[(3,1)] = Voice(11, 'samples/insects/mosquito_1.wav')
voices[(3,0)] = Voice(12, 'samples/insects/bee.wav')
voices[(3,3)] = Voice(13, 'samples/insects/mosquito_2.wav')

voices[(4,0)] = Voice(14, 'samples/bells/bells.plastic.ff.C5B5008.wav')
voices[(4,3)] = Voice(15, 'samples/insects/cicada.wav')
voices[(4,1)] = Voice(16, 'samples/bells/bells.plastic.ff.C5B5006.wav')
voices[(4,4)] = Voice(17, 'samples/insects/mosquito_3.wav')

moonBoard = 5;

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
    log( "Board " + str(address) + " Identified (" + str(self) + ")" )
    
    self.name = address

    if address == moonBoard:
      log( "Moon detected" )
      self.isMoon = True

  def _handle_echo(self, *data):
    log( "ECHO" )
    log( str(data) )

  def _handle_trigger(self, *data):
    #print self

    address = data[0];
    id = data[2];
    pin = data[4];
    status = data[6];
    msg= "Trigger: Board " + str(address) + ", Header J" + str(id+1) + ": "
    # headers are numbered 1-6, "id"s are 0-5. "pin"s are arduino digital io pin numbers
    if (status == 1):
        msg+= "On. "
        if ((address,id) in voices):
            msg+= "Playing sample."
            voices[address,id].play()
        else:
            msg+= "No sample defined."
    else:
        msg+= "Off."

    log(msg)


#
# Board Detection
# 

def detectBoards():
  log( "Detecting boards..." )
  boards[:] = [] # clear board list

  # Try to make a board for each port
  ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/cu.usbmodem*')
  for port in ports:
    try:
	newBoard = CustomBoard(port, None)
    except Exception as e:
  	log( "Board detection error: " + str(e) )
    else:
	log( str(newBoard) )
    	boards.append(newBoard);

  # Wait for arduinos to reset if they're gonna
  time.sleep(2)

  log ( "Found " + str(len(boards)) + " board(s). Requesting identifications..." )

  # Request identification from all boards
  # this is only really needed for moon, since it doesn't send anything otherwise
  for board in boards:
    dataOut = bytearray()
    try:
        board.send_sysex(0xa0, dataOut) # 0xa0 == SELF_IDENTIFY
    except Exception as e:
        currentError += "Error sending identify request to board " + str(board.address) +  ": " + str(e)


def log(msg):
    print msg
    if (logging):
        with open(filename, "a", 0) as logfile:
            logfile.write(msg)
            logfile.write("\n")
            logfile.flush()
            os.fsync(logfile.fileno())

#
# Setup
#

filename= ""
logging= False
if (len(argv) < 2):
    print "No log filename parameter give, not logging."
else:
    filename= str(argv[1])
    print "Logging to " + filename
    logging= True

detectBoards()

#
# Main Loop
#

currentError = ""

while True:
    
  # check for missing or new ports
  numPorts = len( glob.glob('/dev/ttyACM*') + glob.glob('/dev/cu.usbmodem*') )
  if numPorts != len(boards):
    log("Board/Port Count Mismatch: " + "%d boards but %d ports" % (len(boards), numPorts))
    detectBoards()

  

  # Process Voices

  newVoice = False;
  activeVoiceCount = 0;

  for key, voice in voices.iteritems():
    if voice.triggered:
      newVoice = True;
      voice.triggered = False;
    if voice.isPlaying():
      activeVoiceCount += 1;

  # Process Board Data

  oldError = currentError
  currentError = ""

  for board in boards:

    # Process input
    try:
        while board.bytes_available():
	    board.iterate()
    except IOError as e:
        currentError += "Board %s: I/O error({0}): {1}\n".format(e.errno, e.strerror) % str(board.name)
        detectBoards()

    # Handle the moon

    if board.isMoon:
      if (newVoice):
        log("Sending moon data")
        dataOut = bytearray([activeVoiceCount, len(voices)])
        try:
            board.send_sysex(0xa1, dataOut) # 0xa1 == SET_BRIGHTNESS
        except Exception as e:
            currentError += "Error on send moon data: " + str(e)
            detectBoards()
    
    # Quick sleep

    time.sleep(0.001);  

  if currentError != oldError:
    log( currentError )

