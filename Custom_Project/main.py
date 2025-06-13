import pyglet
from world import World

class GameWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_minimum_size(600, 400)
        
        # Game world
        self.world = World('map.txt', self.get_size())

        # Schedule the update function
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def on_draw(self):
        """Clears the window and draws the game world."""
        self.clear()
        self.world.draw()

    def update(self, dt):
        """Updates the game state."""
        self.world.update(dt)
        if self.world.game_over:
            pyglet.clock.unschedule(self.update)
            self.show_game_over()
        elif self.world.win:
            pyglet.clock.unschedule(self.update)
            self.show_win_screen()


    def on_key_press(self, symbol, modifiers):
        """Handles key presses for thief control."""
        if not self.world.game_over and not self.world.win:
            self.world.thief.handle_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        """Handles key releases for thief control."""
        if not self.world.game_over and not self.world.win:
            self.world.thief.handle_key_release(symbol, modifiers)
            
    def on_mouse_press(self, x, y, button, modifiers):
        if self.world.restart_visible:
            if (self.world.restart_button.x <= x <= self.world.restart_button.x + self.world.restart_button.width and
                self.world.restart_button.y <= y <= self.world.restart_button.y + self.world.restart_button.height):
                print("[UI] Restart clicked — restarting game")
                self.restart_game()

    def restart_game(self):
        self.world = World('map.txt', self.get_size())
        pyglet.clock.schedule_interval(self.update, 1/60.0)


    def show_game_over(self):
        """Displays the 'Game Over' message."""
        label = pyglet.text.Label('GAME OVER',
                                  font_name='Arial',
                                  font_size=36,
                                  x=self.width // 2, y=self.height // 2,
                                  anchor_x='center', anchor_y='center')
        label.draw()

    def show_win_screen(self):
        """Displays the 'You Win!' message."""
        label = pyglet.text.Label('YOU WIN!',
                                  font_name='Arial',
                                  font_size=36,
                                  x=self.width // 2, y=self.height // 2,
                                  anchor_x='center', anchor_y='center')
        label.draw()


if __name__ == '__main__':
    window = GameWindow(900, 700, "Heist Simulation", resizable=True)
    pyglet.app.run()
