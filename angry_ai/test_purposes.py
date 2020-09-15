# import pytest,pygame
from gui import *
from single_player import update_score


def test_score_update():
    actual = update_score(10, 6)
    expect = 10
    assert expect == actual


def test_collision_happen():
    WIN_WIDTH = 500
    WIN_HEIGHT = 670
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    win = WIN
    bird = Bird(400,560)
    p = Pipe(400)
    c = p.collide(bird, win)
    expected = True
    actual = c
    assert expected == actual


def test_collision_fail():
    WIN_WIDTH = 500
    WIN_HEIGHT = 670
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    win = WIN
    bird = Bird(230, 350)
    p = Pipe(400)
    # print(p.collide(bird.x,win))
    c = p.collide(bird, win)
    expected = False
    actual = c
    assert expected == actual
