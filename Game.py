import pyglet as py
from pyglet.window import key
from pyglet import text, shapes
from Car import Car
from Obstacles import ObstacleManager
from Utils import aabb, ROAD_PADDING
import math

window = py.window.Window(1280, 720)

class Game:
    def __init__(self):
        self.window_width = window.width
        self.window_height = window.height
        
        self.road = py.image.load("images/road.png")

        self.road_left = (window.width - self.road.width) // 2 + ROAD_PADDING
        self.road_right = ((window.width - self.road.width) // 2 + self.road.width) - ROAD_PADDING

        self.left_boundary = shapes.Line(
            self.road_left, 0, self.road_left, window.height, color=(255, 0, 0)
        )
        self.left_boundary.width = 2
        
        self.right_boundary = shapes.Line(
            self.road_right, 0, self.road_right, window.height, color=(255, 0, 0)
        )
        self.right_boundary.width = 2

        self.scroll_y = 0
        self.base_speed = 200
        self.speed = self.base_speed # State: Speed of the game (affects obstacle speed and car lat movement)
        self.max_speed = 350
        self.min_speed = 120

        self.car = Car(self)
   
        self.obstacles = ObstacleManager(self)
        
        self.score = 0 # Reward: accumulated time survived
        self.game_over = False # Terminal State: True if collision occurs

        self.sensors = [] # State: Distances to nearest 5 obstacles
        self.sensor_lines = []
        self.sensor_labels = [] 


        self.score_label = text.Label(
            "Score: 0", x=10, y=window.height - 30
        )
        self.game_over_label = text.Label(
            "CRASHED!", font_size=48,
            x=window.width // 2, y=window.height // 2 + 40,
            anchor_x="center", anchor_y="center"
        )
        self.restart_label = text.Label(
            "Press R to Restart", font_size=20,
            x=window.width // 2, y=window.height // 2 - 20,
            anchor_x="center", anchor_y="center"
        )

    def reset(self):
        self.scroll_y = 0
        self.speed = self.base_speed
        self.score = 0
        self.game_over = False
        self.obstacles.clear()
        self.car.reset()

    def update(self, dt):
        if self.game_over:
            return

        self.scroll_y -= self.speed * dt
        self.scroll_y %= self.road.height


        self.car.update(dt)
        self.obstacles.update(dt, self.speed)

        for obs in self.obstacles.list:
            if aabb(self.car.get_hitbox(), obs.get_hitbox()):
                self.game_over = True
        

        cx, cy, cw, ch = self.car.get_hitbox()
        if cx < self.road_left or cx + cw > self.road_right:
            self.game_over = True


        self.sensors = []
        self.sensor_lines = []
        self.sensor_labels = []
        
        distances = []
        for obs in self.obstacles.list:
            dx = obs.x - self.car.x
            dy = obs.y - self.car.y
            dist = math.sqrt(dx*dx + dy*dy)
            distances.append((dist, obs))
        
        distances.sort(key=lambda x: x[0])
        
        nearest_5 = distances[:5]
        
        for dist, obs in nearest_5:
            self.sensors.append(dist)
            
            color = (0, 255, 0) # Green
            if dist < 200:
                color = (255, 0, 0) # Red
            
            line = shapes.Line(self.car.x, self.car.y, obs.x, obs.y, color=color)
            line.width = 2
            self.sensor_lines.append(line)
            
            label = text.Label(
                f"{int(dist)}",
                font_size=10,
                x=(self.car.x + obs.x) // 2,
                y=(self.car.y + obs.y) // 2 + 10,
                anchor_x="center", anchor_y="center"
            )
            self.sensor_labels.append(label)

        while len(self.sensors) < 5:
            self.sensors.append(1000.0) 

        self.score += dt
        self.score_label.text = f"Score: {int(self.score)}"

    def draw(self):
        window.clear()

        x = (window.width - self.road.width) // 2
        y = self.scroll_y
        self.road.blit(x, y - self.road.height)
        self.road.blit(x, y)
        self.road.blit(x, y + self.road.height)
        
        self.left_boundary.draw()
        self.right_boundary.draw()

        self.obstacles.draw()
        self.car.draw()
        
        for line in self.sensor_lines:
            line.draw()
        for label in self.sensor_labels:
            label.draw()
        self.score_label.draw()
        if self.game_over:
            self.game_over_label.draw()
            self.restart_label.draw()


game = Game()

@window.event
def on_key_press(symbol, modifiers):
    if game.game_over:
        if symbol == key.R:
            game.reset()
        return

    if symbol == key.LEFT:
        game.car.move_left()
    elif symbol == key.RIGHT:
        game.car.move_right()
    elif symbol == key.UP:
        game.car.accelerate()
    elif symbol == key.DOWN:
        game.car.brake()

@window.event
def on_draw():
    game.draw()

if __name__ == "__main__":
    py.clock.schedule_interval(game.update, 1/60)
    py.app.run()
