import arcade
import random
from animations import Fly, Goblin, Skeleton, Mushroom

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


ENEMY_CLASSES = {
    "fly": Fly,
    "goblin": Goblin,
    "skeleton": Skeleton,
    "mushroom": Mushroom,
}


SPAWN_SLOTS = [
    SCREEN_WIDTH // 2 - 140,
    SCREEN_WIDTH // 2,
    SCREEN_WIDTH // 2 + 140,
]


class Enemy(arcade.Sprite):
    spawn_index = 0

    def __init__(self, lvl: int, final_multiplier: float = 1.0):
        super().__init__()

        self.enemy_type = random.choice(list(ENEMY_DATA.keys()))
        data = ENEMY_DATA[self.enemy_type]

        x = SPAWN_SLOTS[Enemy.spawn_index % len(SPAWN_SLOTS)]
        Enemy.spawn_index += 1
        y = SCREEN_HEIGHT // 2 + 80

        enemy_class = ENEMY_CLASSES[self.enemy_type]
        animated = enemy_class(x, y)

        self.textures = animated.textures_idle
        self.texture = animated.texture
        self.scale = animated.scale

        self.center_x = x
        self.center_y = y

        self.current_texture = 0
        self.timer = 0.0
        self.anim_speed = animated.speed

        coef = 1 + lvl / 10
        self.max_hp = max(1, int(data["hp"] * coef * final_multiplier))
        self.hp = self.max_hp
        self.attack = max(1, int(data["attack"] * coef * final_multiplier))
        self.defense = max(0, int(data["defense"] * coef * final_multiplier))

    def update_animation(self, delta_time: float):
        self.timer += delta_time
        if self.timer >= self.anim_speed:
            self.timer = 0
            self.current_texture = (self.current_texture + 1) % len(self.textures)
            self.texture = self.textures[self.current_texture]

    def draw_label(self):
        arcade.draw_text(
            self.enemy_type.upper(),
            self.center_x,
            self.center_y + 45,
            arcade.color.WHITE,
            12,
            anchor_x="center"
        )
