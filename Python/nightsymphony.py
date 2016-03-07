import pyfirmata
import pygame
import serial
import time
import glob
from sys import argv
import os
import fcntl
import subprocess

#
# Sound Setup
# 

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(18)

#
# Voices
# 

class Voice():
  def __init__(self, id, samplePath):
    self.samplePath = samplePath
    self.channel = pygame.mixer.Channel(id)
    self.sample = pygame.mixer.Sound(samplePath)
    self.triggered = False
  def play(self):
      #print self.samplePath
    self.channel.play(self.sample)
    self.triggered = True
  def isPlaying(self):
    return self.channel.get_busy()

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

moonBoard = 5

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
    self.isMoon = False
    self.lastHeartbeat = time.clock() + 10 # assume board will live for at least 10 seconds
    if not self.name:
      self.name = "?"

    self._command_handlers = {}

    self.add_cmd_handler(0xb0, self._handle_trigger)
    self.add_cmd_handler(0xa0, self._handle_identify)
    self.add_cmd_handler(0xa2, self._handle_echo)
    self.add_cmd_handler(0xa3, self._handle_heatbeat)

  def __str__(self):
    return "Board " + str(self.name) + " on " + str(self.sp.port)

  def _handle_identify(self, *data):
    address = data[0]
    log( "Board " + str(address) + " Identified (" + str(self.sp.port) + ")" )
    
    self.name = address

    if address == moonBoard:
      log( "Moon detected" )
      self.isMoon = True

  def _handle_echo(self, *data):
    log( "ECHO" )
    log( str(data) )

  def _handle_trigger(self, *data):
    if ( len(data) != 8 ):
      log("Board " + str(self.name) + " (" + str(self.sp.port) + "): ")
      log("Error on trigger handle, missing data. Expected 8 bytes")
      msg= "Data (Length = " + str(len(data)) + "): "
      for d in data:
        msg+= str(d) + ", "
      log(msg)
    else:
      address = data[0]
      id = data[2]
      pin = data[4]
      status = data[6]
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

  def _handle_heatbeat(self, *data):
    self.lastHeartbeat= time.clock()

  def isDead(self):
    # heatbeats happen every 2 secons. If we miss two, the board must be dead
    if ( time.clock() > self.lastHeartbeat + 5 ): return True
    else: return False




# The following arduino reset stuff was stolen from Paul Furtado: https://gist.github.com/PaulFurtado/fce98aef890469f34d51

# Equivalent of the _IO('U', 20) constant in the linux kernel.
USBDEVFS_RESET = ord('U') << (4*2) | 20
  
def get_arduinos():
  """
  Gets the devfs path to an Arduino microcontroller by scraping the output
  of the lsusb command
        
  The lsusb command outputs a list of USB devices attached to a computer
  in the format:
  Bus 002 Device 009: ID 16c0:0483 Van Ooijen Technische Informatica Teensyduino Serial
  The devfs path to these devices is:
  /dev/bus/usb/<busnum>/<devnum>
  So for the above device, it would be:
  /dev/bus/usb/002/009
  This function generates that path.
  """
  proc = subprocess.Popen(['lsusb'], stdout=subprocess.PIPE)
  out = proc.communicate()[0]
  lines = out.split('\n')
  arduinos= list()
  for line in lines:
    if 'Arduino' in line:
      parts = line.split()
      bus = parts[1]
      dev = parts[3][:3]
      arduinos.append( '/dev/bus/usb/%s/%s' % (bus, dev) )
  return arduinos
  
def send_reset(dev_path):
  """
    Sends the USBDEVFS_RESET IOCTL to a USB device.
    dev_path - The devfs path to the USB device (under /dev/bus/usb/)
    See get_teensy for example of how to obtain this.
  """
  fd = os.open(dev_path, os.O_WRONLY)
  try:
    fcntl.ioctl(fd, USBDEVFS_RESET, 0)
  finally:
    os.close(fd)


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
      log( "Board detection error (" + str(port) + "): " + str(e) )
    else:
      log( str(newBoard) )
      boards.append(newBoard)

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
      log( "Error sending identify request to board " + str(board.address) +  ": " + str(e) )


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

  newVoice = False
  activeVoiceCount = 0

  for key, voice in voices.iteritems():
    if voice.triggered:
      newVoice = True
      voice.triggered = False
    if voice.isPlaying():
      activeVoiceCount += 1

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

    # check for board death
    if ( board.isDead() ):
      log("Board " + str(board.name) + " (" + str(board.sp.port) + ") Dead")
      # reset arduinos
      arduinos= get_arduinos()
      for arduino in arduinos:
        log( "Resetting arduino at " + str(arduino) )
        send_reset(arduino)
      detectBoards()


    # Quick sleep
    time.sleep(0.001)


  if currentError != oldError:
    log( currentError )

