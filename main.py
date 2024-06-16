import pygame
import math

LENGTH, HEIGHT = 800, 600
win = pygame.display.set_mode((LENGTH, HEIGHT))
pygame.display.set_caption("Verlet Integration")

clock = pygame.time.Clock()

RIGIDNESS = 5 

class Point:
    BOUNCE = 0.7
    GRAVITY = 0.5
    FRICTION = 0.999

    def __init__(self, pos, vel=None, pinned=False):
        self.x, self.y = pos

        if vel:
            self.oldx, self.oldy = self.x - vel[0], self.y - vel[1] 
        else:
            self.oldx, self.oldy = (pos[0], pos[1]) 

        self.pinned = pinned
        self.r = 10

    def update(self):
        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION
        self.oldx, self.oldy = self.x, self.y

        self.x += vx
        self.y += vy
        self.y += self.GRAVITY
    
    def constrain(self):
        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION

        for point in points:
            if point != self:
                dist = math.dist((self.x, self.y), (point.x, point.y))
                if dist < self.r + point.r:
                    dx = point.x - self.x
                    dy = point.y - self.y
                    difference = (self.r + point.r - dist) / dist / 2
                    
                    point.x += dx * difference
                    point.y += dy * difference
                    self.x -= dx * difference
                    self.y -= dy * difference

        if self.x > LENGTH - self.r:
            self.x = LENGTH - self.r
            self.oldx = self.x + vx * self.BOUNCE
        elif self.x < self.r:
            self.x = self.r
            self.oldx = self.x + vx * self.BOUNCE
        if self.y > HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.oldy = self.y + vy * self.BOUNCE
        elif self.y < self.r:
            self.y = self.r
            self.oldy = self.y + vy * self.BOUNCE


    def render(self):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), self.r)

class Stick:
    WIDTH = 3

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = math.dist((self.p1.x, self.p1.y), (self.p2.x, self.p2.y)) 

    def update(self):
        dx = self.p2.x - self.p1.x
        dy = self.p2.y - self.p1.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        difference = (self.length - distance) / distance / 2
        
        if self.p1.pinned or self.p2.pinned:
            difference *= 2

        if not self.p1.pinned:
            self.p1.x -= dx * difference
            self.p1.y -= dy * difference
        if not self.p2.pinned:
            self.p2.x += dx * difference
            self.p2.y += dy * difference

    def render(self):
        pygame.draw.line(win, (255, 255, 255), (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), self.WIDTH)


def update():
    for point in points:
        if not point.pinned:
            point.update()
    
    for _ in range(RIGIDNESS):
        for stick in sticks:
            stick.update()

        for point in points:
            if not point.pinned:
                point.constrain()

def render():
    win.fill((30, 30, 30))

    for point in points:
        point.render()

    for stick in sticks:
        stick.render()

    pygame.display.update()


# points = [Point((300, 200), pinned=True), Point((300, 400)), Point((400, 200)), Point((400, 400))]
# sticks = [Stick(points[0], points[1]), Stick(points[0], points[2]), Stick(points[3], points[2]), Stick(points[3], points[1]), Stick(points[0], points[3])]

points = [Point((300, 200), vel=(3, 0)), Point((300, 150))] # , Point((300, 100))]
sticks = [] # [Stick(points[0], points[1])]

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
    
    update()
    render()
    clock.tick(60)

