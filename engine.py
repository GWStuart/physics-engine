import math
import pygame


class Engine:
    RIGIDNESS = 5

    def __init__(self, win):
        self.win = win
        self.length, self.height = win.get_size()
        self.points = []
        self.sticks = []

    def add_point(self, *args, **kwargs):
        self.points.append(Point(*args, **kwargs))

    def update(self):
        for point in self.points:
            if not point.pinned:
                point.update()
        
        for _ in range(self.RIGIDNESS):
            for stick in self.sticks:
                stick.update()

            for point in self.points:
                if not point.pinned:
                    point.constrain(self.points, self.length, self.height)

    def render(self):
        for point in self.points:
            point.render(self.win)

        for stick in self.sticks:
            stick.render(self.win)
        
    def update_dimensions(self):
        self.length, self.height = self.win.get_size()


class Point:
    BOUNCE = 0
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
    
    def constrain(self, points, max_len, max_height):
        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION

        for point in points:
            if point != self:
                dist = math.dist((self.x, self.y), (point.x, point.y))
                if dist == 0:
                    dist += 0.000001
                if dist < self.r + point.r:
                    dx = point.x - self.x
                    dy = point.y - self.y
                    difference = (self.r + point.r - dist) / dist / 2
                    
                    point.x += dx * difference
                    point.y += dy * difference
                    self.x -= dx * difference
                    self.y -= dy * difference

        if self.x > max_len - self.r:
            self.x = max_len - self.r
            self.oldx = self.x + vx * self.BOUNCE
        elif self.x < self.r:
            self.x = self.r
            self.oldx = self.x + vx * self.BOUNCE
        if self.y > max_height - self.r:
            self.y = max_height - self.r
            self.oldy = self.y + vy * self.BOUNCE
        elif self.y < self.r:
            self.y = self.r
            self.oldy = self.y + vy * self.BOUNCE


    def render(self, win):
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

    def render(self, win):
        pygame.draw.line(win, (255, 255, 255), (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), self.WIDTH)


class Cloth:
    def __init__(self, pos, length, height, density=50):
        self.pos = pos
        self.length = length
        self.height = height
        self.density = density
        
        self.points = [Point((pos[0] + density*i, pos[1] + density*j)) for i in range(length // density) for j in range(height // density)]
    
    def render(self, win):
        for point in self.points:
            point.render(win)

