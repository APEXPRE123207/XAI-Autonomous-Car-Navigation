import pyglet.shapes as shapes
import math
from Utils import PHYSICAL_SIZE, LANE_Y

class Car:
    def __init__(self, game):
        self.game = game
        
        road_width = game.road.width
        
        self.x = (self.game.road_left + self.game.road_right) / 2 # State: Lateral position of the car (0 to road_width)
        self.y = LANE_Y # State: Vertical position (constant for player)

        self.target_x = self.x
        
        self.turn_angle = 0
        self.max_turn = 25 
        self.steer_response = 10.0
        self.movement_step = 10.0 

        width, height = PHYSICAL_SIZE["car"]
        self.shape = shapes.Rectangle(
            x=self.x, y=self.y,
            width=width, height=height,
            color=(50, 50, 255) 
        )
        self.shape.anchor_x = width // 2
        self.shape.anchor_y = height // 2
        self.shape.rotation = 0

    def reset(self):
        self.x = (self.game.road_left + self.game.road_right) / 2
        self.target_x = self.x
        self.turn_angle = 0
        self.shape.rotation = 0

    def update(self, dt):
        dx = self.target_x - self.x
        desired_angle = dx * 0.2 
        desired_angle = max(-self.max_turn, min(self.max_turn, desired_angle))

        diff = desired_angle - self.turn_angle
        self.turn_angle += diff * self.steer_response * dt

        rad = math.radians(self.turn_angle)
        LATERAL_MULTIPLIER = 1.5 
        movement_x = self.game.speed * math.sin(rad) * LATERAL_MULTIPLIER * dt
        self.x += movement_x

        self.shape.x = self.x
        self.shape.y = self.y
        self.shape.rotation = self.turn_angle 

    def move_left(self): # Action: Move car left
        self.target_x -= self.movement_step
        self.target_x = max(self.game.road_left, self.target_x)

    def move_right(self): # Action: Move car right
        self.target_x += self.movement_step
        self.target_x = min(self.game.road_right, self.target_x)

    def accelerate(self): # Action: Increase speed
        self.game.speed = min(self.game.speed + 30, self.game.max_speed)

    def brake(self): # Action: Decrease speed
        self.game.speed = max(self.game.speed - 30, self.game.min_speed)

    def get_hitbox(self):
        w, h = PHYSICAL_SIZE["car"]
        return (self.x - w/2, self.y - h/2, w, h)

    def draw(self):
        self.shape.draw()
