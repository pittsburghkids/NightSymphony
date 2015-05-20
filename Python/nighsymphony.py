import pyfirmata
import pygame
import serial
from time import sleep
import glob

# Sound Setup

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16);

# Voices

Voices = {}

Voices[(0,0)] = pygame.mixer.Sound('samples/bells/bells.plastic.ff.C5B5001.wav')
Voices[(1,5)] = pygame.mixer.Sound('samples/bells/bells.plastic.ff.C5B5003.wav')

# Board Setup

layout =  {
        'digital': tuple(x for x in range(14)),
        'analog': tuple(x for x in range(6)),
        'pwm': (3, 5, 6, 9, 10, 11),
        'use_ports': False,
        'disabled': (0, 1)  # Rx, Tx, Crystal
}

print "Configuring Boards"

class MyBoard(pyfirmata.Board):
	def __init__(self, port, layout=None, baudrate=57600, name=None, timeout=None):
		self.sp = serial.Serial(port, baudrate, timeout=timeout)
		self.name = name
		if not self.name:
			self.name = port		

	def _handle_trigger(self, *data):
		address = data[0];
		id = data[2];
		pin = data[4];
		status = data[6];
		print data
		if (status == 1 and (address,id) in Voices):
			Voices[address,id].play();

ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/cu.usbmodem*')
for port in ports:
	print "New Board: " + port
	my_board = MyBoard(port, None)
	my_board.add_cmd_handler(0xb0, my_board._handle_trigger)
	it = pyfirmata.util.Iterator(my_board)
	it.start()
