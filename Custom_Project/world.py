import pyglet
from pathfinding import a_star_search
from agent import ThiefAgent, GuardAgent
from ui import HealthBar
from graphics import COLOUR_NAMES

class World:
    def __init__(self, map_file, window_size):
        self.tile_size = 40
        self.map = self.load_map(map_file)
        self.width = len(self.map[0]) * self.tile_size
        self.height = len(self.map) * self.tile_size
        self.window_size = window_size
        
        self.batch = pyglet.graphics.Batch()
        self.walls = self.create_wall_shapes()
        self.gem_pos = self.find_gem_position()

        # Game objects
        self.thief = ThiefAgent(x=60, y=60, world=self)
        self.guard = GuardAgent(x=self.width - 60, y=self.height - 60, world=self, thief=self.thief)
        
        self.bullets = []
        self.health_bar = HealthBar(self.thief, 10, self.window_size[1] - 30)

        # Game state
        self.game_over = False
        self.win = False

        # Guard state label
        self.guard_state_label = pyglet.text.Label(
            'Guard State: Unknown',
            font_name='Courier New',
            font_size=14,
            x=self.window_size[0] - 20,
            y=self.window_size[1] - 20,
            anchor_x='right',
            anchor_y='top',
            color=(255, 255, 255, 255),
            batch=None
        )

        self.labels = {}
        self.labels['VICTORY'] = pyglet.text.Label(
            "YOU WIN!",
            font_name='Courier New',
            font_size=72,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x='center',
            anchor_y='center',
            color=COLOUR_NAMES['GREEN']
        )
        self.labels['VICTORY'].visible = False

        self.labels['LOSS'] = pyglet.text.Label(
            "YOU LOSE!",
            font_name='Courier New',
            font_size=72,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x='center',
            anchor_y='center',
            color=COLOUR_NAMES['RED']
        )
        self.labels['LOSS'].visible = False
        
        self.restart_button = pyglet.shapes.Rectangle(
            x=self.width - 150,
            y=20,
            width=130,
            height=40,
            color=(100, 100, 100),
            batch=self.batch
        )
        self.restart_label = pyglet.text.Label(
            "RESTART",
            font_name='Courier New',
            font_size=14,
            x=self.width - 85,
            y=40,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            batch=None  # <- FIXED HERE
        )
        self.restart_visible = False
        
        self.control_mode_label = pyglet.text.Label(
            'Thief: Manual',
            font_name='Courier New',
            font_size=14,
            x=self.window_size[0] - 20,      
            y=self.window_size[1] - 40,    
            anchor_x='right',
            anchor_y='top',
            color=(255, 255, 255, 255)
        )


    def load_map(self, map_file):
        with open(map_file, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def create_wall_shapes(self):
        walls = []
        for r, row in enumerate(self.map):
            for c, tile in enumerate(row):
                if tile == 'W':
                    x1 = c * self.tile_size
                    y1 = self.height - (r + 1) * self.tile_size
                    walls.append(pyglet.shapes.Rectangle(
                        x1, y1, self.tile_size, self.tile_size, color=(50, 50, 50), batch=self.batch))
        return walls

    def find_gem_position(self):
        for r, row in enumerate(self.map):
            for c, tile in enumerate(row):
                if tile == 'G':
                    return (c * self.tile_size + self.tile_size / 2,
                            self.height - (r * self.tile_size + self.tile_size / 2))
        return None

    def is_wall(self, x, y):
        grid_x, grid_y = int(x / self.tile_size), int((self.height - y) / self.tile_size)
        if 0 <= grid_y < len(self.map) and 0 <= grid_x < len(self.map[0]):
            return self.map[grid_y][grid_x] == 'W'
        return True

    def update(self, dt):
        self.thief.update(dt)
        self.guard.update(dt)
        self.guard_state_label.text = f"Guard State: {self.guard.fsm.current_state.__class__.__name__}"

        for bullet in self.bullets[:]:
            bullet.update(dt)
            if bullet.dead:
                self.bullets.remove(bullet)

        self.health_bar.update()

        if self.thief.health <= 0:
            self.game_over = True
            self.labels['LOSS'].visible = True
            self.restart_visible = True

        dist_to_gem = ((self.thief.x - self.gem_pos[0])**2 + (self.thief.y - self.gem_pos[1])**2)**0.5
        if dist_to_gem < self.tile_size / 2:
            self.win = True
            self.labels['VICTORY'].visible = True
            self.restart_visible = True
            
        self.control_mode_label.text = f"Thief State: {'Auto State' if self.thief.auto_mode else 'Manual State'}"


    def draw(self):
        self.batch.draw()

        if not self.win and self.gem_pos:
            pyglet.shapes.Circle(self.gem_pos[0], self.gem_pos[1], 10, color=(0, 255, 255)).draw()

        for label in self.labels.values():
            if label.visible:
                label.draw()

        self.thief.draw()
        self.guard.draw()

        for bullet in self.bullets:
            bullet.draw()

        self.guard_state_label.draw()
        self.health_bar.draw()

        if self.restart_visible:
            self.restart_button.draw()
            self.restart_label.draw()
            
        self.control_mode_label.draw()

