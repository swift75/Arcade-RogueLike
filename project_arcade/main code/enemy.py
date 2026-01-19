import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ENEMY_DATA = {
    "fly": {
        "color": arcade.color.LIGHT_GRAY,
        "hp": 20,
        "attack": 4,
        "defense": 1,
    },
    "goblin": {
        "color": arcade.color.GREEN,
        "hp": 45,
        "attack": 9,
        "defense": 4,
    },
    "skeleton": {
        "color": arcade.color.BONE,
        "hp": 40,
        "attack": 10,
        "defense": 3,
    },
    "mushroom": {
        "color": arcade.color.RED_ORANGE,
        "hp": 80,
        "attack": 15,
        "defense": 7,
    },
}


class Enemy(arcade.SpriteSolidColor):
    def __init__(self, lvl, final_multiplier=1.0):
        self.enemy_type = random.choice(list(ENEMY_DATA.keys()))
        data = ENEMY_DATA[self.enemy_type]

        super().__init__(50, 50, data["color"])

        self.center_x = random.randint(150, SCREEN_WIDTH - 150)
        self.center_y = random.randint(200, SCREEN_HEIGHT - 200)

        coef = 1 + lvl / 10

        self.max_hp = max(1, int(data["hp"] * coef * final_multiplier))
        self.hp = self.max_hp
        self.attack = max(1, int(data["attack"] * coef * final_multiplier))
        self.defense = max(0, int(data["defense"] * coef * final_multiplier))

    def draw_label(self):
        arcade.draw_text(
            self.enemy_type.upper(),
            self.center_x,
            self.center_y + 35,
            arcade.color.WHITE,
            12,
            anchor_x="center"
        )
