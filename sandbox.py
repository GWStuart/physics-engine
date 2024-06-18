import pygame
import random
import math
from engine import Engine 

LENGTH, HEIGHT = 800, 600
win = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Verlet Integration")

clock = pygame.time.Clock()

RADIUS = 50


def render():
    win.fill((30, 30, 30))

    engine.render()

    if pressed:
        mouse = pygame.mouse.get_pos()
        if math.dist(pressed, mouse) > 10:
            pygame.draw.line(win, (255, 0, 0), pressed, mouse, 3)

    pygame.display.update()

engine = Engine(win)

points = []
sticks = []

tick = 0

pressed = None

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            run = False
        elif event.type == pygame.VIDEORESIZE:
            LENGTH, HEIGHT = win.get_size()
            engine.update_dimensions()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            engine.add_point(mouse)
            pressed = pygame.mouse.get_pos()
              

        elif event.type == pygame.MOUSEBUTTONUP:
            if not math.dist(pressed, pygame.mouse.get_pos()) < RADIUS:
                print("Fire")
            pressed = None

    # engine.update()

    render()
    clock.tick(60)

