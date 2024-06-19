import math
import pygame


class Engine:
    RIGIDNESS = 5 

    def __init__(self, win):
        self.win = win
        self.length, self.height = win.get_size()
        self.points = []
        self.sticks = []
        self.cloths = []
        self.rectangles = []

    def add_point(self, *args, **kwargs):
        point = Point(*args, **kwargs)
        self.points.append(point)

        return point

    def add_cloth(self, *args, **kwargs):
        cloth = Cloth(*args, **kwargs)
        self.cloths.append(cloth)

        for point in cloth.points:
            self.points.append(point)

        for stick in cloth.sticks:
            self.sticks.append(stick)

    def add_rectangle(self, *args, **kwargs):
        rect = Rectangle(*args, **kwargs)
        self.rectangles.append(rect)

        for point in rect.points:
            self.points.append(point)

        for stick in rect.sticks:
            self.sticks.append(stick)

    def update(self):
        for point in self.points:
            point.update()
        
        # self.points.sort(reverse=False, key=lambda point: point.y)
        for _ in range(self.RIGIDNESS):
            for stick in self.sticks:
                 stick.update()

            for point in self.points:
                point.constrain(self.points, self.length, self.height)

    def render(self):
        for point in self.points:
            point.render(self.win)

        for stick in self.sticks:
            stick.render(self.win)
        
    def update_dimensions(self):
        self.length, self.height = self.win.get_size()


class Point:
    BOUNCE = 0.3
    GRAVITY = 0.5
    FRICTION = 0.999

    def __init__(self, pos, vel=None, pinned=False, ghost=False, r=10, hidden=False):
        self.x, self.y = pos

        if vel:
            self.oldx, self.oldy = self.x - vel[0], self.y - vel[1] 
        else:
            self.oldx, self.oldy = (pos[0], pos[1]) 

        self.pinned = pinned
        self.ghost = ghost
        self.r = r
        self.hidden = hidden

    def update(self):
        if self.pinned:
            return

        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION
        self.oldx, self.oldy = self.x, self.y

        self.x += vx
        self.y += vy
        self.y += self.GRAVITY
    
    def constrain(self, points, max_len, max_height):
        if self.pinned or self.ghost:
            return

        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION

        for point in points:
            if point != self and not point.ghost:
                dist = math.dist((self.x, self.y), (point.x, point.y))
                if dist == 0:
                    dist += 0.000001
                if dist < self.r + point.r:
                    dx = point.x - self.x
                    dy = point.y - self.y
                    difference = (self.r + point.r - dist) / dist / 2

                    if point.pinned:
                        self.x -= dx * difference * 2
                        self.y -= dy * difference * 2
                    else:
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
        if self.hidden:
            return

        if self.pinned:
            colour = (255, 0, 0)
        else:
            colour = (255, 255, 255)

        pygame.draw.circle(win, colour, (self.x, self.y), self.r)

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
    def __init__(self, pos, length, height, density=50, ghost=False):
        self.pos = pos
        self.columns = length // density
        self.rows = height // density
        self.density = density
        self.ghost = ghost

        self.points = [Point((pos[0] + density*i, pos[1] + density*j), ghost=ghost) for i in range(self.columns) for j in range(self.rows)]

        self.sticks = []
        for row in range(self.columns):
            for column in range(self.rows):
                index = column + row * self.rows
                point = self.points[index]

                if column == 0:
                    point.pinned = True

                if row != self.columns - 1:
                    self.sticks.append(Stick(point, self.points[index + self.rows]))
                if column != self.rows - 1:
                    self.sticks.append(Stick(point, self.points[index + 1]))
        print(len(self.sticks))

    def update(self):
        pass
    
    def render(self, win):
        for point in self.points:
            point.render(win)


class Rectangle:
    def __init__(self, pos, length, height):
        self.pos = pos
        self.length = length
        self.height = height

        self.points = [Point(pos), Point((pos[0] + length, pos[1])), Point((pos[0] + length, pos[1] + height)), Point((pos[0], pos[1] + height))]
        self.sticks = [Stick(self.points[0], self.points[1]), Stick(self.points[1], self.points[2]), Stick(self.points[2], self.points[3]), Stick(self.points[0], self.points[3]), Stick(self.points[0], self.points[2])]


