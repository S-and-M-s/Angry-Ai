import os
import sys
import random
import pygame

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
bird_movement = 0
game_active = True
score = 0
high_score = 0
game_resumed = False
floor_x = 0

# Game images
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "bg.png")).convert_alpha(), (576, 700))
base_img = pygame.transform.scale2x(pygame.image.load("assets/images/base.png").convert())

bird_up_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "small1.png")).convert_alpha())
bird_mid_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "small2.png")).convert_alpha())
bird_down_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets/images", "small3.png")).convert_alpha())
bird_images = [bird_down_img, bird_mid_img, bird_up_img]
bird_index = 2
bird_surface = bird_images[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 300))
# game_over_image
game_over_surface = pygame.transform.scale(pygame.image.load(os.path.join("assets/images", "go.png")).convert_alpha(), (576, 700))
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
flap_sound = pygame.mixer.Sound("assets/sounds/sfx_wing.wav")
death_sound = pygame.mixer.Sound("assets/sounds/sfx_hit.wav")
over_sound = pygame.mixer.Sound("assets/sounds/a.wav")
score_sound = pygame.mixer.Sound("assets/sounds/sfx_point.wav")
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
            if game_over_countdown <= 1000:
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
