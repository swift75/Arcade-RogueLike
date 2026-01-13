import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Enemy(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(50, 50, arcade.color.RED)
        self.center_x = random.randint(150, SCREEN_WIDTH - 150)
        self.center_y = random.randint(200, SCREEN_HEIGHT - 200)

    def draw_label(self):
        arcade.draw_text(
            "ENEMY",
            self.center_x,
            self.center_y + 35,
            arcade.color.WHITE,
            12,
            anchor_x="center"
        )
