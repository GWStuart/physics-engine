import pygame
import random
import math
from engine import *

LENGTH, HEIGHT = 800, 600
win = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Verlet Integration")

clock = pygame.time.Clock()

RIGIDNESS = 5 


def update():
    for point in points:
        if not point.pinned:
            point.update()
    
    for _ in range(RIGIDNESS):
        for stick in sticks:
            stick.update()

        constrain_points(points)


def render():
    win.fill((30, 30, 30))

    for point in points:
        point.render(win)

    for stick in sticks:
        stick.render(win)

    pygame.display.update()


# points = [Point((300, 200), pinned=True), Point((300, 400)), Point((400, 200)), Point((400, 400))]
# sticks = [Stick(points[0], points[1]), Stick(points[0], points[2]), Stick(points[3], points[2]), Stick(points[3], points[1]), Stick(points[0], points[3])]

points = [Point((300, 200), vel=(3, 0)), Point((300, 150))] # , Point((300, 100))]
sticks = [] # [Stick(points[0], points[1])]

tick = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            points.append(Point(mouse))
        elif event.type == pygame.VIDEORESIZE:
            LENGTH, HEIGHT = win.get_size()
            update_dimensions(LENGTH, HEIGHT)
    
    update()
    render()
    clock.tick(60)

    # tick += 1
    # tick %= 30
    # if tick == 0:
    #     points.append(Point((300, 300), vel=(random.uniform(-1, 1), random.uniform(-1, 1))))

