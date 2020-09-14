import sys
import pygame
import os

mainClock = pygame.time.Clock() # Times in pygame are represented in milliseconds (1/1000 seconds).
from pygame.locals import * # This module contains various constants used by pygame. Its contents are automatically placed in the pygame module namespace. However, an application can use pygame.locals to include only the pygame constants with a from pygame.locals import *.

pygame.init()
pygame.display.set_caption('Angry AI')  # Set the current window caption
screen = pygame.display.set_mode((576, 900), 0, 32)
pygame.display.flip() # Update the full display Surface to the screen

font = pygame.font.SysFont(None, 50)  # create a Font object from the system fonts

bg_img = pygame.transform.scale(pygame.image.load(os.path.join("../assets/images", "bg.png")).convert_alpha(), (576, 700))
# convert_alpha() change the pixel format of an image including per pixel alphas

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)  # The font module allows for rendering TrueType fonts into a new Surface object.
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False

def main_menu():
    while True:

        # screen.fill((0, 0, 0))
        draw_text('main menu', font, (255, 255, 255), screen, 180, 20)

        mx, my = pygame.mouse.get_pos() # get the mouse cursor position.
        button_1 = pygame.Rect(50, 100, 200, 50) # Pygame uses Rect objects to store and manipulate rectangular areas.
        draw_text('Play', font, (255, 255, 255), screen,60, 160)

        button_2 = pygame.Rect(300, 100, 200, 50)
        draw_text('BOT Play', font, (255, 255, 255), screen, 310, 160)

        if button_1.collidepoint((mx, my)):
            if click:
                game()

        if button_2.collidepoint((mx, my)):
            if click:
                options()

        pygame.draw.rect(screen, (255, 0, 0), button_1)
        pygame.draw.rect(screen, (255, 0, 0), button_2)


        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)
        screen.blit(bg_img, (0, 0))


def game():
    running = True
    while running:
        # screen.fill((0, 0, 0))

        draw_text('You Play Game', font, (255, 255, 255), screen, 20, 20)
        draw_text("PRESS ", font, (255, 255, 255), screen, 200, 180)
        draw_text("UP_ARROW KEY", font, (25, 100, 255), screen, 150, 250)
        draw_text("/\\", font, (25, 100, 255), screen, 80, 230)
        draw_text("|", font, (25, 100, 255), screen, 85, 250)
        draw_text("TO START PLAY", font, (255, 255, 255), screen, 150, 320)
        draw_text("PRESS", font, (255, 255, 255), screen, 10, 520)
        draw_text("ESC", font, (25, 100, 255), screen, 10, 560)
        draw_text("TO BACK TO MAIN MENU", font, (255, 255, 255), screen, 10, 600)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit() # function is sort of the opposite of the pygame. init() function: it runs code that deactivates the Pygame library.
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    os.system("one_player.py")

        pygame.display.update() # Update portions of the screen for software displays
        screen.blit(bg_img, (0, 0)) # draw one image onto another
        mainClock.tick(60) # update the clock tick(framerate=0) -> milliseconds


def options():
    running = True
    while running:
        # screen.fill((0, 0, 0))


        draw_text('BOT Play Game', font, (255, 255, 255), screen, 20, 20)
        draw_text("PRESS ", font, (255, 255, 255), screen, 200, 180)
        draw_text("DOWN_ARROW KEY", font, (25, 100, 255), screen, 150, 250)
        draw_text("|", font, (25, 100, 255), screen, 85, 230)
        draw_text("\/", font, (25, 100, 255), screen, 80, 250)
        draw_text("TO START PLAY", font, (255, 255, 255), screen, 150, 320)
        draw_text("PRESS", font, (255, 255, 255), screen, 10, 520)
        draw_text("ESC", font, (25, 100, 255), screen, 10, 560)
        draw_text("TO BACK TO MAIN MENU", font, (255, 255, 255), screen, 10, 600)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            if event.type == KEYDOWN:
                if event.key == pygame.K_DOWN:
                    os.system("main.py")

        pygame.display.update()
        # os.system("one_player.py")
        mainClock.tick(60)
        screen.blit(bg_img, (0, 0))


main_menu()
