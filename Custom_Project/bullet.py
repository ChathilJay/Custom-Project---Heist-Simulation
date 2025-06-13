import pyglet
import math

class Bullet:
    def __init__(self, x, y, dir_x, dir_y, world, thief):
        self.x = x
        self.y = y
        self.world = world
        self.thief = thief
        self.speed = 300
        self.velocity_x = dir_x * self.speed
        self.velocity_y = dir_y * self.speed
        self.shape = pyglet.shapes.Circle(self.x, self.y, 5, color=(255, 165, 0))
        self.life = 2.0 # Bullet lives for 2 seconds
        self.dead = False

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.shape.x = self.x
        self.shape.y = self.y
        
        self.life -= dt
        if self.life <= 0:
            self.dead = True

        # Collision with walls
        if self.world.is_wall(self.x, self.y):
            self.dead = True
            
        # Collision with thief
        dist_to_thief = math.sqrt((self.x - self.thief.x)**2 + (self.y - self.thief.y)**2)
        if dist_to_thief < 15: # 15 is thief's radius
            print("Thief hit!")
            self.thief.health -= 20
            self.dead = True
    
    def draw(self):
        self.shape.draw()
