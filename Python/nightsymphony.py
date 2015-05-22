import pyfirmata
import pygame
import serial
import time
import glob

#
# Sound Setup
# 

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16);

#
# Voices
# 

class Voice():
	def __init__(self, samplePath):
		self.samplePath = samplePath
		self.sample = pygame.mixer.Sound(samplePath);
	def play(self):
		self.sample.play();

Voices = {}

Voices[(0,0)] = Voice('samples/bells/bells.plastic.ff.C5B5001.wav')
Voices[(1,0)] = Voice('samples/bells/bells.plastic.ff.C5B5002.wav')
Voices[(2,0)] = Voice('samples/bells/bells.plastic.ff.C5B5003.wav')

#
# Board Setup
# 

class CustomBoard(pyfirmata.Board):
	def __init__(self, port, layout=None, baudrate=57600, name=None, timeout=None):
		self.sp = serial.Serial(port, baudrate, timeout=timeout)
		self.name = name
		if not self.name:
			self.name = port		

	def _handle_identify(self, *data):
		address = data[0];
		print "Board Identified: " + str(address)

	def _handle_trigger(self, *data):
		address = data[0];
		id = data[2];
		pin = data[4];
		status = data[6];
		print data
		if (status == 1 and (address,id) in Voices):
			Voices[address,id].play();

#
# Board Detection
# 

print "Detecting Boards"

boards = list()
ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/cu.usbmodem*')
for port in ports:
	print "New Board: " + port
	newBoard = CustomBoard(port, None)
	newBoard.add_cmd_handler(0xb0, newBoard._handle_trigger)
	newBoard.add_cmd_handler(0xa0, newBoard._handle_identify)
	boards.append(newBoard);

#
# Main Loop
#

while True:

	# Process Board Data

	for board in boards:
		while board.bytes_available():
			board.iterate();
		time.sleep(0.001);