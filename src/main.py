# imports
import pygame
import sys
from pygame.locals import *
from storage import *
from helpers import *
from states import *

# main inits / configs
pygame.init()
pygame.display.set_caption("Floppy Bird : Rebirth")
pygame.display.set_icon(pygame.image.load(S.ASSETS_PATH + "images/icon.png"))
pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
S.WINDOW = pygame.display.set_mode(S.WINDOW_SIZE)
S.WINDOW.fill((0, 0, 0))

S.save_sprite("BACKGROUND", load_image(S.ASSETS_PATH + "images/background.png"))
S.save_sprite("FLOOR", load_image(S.ASSETS_PATH + "images/floor.png"))

load_state("menu")
