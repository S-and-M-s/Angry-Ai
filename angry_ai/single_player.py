from gui import Bird, Pipe, Base, draw_window, blitRotateCenter
import os
import pygame
import sys
from subprocess import call

# initials parameters:
pygame.init()
pygame.mixer.pre_init(frequency=44100, channels=1, buffer=512, size=16)
pygame.display.set_caption("Flappy Bird -S&M's")
pygame.font.init()  # init font
game_font = pygame.font.SysFont("", 50)

WIN_WIDTH = 560
WIN_HEIGHT = 670
FLOOR = 595
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Game variables
global game_active
game_active = True
score = 0
high_score = 0
game_resumed = False

# Background image

bg_img = pygame.transform.scale(pygame.image.load(
    os.path.join("assets/images", "bg4.jpg")).convert_alpha(), (576, 700))


def font_display(game_state):
    if game_state == "main":
        score_surface = game_font.render(
            f"Score {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(80, 50))
        WIN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f"High Score {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(450, 50))
        WIN.blit(high_score_surface, high_score_rect)

    if game_state == "game_over":
        score_surface = game_font.render(
            f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 50))
        WIN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f"High Score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 550))
        WIN.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def draw_window(win, bird, pipes, base, score, pipe_ind, high_score,gameover=False):
    """
    draws the windows for the main game loop
    :param win: pygame window surface
    :param bird: a Bird object
    :param pipes: List of pipes
    :param score: score of the game (int)
    :param pipe_ind: index of closest pipe
    :return: None
    """

    if gameover == True:
        base.draw(win)
        bird.draw(win)
        # WIN.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score = 0

    else:
        win.blit(bg_img, (0, 0))

        for pipe in pipes:
            pipe.draw(win)

        base.draw(win)

        bird.draw(win)

        # score
        score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(score_label, (15, 10))
        # high score
        score_label = STAT_FONT.render(
            "High Score: " + str(high_score), 1, (255, 255, 255))
        win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 10, 10))
        pygame.display.update()





def player_loop():

    high_score = 0
    global WIN
    win = WIN
    bird = Bird(120, 250)
    base = Base(FLOOR)
    pipes = [Pipe(400)]
    score = 0
    clock = pygame.time.Clock()
    game_active = True

    # Timer for game over sound
    GAMEOVER = pygame.USEREVENT + 2
    pygame.time.set_timer(GAMEOVER, 900)
    game_over_countdown = 1000

    # sounds
    flap_sound = pygame.mixer.Sound("assets/sounds/sfx_wing.wav")
    death_sound = pygame.mixer.Sound("assets/sounds/sfx_hit.wav")
    over_sound = pygame.mixer.Sound("assets/sounds/a.wav")
    score_sound = pygame.mixer.Sound("assets/sounds/sfx_point.wav")
    score_sound_countdown = 100
    run = True
    while run:
        clock.tick(30)
        draw_window(win, bird, pipes, base, score, 1, high_score,gameover=False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                      bird.jump()
                      game_resumed = True
                      flap_sound.play()
                # to finish the game
                if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:
                     run = False
                     call(["python", "angry_ai/main_screen.py"])
                     pygame.quit()
                     quit()

                # to back to main menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        draw_window(win, bird, pipes, base, score, 1, high_score,gameover=True)
                        run =False
                        call(["python", "angry_ai/main_screen.py"])
                if event.key == pygame.K_SPACE and game_active == False:
                        game_active = True
                        bird = Bird(200, 300)
                        score = 0
                        over_sound.stop()

            pipe_ind = 0
            if len(pipes) > 1 and bird.x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1

            rem = []
            add_pipe = False
            for pipe in pipes:
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if pipe.collide(bird, win):
                    draw_window(win, bird, pipes, base, score, 1, high_score,gameover=True)
                    run = False

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if add_pipe:
                score += 1
                pipes.append(Pipe(WIN_WIDTH))

            for r in rem:
                pipes.remove(r)
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                draw_window(win, bird, pipes, base, score, 1, high_score,gameover=True)
                run = False

        if game_active==True:
            base.move()
            for pipe in pipes:
                pipe.move()
            bird.move()

            score_sound_countdown -= 1
            if score_sound_countdown <= 0:
                score_sound.play()
                score_sound_countdown = 100




if __name__ == "__main__":
    player_loop()
