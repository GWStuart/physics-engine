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

    if mode == 1 and pressed:
        mouse = pygame.mouse.get_pos()
        pygame.draw.circle(win, (255, 255, 255), pressed, radius)
        if math.dist(pressed, mouse) > radius + BUFFER:
            pygame.draw.line(win, (255, 0, 0), pressed, mouse, 3)

    if mode == 1 and line:
        mouse = pygame.mouse.get_pos()
        pygame.draw.line(win, (255, 255, 255), (line.x, line.y), mouse, 3)

    if mode == 2 and render_cursor_point:
        pygame.draw.circle(win, (255, 0, 0), (cursor_point.x, cursor_point.y), cursor_point.r, 1)

    if mode == 3 and chosen_point:
        colour = (255, 0, 0) if chosen_pinned else (255, 255, 255)
        pygame.draw.circle(win, colour, (chosen_point.x, chosen_point.y), chosen_point.r)

    if mode == 5 and line:
        mouse = pygame.mouse.get_pos()
        pygame.draw.line(win, (255, 0, 0), line, mouse, 1)

    if show_info:
        win.blit(title, (10, 10))
        win.blit(sub_title, (10, 30))
        mode_msg = font_sm.render(f"running (space): {'yes' if update else 'no'}", True, (255, 255, 255))
        win.blit(mode_msg, (10, 60))
        mode_msg = font_sm.render(f"mode (num keys): {modes.get(mode)}", True, (255, 255, 255))
        win.blit(mode_msg, (10, 80))

        if mode == 2:
            mode_msg = font_sm.render(f"show mouse field (f): {render_cursor_point}", True, (255, 255, 255))
            win.blit(mode_msg, (10, 100))

    pygame.display.update()

# def get_point(x, y):


engine = Engine(win)
cursor_point = engine.add_point((-10, -10), pinned=True, hidden=True)
render_cursor_point = True

tick = 0

pressed = None
update = True
show_info = True
line = None
chosen_point = None
chosen_pinned = None

mode = 1
modes = {1: "normal", 2: "mouse field", 3: "drag", 4: "cloth", 5: "cut"}

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
        if mode == 1 and event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if event.button == 1:
                for point in engine.points:
                    if math.dist(mouse, (point.x, point.y)) < point.r:
                        line = point
                        break
                else:
                    pressed = mouse
            elif event.button == 3:
                for point in engine.points:
                    if math.dist(mouse, (point.x, point.y)) < point.r:
                        point.pinned = not point.pinned
                        break
        elif mode == 3 and event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for point in engine.points:
                if math.dist(mouse, (point.x, point.y)) < point.r:
                    chosen_point = point
                    chosen_pinned = chosen_point.pinned
                    chosen_point.pinned = True
                    chosen_point.hidden = True
        elif mode == 3 and event.type == pygame.MOUSEBUTTONUP and chosen_point:
            chosen_point.pinned = chosen_pinned
            chosen_point.hidden = False
            mouse = pygame.mouse.get_pos()
            chosen_point.oldx, chosen_point.oldy = chosen_point.x, chosen_point.y 
            chosen_point.x, chosen_point.y = mouse
            chosen_point = None
            chosen_pinned = None
        elif mode == 5 and event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            line = mouse
        elif mode == 5 and event.type == pygame.MOUSEBUTTONUP:
            line = None
        elif mode == 1 and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if pressed:
                mouse = pygame.mouse.get_pos()
                if math.dist(pressed, mouse) < radius + BUFFER:
                    engine.add_point(pressed, r=radius)
                else:
                    vel = ((pressed[0] - mouse[0]) / 10, (pressed[1] - mouse[1]) / 10)
                    engine.add_point(pressed, vel=vel, r=radius)

                pressed = None
                radius = 10  # reset radius
            else:
                mouse = pygame.mouse.get_pos()
                for point in engine.points:
                    if math.dist(mouse, (point.x, point.y)) < point.r:
                        p2 = point
                        if p2 != line:
                            engine.add_stick(line, p2)
                        break
                line = None

        elif event.type == pygame.MOUSEWHEEL:
            if mode == 2:
                cursor_point.r -= event.y
            else:
                radius -= event.y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                update = not update 
            elif event.key == pygame.K_h:
                show_info = not show_info
            elif mode == 2 and event.key == pygame.K_f:
                render_cursor_point = not render_cursor_point
            elif event.key == pygame.K_c:
                engine.clear_all()
                cursor_point = engine.add_point((-10, -10), pinned=True, hidden=True)
            elif 48 <= event.key <= 57: 
                if mode == 2:
                    cursor_point.x, cursor_point.y = -30, -30
                    cursor_point.r = 10 
                    render_cursor_point = True
                if mode == 1:
                    line = None
                mode = event.key - 48
    
    if mode == 2:
        cursor_point.x, cursor_point.y = pygame.mouse.get_pos()
    if mode == 3 and chosen_point:
        chosen_point.x, chosen_point.y = pygame.mouse.get_pos()
 
    if update:
        engine.update()

    render()
    clock.tick(60)

