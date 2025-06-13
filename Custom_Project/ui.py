import pyglet

class HealthBar:
    def __init__(self, thief, x, y, width=200, height=20):
        self.thief = thief
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.background_bar = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, color=(100, 0, 0))
        self.foreground_bar = pyglet.shapes.Rectangle(self.x, self.y, self.width, self.height, color=(255, 0, 0))
        
        self.label = pyglet.text.Label(f'HEALTH: {self.thief.health}',
                                       font_name='Arial',
                                       font_size=14,
                                       x=self.x + self.width / 2,
                                       y=self.y + self.height / 2,
                                       anchor_x='center',
                                       anchor_y='center')

    def update(self):
        """Updates the health bar's width and text based on thief's health."""
        health_percentage = max(0, self.thief.health / 100.0)
        self.foreground_bar.width = self.width * health_percentage
        self.label.text = f'HEALTH: {int(self.thief.health)}'

    def draw(self):
        self.background_bar.draw()
        self.foreground_bar.draw()
        self.label.draw()
