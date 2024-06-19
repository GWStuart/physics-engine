import pygame
import random
import math
from engine import Engine 
pygame.init()

LENGTH, HEIGHT = 800, 600
win = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Verlet Integration")

clock = pygame.time.Clock()
font_bg = pygame.font.SysFont(None, 24)
font_sm = pygame.font.SysFont(None, 22)

title = font_bg.render("Physics Simulator ~ GWStuart", True, (255, 255, 255))
sub_title = font_sm.render("(toggle this screen with 'h')", True, (255, 255, 255))

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

    if show_info:
        win.blit(title, (10, 10))
        win.blit(sub_title, (10, 30))
        mode_msg = font_sm.render(f"mode: {mode}", True, (255, 255, 255))
        win.blit(mode_msg, (10, 60))

    pygame.display.update()

engine = Engine(win)
cursor_point = engine.add_point((-10, -10), pinned=True, hidden=True)

tick = 0

pressed = None
update = True
show_info = True
mode = 1

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
            if mode == 2:
                cursor_point.r += event.y
            else:
                radius += event.y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                update = not update 
            elif event.key == pygame.K_h:
                show_info = not show_info
            elif 48 <= event.key <= 57: 
                if mode == 2:
                    cursor_point.x, cursor_point.y = -30, -30
                    cursor_point.r = 10 
                mode = event.key - 48
    
    if update:
        if mode == 2:
            cursor_point.x, cursor_point.y = pygame.mouse.get_pos()
        engine.update()

    render()
    clock.tick(60)

