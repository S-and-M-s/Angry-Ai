import sys
from single_player import player_loop
from ai import run
import pygame
import os
class Game:
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY ,self.ENTER_KEY,self.K_SPACE= False, False, False, False,False,False
        self.DISPLAY_W, self.DISPLAY_H = 576, 800
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = '../assets/fonts/8-BITWONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY ,self.ESCAPE_KEY= False, False, False, False,False
    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (round(x),round(y))
        self.display.blit(text_surface,text_rect)
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)
    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 100
        self.botx, self.boty = self.mid_w, self.mid_h + 150
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 200
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 250
        self.cursor_rect.midtop = (round(self.startx + self.offset),round( self.starty))
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("BOT Game", 20, self.botx, self.boty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop =(round(self.botx + self.offset),round(self.boty))
                self.state = 'BOT Game'
            elif self.state == 'BOT Game':
                self.cursor_rect.midtop = (round(self.optionsx + self.offset), round(self.optionsy))
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (round(self.creditsx + self.offset), round(self.creditsy))
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (round(self.startx + self.offset), round(self.starty))
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (round(self.creditsx + self.offset), round(self.creditsy))
                self.state = 'Credits'
            elif self.state == 'BOT Game':
                self.cursor_rect.midtop = (round(self.startx + self.offset), round(self.starty))
                self.state = 'Start'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (round(self.botx+ self.offset),round(self.boty))
                self.state = 'BOT Game'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (round(self.optionsx + self.offset), round(self.optionsy))
                self.state = 'Options'
    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                player_loop()
                if self.game.BACK_KEY:
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
                    sys.exit()
                # to close the game and return to the menu
                if self.game.BACK_KEY:
                    self.run_display = False
                    pygame.quit()
                    quit()
                    sys.exit()
                # to finish the game
                if self.game.ESCAPE_KEY:
                    self.game.curr_menu = self.game.main_menu
                    self.run_display = False
            elif self.state == 'BOT Game':
                if self.run_display:
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, 'config-feedforward.txt')
                    run(config_path)
                    # to close the game and return to the menu
                    if self.game.K_SPACE:
                        pygame.quit()
                        quit()
                        sys.exit()
                        self.game.curr_menu = self.game.main_menu
                        self.run_display = False
                    # to finish the game
                    if self.game.ESCAPE_KEY:
                        self.run_display = False
                        # pygame.quit()
                        # quit()
                        self.game.curr_menu = self.game.main_menu
                        # sys.exit()

            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (round(self.volx + self.offset),round(self.voly))
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Options', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()
    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (round(self.controlsx + self.offset), round(self.controlsy))
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (round(self.volx + self.offset), round(self.voly))
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass
class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Mais Jamil', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
            self.game.draw_text('Saed alkhtib', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 80)
            self.game.draw_text('Mohammed Ghafri', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 110)
            self.game.draw_text('Mohamad Sheikh Alshabab', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 140)
            self.blit_screen()
if __name__ == "__main__":
    g = Game()
    while g.running:
        g.curr_menu.display_menu()
