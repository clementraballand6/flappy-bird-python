import pygame
import sys
import time
import random
from pygame.locals import *
from helpers import *
from storage import *

clock = pygame.time.Clock()


def load_state(state):
    globals()[state.title()].run()


def default_events(evt):
    if evt.type == pygame.QUIT:
        pygame.quit()
        sys.exit()


class Menu:

    @staticmethod
    def init():
        clean_scene()

        pygame.mixer.music.stop()
        pygame.mixer.music.load(S.ASSETS_PATH + "menu.mp3")
        pygame.mixer.music.play(-1)

        S.save_sprite("BIRD", load_image(S.ASSETS_PATH + "images/bird-normal.png"))
        S.BIRD_RECT.x = center_coord_x(S.BIRD)
        S.BIRD_RECT.y = S.WINDOW_SIZE[1] - S.FLOOR_RECT.height - S.BIRD_RECT.height

        S.save_sprite("TITLE", load_image(S.ASSETS_PATH + "images/title.png"))
        S.TITLE_RECT.x = center_coord_x(S.TITLE)
        S.TITLE_RECT.y = S.WINDOW.get_size()[1] / 3

        S.save_sprite("PLAY", load_image(S.ASSETS_PATH + "images/play.png"))
        S.PLAY = S.PLAY.convert_alpha()
        S.PLAY_RECT.x = center_coord_x(S.PLAY)
        S.PLAY_RECT.y = (S.WINDOW.get_size()[1] / 2) - (S.PLAY_RECT.height / 2) + 100

        S.WINDOW.blit(S.TITLE, S.TITLE_RECT)
        S.WINDOW.blit(S.PLAY, S.PLAY_RECT)
        S.WINDOW.blit(S.BIRD, S.BIRD_RECT)
        pygame.display.flip()

    @staticmethod
    def blink_text(inverse=True):
        color1 = 0
        color2 = 255
        if inverse:
            color1 = 255
            color2 = 0
        writer = pygame.font.SysFont("monospace", 25)
        warn = writer.render("WARNING \!/", 1, (255, color1, 0))
        songs = writer.render("HUGE SONGS INCOMING", 1, (255, color2, 0))
        best_score = writer.render("BEST SCORE : " + str(Play.best_score), 1, (255, color1, 0))
        S.WINDOW.blit(warn, ((S.WINDOW.get_size()[0] / 2) - (warn.get_rect().width / 2), 100))
        S.WINDOW.blit(songs, ((S.WINDOW.get_size()[0] / 2) - (songs.get_rect().width / 2), 150))
        S.WINDOW.blit(best_score, ((S.WINDOW.get_size()[0] / 2) - (best_score.get_rect().width / 2), 200))
        pygame.display.flip()

    @staticmethod
    def loop():
        t = time.time()
        nb = 0
        running = True
        while running:
            if time.time() > t + 0.75:
                t = time.time()
                nb += 1
                Menu.blink_text(nb % 2)
            for evt in pygame.event.get():
                default_events(evt)
                if evt.type == pygame.MOUSEBUTTONDOWN:
                    x, y = evt.pos
                    if S.PLAY_RECT.collidepoint(x, y):
                        Menu.on_play_clicked()
                        running = False

        Play.run()

    @staticmethod
    def items_reach_borders():
        return S.TITLE_RECT.y < 0 - S.TITLE_RECT.size[1]

    @staticmethod
    def on_play_clicked():
        while True:
            for evt in pygame.event.get():
                default_events(evt)

            clean_scene()

            S.TITLE_RECT.move_ip(0, -1)
            S.PLAY_RECT.move_ip(1, 0)

            S.WINDOW.blit(S.TITLE, S.TITLE_RECT)
            S.WINDOW.blit(S.PLAY, S.PLAY_RECT)
            S.WINDOW.blit(S.BIRD, S.BIRD_RECT)

            pygame.display.flip()
            if Menu.items_reach_borders():
                return

    @staticmethod
    def run():
        Menu.init()
        Menu.loop()


class Play:
    v = 8
    is_jump = False
    is_playground_running = False
    is_playground_inited = False
    best_score = 0
    current_score = 0

    @staticmethod
    def init():
        pygame.mixer.music.stop()
        pygame.mixer.music.load(S.ASSETS_PATH + "game.mp3")
        pygame.mixer.music.play(-1)
        Play.draw_bird()
        pygame.display.flip()

    @staticmethod
    def draw_bird():
        S.save_sprite("BIRD", load_image(S.ASSETS_PATH + "images/bird-normal.png"))

        S.BIRD_RECT.x = center_coord_x(S.BIRD)
        S.BIRD_RECT.y = S.WINDOW_SIZE[1] - S.FLOOR_RECT.height - S.BIRD_RECT.height

        S.WINDOW.blit(S.BIRD, S.BIRD_RECT)

    @staticmethod
    def show_score():
        pygame.mixer.music.stop()
        pygame.mixer.music.load(S.ASSETS_PATH + "lost.mp3")
        pygame.mixer.music.play()
        writer = pygame.font.SysFont("monospace", 20)
        try_again = writer.render("TRY AGAIN! PRESS SPACE TO RETRY", 1, (255, 255, 0))
        best_score = writer.render("BEST SCORE : " + str(Play.best_score), 1, (255, 255, 0))
        time.sleep(.5)

        while True:
            for evt in pygame.event.get():
                default_events(evt)
            S.WINDOW.blit(try_again, ((S.WINDOW.get_size()[0] / 2) - (try_again.get_rect().width / 2), 200))
            S.WINDOW.blit(best_score, ((S.WINDOW.get_size()[0] / 2) - (best_score.get_rect().width / 2), 300))
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                return

    @staticmethod
    def draw_number(number):
        if number == 1:
            number = "one"
        if number == 2:
            number = "two"
        if number == 3:
            number = "three"

        S.save_sprite(number.upper(), load_image(S.ASSETS_PATH + "images/" + number + ".png"))

        getattr(S, number.upper() + "_RECT").x = center_coord_x(getattr(S, number.upper()))
        getattr(S, number.upper() + "_RECT").y = center_coord_y(getattr(S, number.upper())) - 100
        S.WINDOW.blit(getattr(S, number.upper()), getattr(S, number.upper() + "_RECT"))

    @staticmethod
    def timer():
        t = time.time()
        nb = 3
        writer = pygame.font.SysFont("monospace", 20)
        while True:
            hint = writer.render("PRESS SPACE TO JUMP", 1, (255, 128, 0))
            S.WINDOW.blit(hint, ((S.WINDOW.get_size()[0] / 2) - (hint.get_rect().width / 2), 100))
            pygame.display.flip()
            for evt in pygame.event.get():
                default_events(evt)
            if time.time() > t + 1:
                if not nb == 0:
                    t = time.time()
                    clean_scene()
                    Play.draw_number(nb)
                    Play.draw_bird()
                    pygame.display.flip()
                nb -= 1
                if nb == -1:
                    return

    @staticmethod
    def init_playground():
        S.save_sprite("PIPE_UP_FIRST", load_image(S.ASSETS_PATH + "images/pipe-up.png"))
        S.save_sprite("PIPE_UP_SECOND", load_image(S.ASSETS_PATH + "images/pipe-up.png"))

        S.PIPE_UP_FIRST_RECT.x = S.WINDOW_SIZE[0]
        S.PIPE_UP_FIRST_RECT.y = S.WINDOW_SIZE[1] - random.randint(250, 295)

        S.PIPE_UP_SECOND_RECT.x = S.WINDOW_SIZE[0] + 300
        S.PIPE_UP_SECOND_RECT.y = S.WINDOW_SIZE[1] - random.randint(250, 295)

        S.WINDOW.blit(S.PIPE_UP_FIRST, S.PIPE_UP_FIRST_RECT)
        S.WINDOW.blit(S.PIPE_UP_SECOND, S.PIPE_UP_SECOND_RECT)

    @staticmethod
    def update_score():
        writer = pygame.font.SysFont("monospace", 25)
        score = writer.render("SCORE : " + str(Play.current_score), 1, (0, 0, 0))
        S.WINDOW.blit(score, ((S.WINDOW.get_size()[0] / 2) - (score.get_rect().width / 2), 250))

    @staticmethod
    def update_playground():
        if not Play.is_playground_inited:
            Play.init_playground()
            Play.is_playground_inited = True

        S.PIPE_UP_FIRST_RECT.move_ip(-13, 0)
        S.PIPE_UP_SECOND_RECT.move_ip(-13, 0)

        if S.PIPE_UP_FIRST_RECT.x < 0 - S.PIPE_UP_FIRST_RECT.width:
            Play.current_score += 1
            S.PIPE_UP_FIRST_RECT.x = S.WINDOW_SIZE[0] + random.randint(-10, 30)
            S.PIPE_UP_FIRST_RECT.y = S.WINDOW_SIZE[1] - random.randint(250, 295)

        if S.PIPE_UP_SECOND_RECT.x < 0 - S.PIPE_UP_SECOND_RECT.width:
            Play.current_score += 1
            S.PIPE_UP_SECOND_RECT.x = S.PIPE_UP_FIRST_RECT.x + 250 + random.randint(-25, 25)
            S.PIPE_UP_SECOND_RECT.y = S.WINDOW_SIZE[1] - random.randint(250, 320)

        S.WINDOW.blit(S.PIPE_UP_FIRST, S.PIPE_UP_FIRST_RECT)
        S.WINDOW.blit(S.PIPE_UP_SECOND, S.PIPE_UP_SECOND_RECT)

    @staticmethod
    def bird_collides():
        return S.PIPE_UP_FIRST_RECT.colliderect(S.BIRD_RECT) or S.PIPE_UP_SECOND_RECT.colliderect(S.BIRD_RECT)

    @staticmethod
    def handle_bird_jump():
        if Play.is_jump:
            m = 2
            if Play.v > 0:
                force = (0.5 * m * (Play.v * Play.v))
            else:
                force = -(0.5 * m * (Play.v * Play.v))

            S.BIRD_RECT.y = S.BIRD_RECT.y - force

            # Change velocity
            Play.v = Play.v - 1

            # If ground is reached, reset variables.
            if S.BIRD_RECT.y >= S.WINDOW_SIZE[1] - S.FLOOR_RECT.height - S.BIRD_RECT.height:
                Play.is_jump = False
                S.BIRD_RECT.y = S.WINDOW_SIZE[1] - S.FLOOR_RECT.height - S.BIRD_RECT.height
                Play.v = 8

    @staticmethod
    def loop():
        run = True
        while run:
            for evt in pygame.event.get():
                default_events(evt)

            keys = pygame.key.get_pressed()
            if keys[K_SPACE]:
                Play.is_jump = True

            clean_scene()
            Play.handle_bird_jump()
            Play.update_score()
            Play.update_playground()
            S.WINDOW.blit(S.BIRD, S.BIRD_RECT)
            pygame.display.flip()
            time.sleep(0.03)
            run = not Play.bird_collides()
            continue

        Play.is_playground_inited = False
        Play.is_jump = False
        Play.v = 8
        if Play.current_score > Play.best_score:
            Play.best_score = Play.current_score

        Play.show_score()
        pygame.mixer.music.stop()
        Play.current_score = 0
        load_state("menu")

    @staticmethod
    def run():
        Play.init()
        Play.timer()
        Play.loop()
