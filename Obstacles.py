
# Obstacles.py
import pyglet.shapes as shapes
from random import choice, uniform
from Utils import PHYSICAL_SIZE, ROAD_PADDING

class Obstacle:
    def __init__(self, game, kind):
        self.game = game
        self.kind = kind # State: Type of obstacle (affects size)
        
        COLORS = {
            "bike": (255, 255, 0),
            "car2": (255, 50, 50),
            "truck": (50, 255, 50)
        }

        road_left = (self.game.road_left) 
        road_width = (self.game.road_right - self.game.road_left)

        width, height = PHYSICAL_SIZE[kind]
        
        self.x = uniform(road_left + width/2, road_left + road_width - width/2) # State: Lateral position of obstacle
        self.y = getattr(self.game, 'window_height', 720) + 200 # State: Vertical position of obstacle

        self.shape = shapes.Rectangle(
            x=self.x, y=self.y,
            width=width, height=height,
            color=COLORS.get(kind, (200, 200, 200))
        )
        self.shape.anchor_x = width // 2
        self.shape.anchor_y = height // 2

    def update(self, dt, speed):
        self.y -= speed * dt
        self.shape.y = self.y

    def get_hitbox(self):
        w, h = PHYSICAL_SIZE[self.kind]
        return (self.x - w/2, self.y - h/2, w, h)

    def draw(self):
        self.shape.draw()

    def off_screen(self):
        return self.y < -200


class ObstacleManager:
    def __init__(self, game):
        self.game = game
        self.list = [] # State: List of all active obstacles
        self.timer = 0
        self.spawn_period_range = (1.0, 2.0) # Variable: Range (min, max) for spawn time (seconds). Lower = Faster.
        self.spawn_time = uniform(*self.spawn_period_range)

    def clear(self):
        self.list.clear()

    def update(self, dt, speed):
        self.timer += dt

        if self.timer >= self.spawn_time:
            kind = choice(["bike", "car2", "truck"])
            self.list.append(Obstacle(self.game, kind))
            self.timer = 0
            self.spawn_time = uniform(*self.spawn_period_range)

        for o in self.list[:]:
            o.update(dt, speed)
            if o.off_screen():
                self.list.remove(o)

    def draw(self):
        for o in self.list:
            o.draw()
