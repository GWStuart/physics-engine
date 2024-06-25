import math
import pygame


class Engine:
    RIGIDNESS = 5 

    def __init__(self, length, height):
        self.length, self.height = length, height 
        self.points = []
        self.sticks = []
        self.lines = []

    def add_line(self, *args, **kwargs):
        line = Line(*args, **kwargs)
        self.lines.append(line)

        return line

    def add_point(self, *args, **kwargs):
        point = Point(*args, **kwargs)
        self.points.append(point)

        return point

    def add_cloth(self, *args, **kwargs):
        cloth = Cloth(*args, **kwargs)
        # self.cloths.append(cloth)

        for point in cloth.points:
            self.points.append(point)

        for stick in cloth.sticks:
            self.sticks.append(stick)

    def add_stick(self, *args, **kwargs):
        stick = Stick(*args, **kwargs)
        self.sticks.append(stick)

        return stick

    def add_rectangle(self, *args, **kwargs):
        rect = Rectangle(*args, **kwargs)
        self.rectangles.append(rect)

        for point in rect.points:
            self.points.append(point)

        for stick in rect.sticks:
            self.sticks.append(stick)

    def clear_all(self):
        self.points = []
        self.sticks = []
        # self.cloths = []
        self.rectangle = []

    def get_point(self, x, y):
        # return the point that overlaps the coordinates (x, y)
        # if there was not point then it return none
        for point in self.points:
            if math.dist((x, y), (point.x, point.y)) <= point.r:
                return point

    def remove_point(self, point):
        for stick in self.sticks:
            if stick.p1 == point or stick.p2 == point:
                self.sticks.remove(stick)

        self.points.remove(point)

    def stick_line_intersection(self, p1, p2):
        # Finds the stick that intersects a line from p1 to p2
        collisions = []
 
        for stick in self.sticks:
            x1, y1 = p1
            x2, y2 = p2
            x3, y3 = stick.p1.x, stick.p1.y
            x4, y4 = stick.p2.x, stick.p2.y
            
            d = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
            if d == 0:
                print("IF SOMETHING BREAKS CHECK THIS OUT")
                # if min(y3, y4) <= y1 and max(y3, y4) >= y1:
                #     print("possible collision")
                continue

            a = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / d
            b = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / d 
            if 0 <= a <= 1 and 0 <= b <= 1:
                collisions.append(stick)

        return collisions

    def remove_stick(self, stick):
        self.sticks.remove(stick)

    def update(self):
        for point in self.points:
            point.update()
        
        # self.points.sort(reverse=False, key=lambda point: point.y)
        for _ in range(self.RIGIDNESS):
            for stick in self.sticks:
                 stick.update()

            for point in self.points:
                point.constrain(self.points, self.length, self.height, self.lines)

    def render(self, win):
        for line in self.lines:
            line.render(win)

        for stick in self.sticks:
            stick.render(win)

        for point in self.points:
            point.render(win)
        
    def update_dimensions(self, length, height):
        self.length, self.height = length, height 


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
    
    def constrain(self, points, max_len, max_height, lines):
        # print("CONSTRAIN")
        # for line in lines:
        #     if line.intersect_point(self):
        #         print("TOUCH")

        if self.pinned or self.ghost:
            return

        vx = (self.x - self.oldx) * self.FRICTION
        vy = (self.y - self.oldy) * self.FRICTION
        
        # check for point collisions and constrain if necessary
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

        for line in lines:
            collision = line.intersect_point(self)
            if collision:
                print("COLLIDE")
                while line.intersect_point(self):
                    self.x += line.nx
                    self.y += line.ny
                # self.x, self.y = collision 
        
        # check for border collisions and constrain if necessary
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
    def __init__(self, pos, length, height, density=50, ghost=False, hidden=False):
        self.columns = length // density + 1
        self.rows = height // density + 1

        self.points = [Point((pos[0] + density*i, pos[1] + density*j), ghost=ghost, hidden=hidden) 
            for i in range(self.columns) for j in range(self.rows)]

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


class Rectangle:
    def __init__(self, pos, length, height):
        self.pos = pos
        self.length = length
        self.height = height

        self.points = [Point(pos), Point((pos[0] + length, pos[1])), Point((pos[0] + length, pos[1] + height)), Point((pos[0], pos[1] + height))]
        self.sticks = [Stick(self.points[0], self.points[1]), Stick(self.points[1], self.points[2]), Stick(self.points[2], self.points[3]), Stick(self.points[0], self.points[3]), Stick(self.points[0], self.points[2])]


class Line:
    # A line is an immovable barrier that constrains points
    def __init__(self, p1, p2, width=11):
        self.p1 = p1
        self.p2 = p2
        self.width = width
        length = ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2) ** 0.5
        coef = 1 if min(p1, p2, key=lambda x: x[0])[1] < max(p1, p2, key=lambda x: x[0])[1] else -1
        self.nx = (p2[1] - p1[1]) / length * coef 
        self.ny = -(p2[0] - p1[0]) / length * coef 

    def render(self, win):
        pygame.draw.line(win, (255, 255, 255), self.p1, self.p2, self.width)
        # pygame.draw.circle(win, (255, 255, 255), self.p1, self.width // 2)
        # pygame.draw.circle(win, (255, 255, 255), self.p2, self.width // 2)

    def intersect_point(self, point):
        x1, y1 = point.x, point.y 
        x2, y2 = point.oldx, point.oldy 
        x3, y3 = self.p1[0], self.p1[1] - point.r - self.width/2
        x4, y4 = self.p2[0], self.p2[1] - point.r - self.width/2

        d = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
        if d == 0:  # This means that there is a horizontal line
            print("CHECK OUT IF SOMTHIN BREAKS")
            return False

        a = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / d
        b = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / d 
        if 0 <= a <= 1 and 0 <= b <= 1:
            return (x1 + a * (x2 - x1)), (y1 + b * (y2 - y1))

