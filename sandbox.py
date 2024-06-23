import pygame
import math
from engine import Engine 
from tkinter import filedialog
import pickle
import random # DELETE LATER
pygame.init()

LENGTH, HEIGHT = 800, 600
win = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Verlet Integration")

clock = pygame.time.Clock()
font_bg = pygame.font.SysFont(None, 24)
font_sm = pygame.font.SysFont(None, 22)

title = font_bg.render("Physics Simulator ~ GWStuart", True, (255, 255, 255))
sub_title = font_sm.render("(toggle this screen with 'h')", True, (255, 255, 255))

## some variables ##
mode = 1  # the current game mode (see modes dictionary for their corresponding names)
modes = {1: "normal", 2: "drag", 3: "mouse field", 4: "cloth", 5: "cut"}
update = True  # whether the physics should update or not (toggled with space)
show_info = True  # whether info should be shown on the screen or not(toggled with h)
mouse_coords = None  # used to store the location of a mouse click 
point_radius = 10  # the default radius of a circle (is defined in more than 1 place)
chosen_point = None  # stores a point object
chosen_pinned = None  # records whether the chosen point was pinned or not (used for point dragging)

CLICK_BUFFER = 5  # A buffer allowing a region where the click can be release without adding velocity
VEL_FACTOR = 10  # The factor by which the points velocity is scaled down (smaller number = more velocity)

engine = Engine(LENGTH, HEIGHT)
cursor_point = engine.add_point((-10, -10), pinned=True, hidden=True)
render_cursor_point = True


def render():
    win.fill((30, 30, 30))

    engine.render(win)

    if mode == 1:
        if chosen_point:
            mouse = pygame.mouse.get_pos()
            pygame.draw.line(win, (255, 255, 255), (chosen_point.x, chosen_point.y), mouse, 3)
        if mouse_coords:
            mouse = pygame.mouse.get_pos()
            pygame.draw.circle(win, (255, 255, 255), mouse_coords, point_radius)
            if math.dist(mouse_coords, mouse) > point_radius + CLICK_BUFFER:
                pygame.draw.line(win, (255, 0, 0), mouse_coords, mouse, 3)

    if mode == 2 and chosen_point:
        colour = (255, 0, 0) if chosen_pinned else (255, 255, 255)
        pygame.draw.circle(win, colour, (chosen_point.x, chosen_point.y), chosen_point.r)

    if mode == 3 and render_cursor_point:
        pygame.draw.circle(win, (255, 0, 0), (cursor_point.x, cursor_point.y), cursor_point.r, 1)

    if mode == 4 and mouse_coords:
        mouse = pygame.mouse.get_pos()
        pygame.draw.line(win, (200, 200, 200), mouse_coords, (mouse_coords[0], mouse[1]), 1)
        pygame.draw.line(win, (200, 200, 200), mouse_coords, (mouse[0], mouse_coords[1]), 1)
        pygame.draw.line(win, (200, 200, 200), mouse, (mouse[0], mouse_coords[1]), 1)
        pygame.draw.line(win, (200, 200, 200), mouse, (mouse_coords[0], mouse[1]), 1)
        pygame.draw.circle(win, (0, 255, 0), mouse_coords, point_radius)
        pygame.draw.circle(win, (0, 255, 0), mouse, point_radius)

    if mode == 5 and mouse_coords:
        mouse = pygame.mouse.get_pos()
        pygame.draw.line(win, (255, 0, 0), mouse_coords, mouse, 1)

    if show_info:
        win.blit(title, (10, 10))
        win.blit(sub_title, (10, 30))
        mode_msg = font_sm.render(f"running (space): {'yes' if update else 'no'}", True, (255, 255, 255))
        win.blit(mode_msg, (10, 60))
        mode_msg = font_sm.render(f"mode (num keys): {modes.get(mode)}", True, (255, 255, 255))
        win.blit(mode_msg, (10, 80))

        if mode == 3:
            mode_msg = font_sm.render(f"show mouse field (f): {render_cursor_point}", True, (255, 255, 255))
            win.blit(mode_msg, (10, 100))

    pygame.display.update()


run = True
while run:
    # Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            run = False
        if event.type == pygame.VIDEORESIZE:
            LENGTH, HEIGHT = win.get_size()
            engine.update_dimensions(LENGTH, HEIGHT)
        if event.type == pygame.MOUSEWHEEL:
            if mode == 3:
                cursor_point.r -= event.y
            else:
                point_radius -= event.y
        
        # Check for each sandbox mode
        if mode == 1:  # normal mode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if event.button == 1: # detect a left click
                    point = engine.get_point(*mouse)
                    if point:
                        chosen_point = point
                    else:  # if the user did not click on a point
                        mouse_coords = mouse
                elif event.button == 3:
                    point = engine.get_point(*mouse)
                    if point:
                        point.pinned = not point.pinned

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse = pygame.mouse.get_pos()
                if mouse_coords:  # if this is the case then the user is placing a regular point
                    if math.dist(mouse_coords, mouse) < point_radius + CLICK_BUFFER:
                        engine.add_point(mouse_coords, r=point_radius)
                    else:
                        vel = ((mouse_coords[0] - mouse[0]) / VEL_FACTOR, (mouse_coords[1] - mouse[1]) / VEL_FACTOR)
                        engine.add_point(mouse_coords, vel=vel, r=point_radius)

                    mouse_coords = None
                    point_radius = 10  # reset point_radius
                elif chosen_point:  # if this is the case then the user is trying to connect points
                    point = engine.get_point(*mouse)
                    if point and point != chosen_point:
                        engine.add_stick(chosen_point, point)  # create a new stick that joins the points
                    chosen_point = None
                else:
                    print("THIS SHOULD NEVER PRINT")
 
        elif mode == 2:  # drag mode
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                chosen_point = engine.get_point(*mouse)
                if chosen_point:  # save the clicked point. Set it up so that the user can drag it
                    chosen_pinned = chosen_point.pinned
                    chosen_point.pinned = True
                    chosen_point.hidden = True

            if event.type == pygame.MOUSEBUTTONUP and chosen_point:
                chosen_point.pinned = chosen_pinned
                chosen_point.hidden = False
                mouse = pygame.mouse.get_pos()
                chosen_point.oldx, chosen_point.oldy = chosen_point.x, chosen_point.y 
                chosen_point.x, chosen_point.y = mouse
                chosen_point = None
                chosen_pinned = None
        
        elif mode == 4:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if mouse_coords:
                    engine.add_cloth(mouse_coords, mouse[0] - mouse_coords[0], mouse[1] - mouse_coords[1])
                    # density = 50 is default
                    mouse_coords = None
                else:
                    mouse_coords = mouse

        elif mode == 5:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_coords = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_coords = None
        
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                update = not update 
            elif event.key == pygame.K_h:
                show_info = not show_info
            elif mode == 3 and event.key == pygame.K_f:
                render_cursor_point = not render_cursor_point
            elif event.key == pygame.K_c:
                engine.clear_all()
                cursor_point = engine.add_point((-10, -10), pinned=True, hidden=True)
            elif event.key == pygame.K_s:
                file_path = filedialog.asksaveasfilename(defaultextension=".physics")
                if file_path:
                    with open(file_path, "wb") as f:
                        pickle.dump(engine, f)
            elif event.key == pygame.K_o:
                file_path = filedialog.askopenfilename()
                if file_path:
                    with open(file_path, "rb") as f:
                        engine = pickle.load(f)
            elif 48 <= event.key <= 57: 
                chosen_point = None
                mouse_coords = None
                point_radius = 10
                cursor_point.x, cursor_point.y = -30, -30
                cursor_point.r = 10 
                render_cursor_point = True
                
                mode = event.key - 48
    
    # Update the display
    if mode == 2 and chosen_point:
        chosen_point.x, chosen_point.y = pygame.mouse.get_pos()
    if mode == 3:
        cursor_point.x, cursor_point.y = pygame.mouse.get_pos()
 
    if update:
        engine.update()
    
    # Render
    render()
    
    clock.tick(60)

