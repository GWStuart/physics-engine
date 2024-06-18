import pygame
import random
import math
from engine import Engine 

LENGTH, HEIGHT = 800, 600
win = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Verlet Integration")

clock = pygame.time.Clock()

radius = 10
BUFFER = 5


def render():
    win.fill((30, 30, 30))

    engine.render()

    if pressed:
        mouse = pygame.mouse.get_pos()
        pygame.draw.circle(win, (255, 255, 255), pressed, radius)
        if math.dist(pressed, mouse) > radius + BUFFER:
            pygame.draw.line(win, (255, 0, 0), pressed, mouse, 3)

    pygame.display.update()

engine = Engine(win)

tick = 0

pressed = None
update = True

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
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pressed = pygame.mouse.get_pos() 

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse = pygame.mouse.get_pos()
            if math.dist(pressed, mouse) < radius + BUFFER:
                engine.add_point(pressed, r=radius)
            else:
                vel = ((pressed[0] - mouse[0]) / 10, (pressed[1] - mouse[1]) / 10)
                engine.add_point(pressed, vel=vel, r=radius)

            pressed = None
            radius = 10  # reset radius

        elif event.type == pygame.MOUSEWHEEL:
            radius += event.y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                update = not update 
    
    if update:
        engine.update()

    render()
    clock.tick(60)

