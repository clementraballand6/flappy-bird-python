import pygame
from storage import *


def load_image(path):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, (image.get_size()[0] * 3, image.get_size()[1] * 3)).convert_alpha()


def center_coord_x(element):
    return (S.WINDOW.get_size()[0] / 2) - (element.get_size()[0] / 2)


def center_coord_y(element):
    return (S.WINDOW.get_size()[1] / 2) - (element.get_size()[1] / 2)


def clean_scene():
    S.WINDOW.fill((0, 0, 0))
    S.WINDOW.blit(S.BACKGROUND, (0, 0))
    S.WINDOW.blit(S.FLOOR, (0, S.BACKGROUND.get_size()[1] - S.FLOOR.get_size()[1]))