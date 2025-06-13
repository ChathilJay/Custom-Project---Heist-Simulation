import math
from pathfinding import a_star_search

class GuardFSM:
    def __init__(self, guard):
        self.guard = guard
        self.states = {
            'patrol': PatrolState(self),
            'chase': ChaseState(self)
        }
        self.current_state = self.states['patrol']
        self.current_state.enter()

    def change_state(self, state_name):
        print(f"[FSM] Guard changing from {self.current_state.name} to {state_name}")
        self.current_state.exit()
        self.current_state = self.states[state_name]
        self.current_state.enter()

    def update(self, dt):
        self.current_state.execute(dt)

class State:
    def __init__(self, fsm, name):
        self.fsm = fsm
        self.guard = fsm.guard
        self.name = name

    def enter(self): pass
    def execute(self, dt): pass
    def exit(self): pass

class PatrolState(State):
    def __init__(self, fsm):
        super().__init__(fsm, 'patrol')
        # Grid-based waypoints (col, row)
        self.waypoints = [(1, 1), (1, 10), (15, 10), (15, 1)]
        self.current_waypoint_index = 0
        self.path = []
        self.path_index = 0

    def enter(self):
        self.guard.speed = 80
        self.calculate_path_to_next_waypoint()

    def execute(self, dt):
        # Transition to chase if thief nearby
        dist_to_thief = math.hypot(self.guard.x - self.guard.thief.x, self.guard.y - self.guard.thief.y)
        if dist_to_thief < 200:
            self.fsm.change_state('chase')
            return

        # Move along A* path
        if self.path and self.path_index < len(self.path):
            tile = self.path[self.path_index]
            tile_x = tile[0] * self.guard.world.tile_size + self.guard.world.tile_size / 2
            tile_y = self.guard.world.height - (tile[1] * self.guard.world.tile_size + self.guard.world.tile_size / 2)

            dx = tile_x - self.guard.x
            dy = tile_y - self.guard.y
            dist = math.hypot(dx, dy)

            if dist < 5:
                self.path_index += 1
            else:
                self.guard.velocity_x = (dx / dist) * self.guard.speed
                self.guard.velocity_y = (dy / dist) * self.guard.speed
        else:
            self.current_waypoint_index = (self.current_waypoint_index + 1) % len(self.waypoints)
            self.calculate_path_to_next_waypoint()

    def calculate_path_to_next_waypoint(self):
        start_tile = (
            int(self.guard.x / self.guard.world.tile_size),
            int((self.guard.world.height - self.guard.y) / self.guard.world.tile_size)
        )
        end_tile = self.waypoints[self.current_waypoint_index]
        self.path = a_star_search(self.guard.world.map, start_tile, end_tile)
        self.path_index = 0

    def exit(self):
        self.guard.velocity_x = 0
        self.guard.velocity_y = 0

class ChaseState(State):
    def __init__(self, fsm):
        super().__init__(fsm, 'chase')

    def enter(self):
        print("[FSM] Guard entered Chase state.")
        self.guard.speed = 120

    def execute(self, dt):
        dist_to_thief = math.hypot(self.guard.x - self.guard.thief.x, self.guard.y - self.guard.thief.y)

        if dist_to_thief > 250:
            self.fsm.change_state('patrol')
            return

        dx = self.guard.thief.x - self.guard.x
        dy = self.guard.thief.y - self.guard.y
        if dist_to_thief > 0:
            self.guard.velocity_x = (dx / dist_to_thief) * self.guard.speed
            self.guard.velocity_y = (dy / dist_to_thief) * self.guard.speed

        if dist_to_thief < 180:
            self.guard.shoot()

    def exit(self):
        print("[FSM] Guard exited Chase state.")
        self.guard.velocity_x = 0
        self.guard.velocity_y = 0
