import os
import sys
import random
import pygame
from menu import *

# initials parameters:
pygame.init()
pygame.mixer.pre_init(frequency=44100,channels=1,buffer=512,size=16)
pygame.display.set_caption("Angry AI")
win_w = 576
win_h = 900
win = pygame.display.set_mode((win_w, win_h))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("", 50)


# Game varibles
gravity = 0.25
global bird_movement
bird_movement = 0
global game_active
game_active = True
score = 0
high_score = 0
game_resumed = False
floor_x = 0

# Game images
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("../assets/images", "pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("../assets/images", "bg.png")).convert_alpha(), (576, 700))
base_img = pygame.transform.scale2x(pygame.image.load("../assets/images/base.png").convert())
bird_up_img = pygame.transform.scale2x(pygame.image.load(os.path.join("../assets/images", "bird1.png")).convert_alpha())
bird_mid_img = pygame.transform.scale2x(pygame.image.load(os.path.join("../assets/images", "bird2.png")).convert_alpha())
bird_down_img = pygame.transform.scale2x(pygame.image.load(os.path.join("../assets/images", "bird3.png")).convert_alpha())
bird_images = [bird_down_img, bird_mid_img, bird_up_img]
bird_index = 2
bird_surface = bird_images[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 300))
# game_over_image
game_over_surface = pygame.transform.scale2x(pygame.image.load("../assets/images/go.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,300))

# Timer for bird's wings
BIRDFLIP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLIP, 200)

# Timer for game over sound
GAMEOVER = pygame.USEREVENT + 2
pygame.time.set_timer(GAMEOVER, 900)
game_over_countdown = 1000

# Timer for creating pipe
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [300,400,500,600,700]

# sounds
flap_sound = pygame.mixer.Sound("../assets/sounds/sfx_wing.wav")
death_sound = pygame.mixer.Sound("../assets/sounds/sfx_hit.wav")
over_sound = pygame.mixer.Sound("../assets/sounds/a.wav")
score_sound = pygame.mixer.Sound("../assets/sounds/sfx_point.wav")
score_sound_countdown = 100

class Pipe:
    def create_pipe():
        random_pipe_position = random.choice(pipe_height)
        bottom_pipe = pipe_img.get_rect(midtop=(700, random_pipe_position))  # first num from where start, position of pipe
        top_pipe = pipe_img.get_rect(midbottom=(700, random_pipe_position - 200))
        return bottom_pipe, top_pipe


    def move_pipe(pipes):
        for pipe in pipes:
            pipe.centerx -= 3
        return pipes


    def draw_pipes(pipes):
        for pipe in pipes:
            if pipe.bottom >= 800 :
                win.blit(pipe_img, pipe)
            elif pipe.top < 800:
                flip_pipe = pygame.transform.flip(pipe_img, True, True)
                win.blit(flip_pipe, pipe)


def draw_floor():
    win.blit(base_img, (floor_x, 600))
    win.blit(base_img, (floor_x + 576, 600))


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 650:
        return False
    return True

class Bird:
    def rotate_bird(bird):
        new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
        return new_bird


    def bird_animation():
        new_bird = bird_images[bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
        return new_bird, new_bird_rect


def font_display(game_state):
    if game_state == "main":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(80, 50))
        win.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(450, 50))
        win.blit(high_score_surface, high_score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255,255))
        score_rect = score_surface.get_rect(center=(288, 50))
        win.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 550))
        win.blit(high_score_surface, high_score_rect)


def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score

def player_loop():
    from menu import Menu
    m = Menu()
    gravity = 0.25
    global bird_movement
    bird_movement = 0
    global game_active
    game_active = True
    score = 0
    high_score = 0
    game_resumed = False
    floor_x = 0

    # Game images
    pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("../assets/images", "pipe.png")).convert_alpha())
    bg_img = pygame.transform.scale(pygame.image.load(os.path.join("../assets/images", "bg.png")).convert_alpha(),
                                    (576, 700))
    base_img = pygame.transform.scale2x(pygame.image.load("../assets/images/base.png").convert())
    bird_up_img = pygame.transform.scale2x(
        pygame.image.load(os.path.join("../assets/images", "bird1.png")).convert_alpha())
    bird_mid_img = pygame.transform.scale2x(
        pygame.image.load(os.path.join("../assets/images", "bird2.png")).convert_alpha())
    bird_down_img = pygame.transform.scale2x(
        pygame.image.load(os.path.join("../assets/images", "bird3.png")).convert_alpha())
    bird_images = [bird_down_img, bird_mid_img, bird_up_img]
    bird_index = 2
    bird_surface = bird_images[bird_index]
    bird_rect = bird_surface.get_rect(center=(100, 300))
    # game_over_image
    game_over_surface = pygame.transform.scale2x(pygame.image.load("../assets/images/download.png").convert_alpha())
    game_over_rect = game_over_surface.get_rect(center=(288, 300))

    # Timer for bird's wings
    BIRDFLIP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLIP, 200)

    # Timer for game over sound
    GAMEOVER = pygame.USEREVENT + 2
    pygame.time.set_timer(GAMEOVER, 900)
    game_over_countdown = 1000

    # Timer for creating pipe
    pipe_list = []
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 1200)
    pipe_height = [300, 400, 500, 600, 700]

    # sounds
    flap_sound = pygame.mixer.Sound("assets/sounds/sfx_wing.wav")
    death_sound = pygame.mixer.Sound("assets/sounds/sfx_hit.wav")
    over_sound = pygame.mixer.Sound("assets/sounds/a.wav")
    score_sound = pygame.mixer.Sound("assets/sounds/sfx_point.wav")
    score_sound_countdown = 100
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = 0
                    bird_movement -= 3
                    game_resumed = True
                    flap_sound.play()

                # to finish the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_resumed = False
                        pygame.quit()
                        quit()
                        break
                # to back to main menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        game_resumed = False


                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, 350)
                    bird_movement = 0
                    score = 0
                    over_sound.stop()

                if event.key == pygame.K_UP:
                    bird_movement = 0
                    bird_movement -= 6
                    flap_sound.play()
                    game_resumed = True

            if event.type == SPAWNPIPE:
                pipe_list.extend(Pipe.create_pipe())

            if event.type == BIRDFLIP:
                if bird_index < 2:
                    bird_index += 1
                else:
                    bird_index = 0
                bird_surface, bird_rect = Bird.bird_animation()

        win.blit(bg_img, (0, 0))

        if game_active:
            bird_movement += gravity
            rotated_bird = Bird.rotate_bird(bird_surface)
            bird_rect.centery += bird_movement
            win.blit(rotated_bird, bird_rect)
            game_active = check_collision(pipe_list)
            pipe_list = Pipe.move_pipe(pipe_list)
            Pipe.draw_pipes(pipe_list)
            score += 0.01
            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown = 100
            font_display("main")
        else:
            win.blit(game_over_surface,game_over_rect)
            high_score = update_score(score,high_score)
            if event.type == GAMEOVER:
                if game_over_countdown < 1000:
                    over_sound.play()
                    game_over_countdown += 100

                else:
                    game_over_countdown = 1000
                    over_sound.stop()

            font_display("game_over")

        floor_x -= 1
        draw_floor()
        if floor_x <= -576:
            floor_x = 0

        pygame.display.update()
        clock.tick(120)

if __name__ == "__main__":
    player_loop()

#  import os
# import sys
# import random
# import pygame

# # initials parameters:
# pygame.init()
# pygame.mixer.pre_init(frequency=44100,channels=1,buffer=512,size=16)
# pygame.display.set_caption("Angry AI")
# win_w = 576
# win_h = 900
# win = pygame.display.set_mode((win_w, win_h))
# clock = pygame.time.Clock()
# game_font = pygame.font.SysFont("", 50)


# # Game varibles
# gravity = 0.25
# bird_movement = 0
# game_active = True
# score = 0
# high_score = 0
# game_resumed = False
# floor_x = 0

# # Game images
# pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "pipe.png")).convert_alpha())
# bg_img = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "bg.png")).convert_alpha(), (576, 700))
# base_img = pygame.transform.scale2x(pygame.image.load("assets/images/base.png").convert())
# bird_up_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird1.png")).convert_alpha())
# bird_mid_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird2.png")).convert_alpha())
# bird_down_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "bird3.png")).convert_alpha())
# bird_images = [bird_down_img, bird_mid_img, bird_up_img]
# bird_index = 2
# bird_surface = bird_images[bird_index]
# bird_rect = bird_surface.get_rect(center=(100, 300))
# # game_over_image
# game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/images/download.png").convert_alpha())
# game_over_rect = game_over_surface.get_rect(center = (288,300))
# PIP_IMG=pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "pipe.png")))


# # Timer for bird's wings
# BIRDFLIP = pygame.USEREVENT + 1
# pygame.time.set_timer(BIRDFLIP, 200)

# # Timer for game over sound
# GAMEOVER = pygame.USEREVENT + 2
# pygame.time.set_timer(GAMEOVER, 900)
# game_over_countdown = 1000

# # Timer for creating pipe
# pipe_list = []
# SPAWNPIPE = pygame.USEREVENT
# pygame.time.set_timer(SPAWNPIPE, 1200)
# pipe_height = [300,400,500,600,700]

# # sounds
# flap_sound = pygame.mixer.Sound("assets/sounds/sfx_wing.wav")
# death_sound = pygame.mixer.Sound("assets/sounds/sfx_hit.wav")
# over_sound = pygame.mixer.Sound("assets/sounds/a.wav")
# score_sound = pygame.mixer.Sound("assets/sounds/sfx_point.wav")
# score_sound_countdown = 100

# class Pipe:
#     def create_pipe():
#         random_pipe_position = random.choice(pipe_height)
#         bottom_pipe = pipe_img.get_rect(midtop=(700, random_pipe_position))  # first num from where start, position of pipe
#         top_pipe = pipe_img.get_rect(midbottom=(700, random_pipe_position - 200))
#         # print("This top and bottom",bottom_pipe, top_pipe,bottom_pipe.top)
#         return bottom_pipe, top_pipe


#     def move_pipe(pipes):
#         for pipe in pipes:
#             pipe.centerx -= 3
#         return pipes


#     def draw_pipes(pipes):
#         for pipe in pipes:
#             if pipe.bottom >= 800 :
#                 win.blit(pipe_img, pipe)
#             elif pipe.top < 800:
#                 print(pipe.top,pipe.bottom)
#                 flip_pipe = pygame.transform.flip(pipe_img, True, True)
#                 win.blit(flip_pipe, pipe)
#     # GAP = 200
#     # VEL = 5
#     #
#     # def __init__(self, x):
#     #     self.x = x
#     #     self.height = 0
#     #     # self.gap =100
#     #
#     #     self.top = 0
#     #     self.bottom = 0
#     #     self.PIPE_TOP = pygame.transform.flip(PIP_IMG, False, True)
#     #     self.PIP_BOTTOM = PIP_IMG
#     #
#     #     self.passed = False
#     #     self.set_height()
#     #
#     # def set_height(self):
#     #     self.height = random.randrange(50, 450)
#     #     self.top = self.height - self.PIPE_TOP.get_height()
#     #     self.bottom = self.height + self.GAP
#     #
#     # def move(self):
#     #     self.x -= self.VEL
#     #
#     # def draw(self, win):
#     #     # print(win)
#     #     win.blit(self.PIPE_TOP, (self.x, self.top))
#     #     win.blit(self.PIP_BOTTOM, (self.x, self.bottom))
#     #
#     # def collide(self, bird, win):
#     #     bird_mask = bird.get_mask()
#     #     top_mask = pygame.mask.from_surface(self.PIPE_TOP)
#     #     bottom_mask = pygame.mask.from_surface(self.PIP_BOTTOM)
#     #
#     #     top_offset = (self.x - bird.x, self.top - round(bird.y))
#     #     bottom_offset = self.x - bird.x, self.bottom - round(bird.y)
#     #
#     #     b_point = bird_mask.overlap(bottom_mask, bottom_offset)  # bottom point
#     #
#     #     t_point = bird_mask.overlap(top_mask, top_offset)  # top point
#     #
#     #     # check for collision
#     #     if t_point or b_point:
#     #         return True
#     #     else:
#     #         return False


# def draw_floor():
#     win.blit(base_img, (floor_x, 600))
#     win.blit(base_img, (floor_x + 576, 600))


# def check_collision(pipes):
#     # print(pipes)
#     new_pip=[]
#     for i,co in enumerate(pipes):
#         # if  i%2==0:
#         #     bt = (0, co.top )
#         # #     bt=(0,co.top)
#         #     new_pip.append(bt)
#         # #
#         # if not i%2==0:
#         #     to = (0, co.top)
#         # #     to=(0,co.bottom)
#         #     new_pip.append(to)
#         bt = (0, co.top )
#         to=(0,co.bottom)


#         new_pip.append(bt)
#         new_pip.append(to)

#     # print(new_pip)
#     # print(bird.collide(new_pip))
#     # if bird.collide(new_pip):
#     #     death_sound.play()
#     #     return False



#     for pipe in pipes:
#         if bird_rect.colliderect(pipe):
#             death_sound.play()
#             return False
#     if bird_rect.top <= -50 or bird_rect.bottom >= 640:
#         return False
#     return True

# class Bird:
#     IMGS = bird_images
#     def __init__(self):
#         self.img = self.IMGS[0]
#         # 230, 350
#         self.x = 230
#         self.y = 350
#     def rotate_bird(bird):
#         new_bird = pygame.transform.rotozoom(bird, - bird_movement * 3, 1)
#         return new_bird


#     def bird_animation():
#         new_bird = bird_images[bird_index]
#         new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
#         return new_bird, new_bird_rect


#     def get_mask(self):
#         return pygame.mask.from_surface(self.img)


#     def collide(self, pip):
#         bird=Bird()
#         self.GAP = 200
#         self.PIPE_TOP = pygame.transform.flip(PIP_IMG, False, True)
#         self.PIP_BOTTOM = PIP_IMG
#         self.height = random.randrange(50, 450)
#         self.top = self.height - self.PIPE_TOP.get_height()
#         self.bottom = self.height + self.GAP
#         bird_mask = bird.get_mask()
#         top_mask = pygame.mask.from_surface(self.PIPE_TOP)
#         bottom_mask = pygame.mask.from_surface(self.PIP_BOTTOM)

#         top_offset = (self.x - bird.x, self.top - round(bird.y))

#         bottom_offset = self.x - bird.x, self.bottom - round(bird.y)
#         # print(top_offset,"   ",top_mask,"   ",bottom_offset)
#         for x,i in enumerate(pip):
#             if x %2==0:
#                 top_offset=i
#                 print(bottom_offset)
#             if not x%2==0:
#                 bottom_offset=i
#                 print(top_offset)
#                 b_point = bird_mask.overlap(bottom_mask, bottom_offset)  # bottom point

#                 t_point = bird_mask.overlap(top_mask, top_offset)  # top point



#                 # check for collision
#                 if t_point or b_point:
#                     return True
#                 else:
#                     return False


# def font_display(game_state):
#     if game_state == "main":
#         score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
#         score_rect = score_surface.get_rect(center=(80, 50))
#         win.blit(score_surface, score_rect)

#         high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
#         high_score_rect = high_score_surface.get_rect(center=(450, 50))
#         win.blit(high_score_surface, high_score_rect)

#     if game_state == "game_over":
#         score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255,255))
#         score_rect = score_surface.get_rect(center=(288, 50))
#         win.blit(score_surface, score_rect)

#         high_score_surface = game_font.render(f"High Score: {int(high_score)}", True, (255, 255, 255))
#         high_score_rect = high_score_surface.get_rect(center=(288, 550))
#         win.blit(high_score_surface, high_score_rect)




# def update_score(score,high_score):
#     if score > high_score:
#         high_score = score
#     return high_score


# while True:
#     bird = Bird()
#     # print(bird.collide(bird, win))
#     # print("mmmmmmmmmmmmm")
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE and game_active:
#                 bird_movement = 0
#                 bird_movement -= 3
#                 game_resumed = True
#                 flap_sound.play()

#             if event.key == pygame.K_SPACE and game_active == False:
#                 game_active = True
#                 pipe_list.clear()
#                 bird_rect.center = (100, 350)
#                 bird_movement = 0
#                 score = 0
#                 over_sound.stop()

#             if event.key == pygame.K_UP:
#                 bird_movement = 0
#                 bird_movement -= 6
#                 flap_sound.play()
#                 game_resumed = True

#         if event.type == SPAWNPIPE:
#             pipe_list.extend(Pipe.create_pipe())

#         if event.type == BIRDFLIP:
#             if bird_index < 2:
#                 bird_index += 1
#             else:
#                 bird_index = 0
#             bird_surface, bird_rect = Bird.bird_animation()

#     win.blit(bg_img, (0, 0))

#     if game_active:
#         bird_movement += gravity
#         rotated_bird = Bird.rotate_bird(bird_surface)
#         bird_rect.centery += bird_movement
#         win.blit(rotated_bird, bird_rect)
#         game_active = check_collision(pipe_list)
#         # game_active = check_collision(pipe_list)

#         pipe_list = Pipe.move_pipe(pipe_list)
#         # print("pipe list ",pipe_list)
#         Pipe.draw_pipes(pipe_list)
#         score += 0.01
#         score_sound_countdown -= 1
#         if score_sound_countdown <= 0:
#             score_sound.play()
#             score_sound_countdown = 100
#         font_display("main")
#     else:
#         win.blit(game_over_surface,game_over_rect)
#         high_score = update_score(score,high_score)
#         if event.type == GAMEOVER:
#             if game_over_countdown <= 1000:
#                 over_sound.play()
#                 game_over_countdown += 100

#             else:
#                 game_over_countdown = 1000
#                 over_sound.stop()

#         font_display("game_over")

#     floor_x -= 1
#     draw_floor()
#     if floor_x <= -576:
#         floor_x = 0

#     pygame.display.update()
#     clock.tick(120)

# # if __name__=='__main__':
# #     pass
