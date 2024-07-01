import pygame
import math
import random
pygame.init()

LENGTH, HEIGHT = 400, 500
win = pygame.display.set_mode((LENGTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Fire Simulation")

clock = pygame.time.Clock()


class Engine:
    RIGIDNESS = 5 

    def __init__(self):
        self.points = []

    def add_point(self, *args, **kwargs):
        point = Point(*args, **kwargs)
        self.points.append(point)
        return point

    def update(self):
        for point in self.points:
            point.update()
        
        # self.points.sort(reverse=False, key=lambda point: point.y)
        for _ in range(self.RIGIDNESS):
            for point in self.points:
                point.constrain(self.points)

    def render(self, win):
        for point in self.points:
            point.render(win)


class Point:
    GRAVITY = 0.5
    FRICTION = 0.999
    radius = 10

    def __init__(self, pos, vel=None):
        self.x, self.y = pos

        if vel:
            self.oldx, self.oldy = self.x - vel[0], self.y - vel[1] 
        else:
            self.oldx, self.oldy = pos

    def update(self):
        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION
        self.oldx, self.oldy = self.x, self.y

        self.x += vx
        self.y += vy + self.GRAVITY
    
    def constrain(self, points):
        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION
        
        # check for point collisions and constrain if necessary
        for point in points:
            if point != self:
                dist = math.dist((self.x, self.y), (point.x, point.y))
                if dist == 0:
                    point.x += 5
                    point.y += 5
                    self.x -= 5
                    self.y -= 5
                    # dist += 0.000001
                elif dist < self.radius*2:
                    difference = (self.radius*2 - dist) / dist / 2
                    dx = (point.x - self.x) * difference
                    dy = (point.y - self.y) * difference

                    point.x += dx
                    point.y += dy
                    self.x -= dx
                    self.y -= dy
        
        if self.x > LENGTH - self.radius:
            self.x = LENGTH - self.radius
        elif self.x < self.radius:
            self.x = self.radius
        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
        elif self.y < self.radius:
            self.y = self.radius

    def render(self, win):
        colour = (255, 255, 255)
        pygame.draw.circle(win, colour, (self.x, self.y), self.radius)


def render():
    win.fill((30, 30, 30))
    engine.render(win)
    pygame.display.update()


engine = Engine()

spacing = 20
rows = 8
for column in range(6, LENGTH - 6, spacing):
    for row in range(0, rows * spacing, spacing):
        engine.add_point((column + 6, HEIGHT - row - 6))

# count = 200
frame = 0

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            run = False
        if event.type == pygame.VIDEORESIZE:
            LENGTH, HEIGHT = win.get_size()
        
    frame += 1
    frame %= 60 
    # if frame % 10 == 0 and count:
    #     engine.add_point((LENGTH/2, HEIGHT/2), vel=(random.uniform(-1, 1), random.uniform(-1, 1)))
    #     count -= 1

    engine.update()
    render()
    
    clock.tick(60)
    if not frame:  # 200 balls --> 25-28fps => 27-28fps => 29fps
        print(clock.get_fps())

