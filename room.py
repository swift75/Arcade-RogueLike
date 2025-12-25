import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

ROOM_TYPES = ["enemy", "chest", "empty"]


class ExitPortal(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(80, 60, arcade.color.PURPLE)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT - 60
        self.active = True

    def update_color(self):
        self.color = arcade.color.PURPLE if self.active else arcade.color.GRAY


class Room:
    def __init__(self, room_type: str):
        self.type = room_type

        self.exit = ExitPortal()
        self.exit_list = arcade.SpriteList()
        self.exit_list.append(self.exit)

        if self.type == "enemy":
            self.exit.active = False
            self.exit.update_color()

        self.text = arcade.Text(
            f"ROOM: {self.type.upper()}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

    def draw(self):
        bg_color = {
            "start": arcade.color.DARK_BLUE,
            "enemy": arcade.color.DARK_RED,
            "chest": arcade.color.DARK_GREEN,
            "empty": arcade.color.DARK_GRAY
        }.get(self.type, arcade.color.BLACK)

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, bg_color
        )

        self.text.draw()
        self.exit.update_color()
        self.exit_list.draw()


class RoomManager:
    def __init__(self):
        self.current_room = Room("start")

    def next_room(self):
        self.current_room = Room(random.choice(ROOM_TYPES))

    def reset(self):
        self.current_room = Room("start")
