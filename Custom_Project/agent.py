import pyglet
import math
from fsm import GuardFSM
from pathfinding import a_star_search
from bullet import Bullet
from pyglet import graphics



class Agent:
    def __init__(self, x, y, world):
        self.x = x
        self.y = y
        self.world = world
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 100
        self.shape = pyglet.shapes.Circle(self.x, self.y, 15, color=(0, 0, 255))
        self.path = []

    def update(self, dt):
        next_x = self.x + self.velocity_x * dt
        next_y = self.y + self.velocity_y * dt

        if not self.world.is_wall(next_x, next_y):
            self.x = next_x
            self.y = next_y

        self.shape.x = self.x
        self.shape.y = self.y

    def draw(self):
        self.shape.draw()

class ThiefAgent(Agent):
    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.shape.color = (0, 255, 0)  # Green for the thief
        self.keys = {}
        self.health = 100
        self.auto_mode = False
        self.escaping = False


    def handle_key_press(self, symbol, modifiers):
        self.keys[symbol] = True
        if symbol == pyglet.window.key.A:
            self.auto_mode = not self.auto_mode
            if self.auto_mode:
                self.find_path_to_gem()
            else:
                self.velocity_x = 0
                self.velocity_y = 0

    def handle_key_release(self, symbol, modifiers):
        if symbol in self.keys:
            del self.keys[symbol]
            
        if symbol == pyglet.window.key.T:
            self.auto_mode = not self.auto_mode
            print(f"[Thief] Auto Mode: {self.auto_mode}")
            if self.auto_mode:
                self.find_path_to_gem()
                print(f"[Thief] Path to Gem: {self.path}")
            else:
                self.velocity_x = 0
                self.velocity_y = 0


    def find_path_to_gem(self):
        start = (int(self.x / self.world.tile_size), int((self.world.height - self.y) / self.world.tile_size))
        end = (int(self.world.gem_pos[0] / self.world.tile_size), int((self.world.height - self.world.gem_pos[1]) / self.world.tile_size))
        self.path = a_star_search(self.world.map, start, end)

    def update(self, dt):
        if self.auto_mode:
            # Flee if guard is too close
            dist_to_guard = math.hypot(self.world.guard.x - self.x, self.world.guard.y - self.y)
            if dist_to_guard < 150:
                self.recalculate_escape_path()
            elif self.path:
                self.follow_path_to_gem()
            else:
                self.velocity_x = 0
                self.velocity_y = 0
        else:  # Manual control
            self.velocity_x = 0
            self.velocity_y = 0
            if pyglet.window.key.LEFT in self.keys:
                self.velocity_x = -self.speed
            if pyglet.window.key.RIGHT in self.keys:
                self.velocity_x = self.speed
            if pyglet.window.key.UP in self.keys:
                self.velocity_y = self.speed
            if pyglet.window.key.DOWN in self.keys:
                self.velocity_y = -self.speed
                
        if self.auto_mode:
            dist_to_guard = math.hypot(self.world.guard.x - self.x, self.world.guard.y - self.y)

            if dist_to_guard < 150 and not self.escaping:
                self.escaping = True
                self.recalculate_escape_path()

            if self.escaping:
                if dist_to_guard > 200:
                    print("[Thief] Guard far enough, resuming normal path")
                    self.escaping = False
                    self.find_path_to_gem()
                elif self.path:
                    self.follow_path_to_gem()
                else:
                    self.velocity_x = 0
                    self.velocity_y = 0
            else:
                if self.path:
                    self.follow_path_to_gem()
                else:
                    self.velocity_x = 0
                    self.velocity_y = 0

        super().update(dt)

    def follow_path_to_gem(self):
        if self.path:
            target_node = self.path[0]
            target_x = target_node[0] * self.world.tile_size + self.world.tile_size / 2
            target_y = self.world.height - (target_node[1] * self.world.tile_size + self.world.tile_size / 2)

            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < 5:
                self.path.pop(0)
            else:
                self.velocity_x = (dx / dist) * self.speed
                self.velocity_y = (dy / dist) * self.speed

    def recalculate_escape_path(self):
        thief_tile = (
            int(self.x / self.world.tile_size),
            int((self.world.height - self.y) / self.world.tile_size)
        )
        gem_tile = (
            int(self.world.gem_pos[0] / self.world.tile_size),
            int((self.world.height - self.world.gem_pos[1]) / self.world.tile_size)
        )
        guard_tile = (
            int(self.world.guard.x / self.world.tile_size),
            int((self.world.height - self.world.guard.y) / self.world.tile_size)
        )

        # Clone the map and block off guard area
        temp_map = [list(row) for row in self.world.map]
        gx, gy = guard_tile
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = gx + dx, gy + dy
                if 0 <= ny < len(temp_map) and 0 <= nx < len(temp_map[0]):
                    temp_map[ny][nx] = 'W'

        new_path = a_star_search(temp_map, thief_tile, gem_tile)
        if new_path:
            self.path = new_path
            print(f"[Thief] Recalculated escape path from {thief_tile} to gem avoiding {guard_tile}")
        else:
            print("[Thief] No escape path found — stopping")
            self.path = []
            self.velocity_x = 0
            self.velocity_y = 0

class GuardAgent(Agent):
    def __init__(self, x, y, world, thief):
        super().__init__(x, y, world)
        self.shape.color = (255, 0, 0)  # Red for the guard
        self.thief = thief
        self.fsm = GuardFSM(self)
        self.speed = 80
        self.shoot_cooldown = 0

    def update(self, dt):
        self.fsm.update(dt)
        super().update(dt)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

    def shoot(self):
        if self.shoot_cooldown <= 0:
            dx = self.thief.x - self.x
            dy = self.thief.y - self.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > 0:
                dir_x = dx / dist
                dir_y = dy / dist
                bullet = Bullet(self.x, self.y, dir_x, dir_y, self.world, self.thief)
                self.world.bullets.append(bullet)
                self.shoot_cooldown = 2  # 2 seconds cooldown
                
    def draw_vision_cone(self):
        range_radius = 180
        angle = math.atan2(self.thief.y - self.y, self.thief.x - self.x)
        cone_angle = math.radians(40)
        num_points = 12

        points = [(self.x, self.y)]  # Apex of cone

        for i in range(num_points + 1):
            theta = angle - cone_angle / 2 + cone_angle * (i / num_points)
            px = self.x + range_radius * math.cos(theta)
            py = self.y + range_radius * math.sin(theta)
            points.append((px, py))

        
        vision_shape = pyglet.shapes.Polygon(*points, color=(255, 255, 0))
        vision_shape.opacity = 50
        vision_shape.draw()


    def draw(self):
        self.draw_vision_cone()
        self.shape.draw()

