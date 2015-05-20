import pyfirmata
from pyfirmata import util
import pygame

pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()
sample = pygame.mixer.Sound('samples/bells/bells.plastic.ff.C5B5001.wav')

arduinoBoard =  {
        'digital': tuple(x for x in range(14)),
        'analog': tuple(x for x in range(6)),
        'pwm': (3, 5, 6, 9, 10, 11),
        'use_ports': True,
        'disabled': (0, 1)  # Rx, Tx, Crystal
}

class MyBoard(pyfirmata.Board):
    def _handle_i2c(self, *data):
    	address = data[0];
    	id = data[2];
    	pin = data[4];
    	status = data[6];
    	sample.play();

my_board = MyBoard('/dev/cu.usbmodemfd121', arduinoBoard)
my_board.add_cmd_handler(0xb0, my_board._handle_i2c)

it = util.Iterator(my_board)
it.start()
