import arcade
import random
import sqlite3
import sys
import os

from enemy import Enemy
from items import roll_item
arcade.load_font("minecraft.ttf")
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
START_BG_TEXTURE = arcade.load_texture("start_room.jpg")
MAIN_BG_TEXTURE = arcade.load_texture("main_room.jpg")
DB_NAME = "rooms.db"

ROOM_WEIGHTS = [
    ("enemy", 0.45),
    ("empty", 0.3),
    ("chest", 0.25),
]


def random_room_type():
    r = random.random()
    s = 0
    for t, w in ROOM_WEIGHTS:
        s += w
        if r <= s:
            return t
    return "enemy"

class Portal(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(70, 50, (0, 0, 0, 0))
        self.center_x = x
        self.center_y = y
        self.active = True

    def update_color(self):
        pass



class Chest(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("Chest.png")
        self.scale = 0.15
        self.center_x = SCREEN_WIDTH // 2 - 140
        self.center_y = SCREEN_HEIGHT // 2
        self.item = roll_item()

    def open_chest(self):
        self.chest_opened = True
        self.chest_ui_active = True




class Room:
    def __init__(self, room_type, number, cleared=False, chest_opened=False):
        self.type = room_type
        self.number = number
        self.cleared = cleared
        self.chest_opened = chest_opened
        self.chest_ui_active = False

        self.enemies = arcade.SpriteList()
        self.chest_list = arcade.SpriteList()
        self.walls = arcade.SpriteList()

        self.create_walls()

        self.exit_forward = Portal(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60)
        self.exit_back = Portal(SCREEN_WIDTH // 2, 60)

        self.portal_list = arcade.SpriteList()
        self.portal_list.append(self.exit_forward)
        if self.number > 0:
            self.portal_list.append(self.exit_back)

        if self.type == "enemy" and not self.cleared:
            enemy_count = random.randint(1, 3)
            mult = 1 / 3 if enemy_count == 1 else 1 / 2 if enemy_count == 2 else 1
            for _ in range(enemy_count):
                self.enemies.append(Enemy(self.number, mult))
            self.exit_forward.active = False

        if self.type == "chest" and not self.chest_opened:
            self.chest_list.append(Chest())
            self.exit_forward.active = False

        bg_texture = START_BG_TEXTURE if self.type == "start" else MAIN_BG_TEXTURE
        self.bg_sprite = arcade.Sprite()
        self.bg_sprite.texture = bg_texture
        self.bg_sprite.center_x = SCREEN_WIDTH // 2
        self.bg_sprite.center_y = SCREEN_HEIGHT // 2
        self.bg_sprite.scale = max(
            SCREEN_WIDTH / bg_texture.width,
            SCREEN_HEIGHT / bg_texture.height
        )

        self.text = arcade.Text(
            f"Комната {self.number} — {self.type.upper()}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20,
            font_name="Minecraft Rus"
        )

    def create_walls(self):
        self.walls.clear()
        thickness = 40

        if self.type == "start":
            top = arcade.SpriteSolidColor(520, thickness, (0, 0, 0, 0))
            top.center_x = SCREEN_WIDTH // 2
            top.center_y = SCREEN_HEIGHT // 2 + 260
            self.walls.append(top)

            bottom = arcade.SpriteSolidColor(520, thickness, (0, 0, 0, 0))
            bottom.center_x = SCREEN_WIDTH // 2
            bottom.center_y = SCREEN_HEIGHT // 2 - 180
            self.walls.append(bottom)

            left = arcade.SpriteSolidColor(thickness, 360, (0, 0, 0, 0))
            left.center_x = SCREEN_WIDTH // 2 - 182
            left.center_y = SCREEN_HEIGHT // 2
            self.walls.append(left)

            right = arcade.SpriteSolidColor(thickness, 360, (0, 0, 0, 0))
            right.center_x = SCREEN_WIDTH // 2 + 182
            right.center_y = SCREEN_HEIGHT // 2
            self.walls.append(right)

        else:
            top = arcade.SpriteSolidColor(720, thickness, (0, 0, 0, 0))
            top.center_x = SCREEN_WIDTH // 2
            top.center_y = SCREEN_HEIGHT // 2 + 260
            self.walls.append(top)

            bottom = arcade.SpriteSolidColor(720, thickness, (0, 0, 0, 0))
            bottom.center_x = SCREEN_WIDTH // 2
            bottom.center_y = SCREEN_HEIGHT // 2 - 245
            self.walls.append(bottom)

            left = arcade.SpriteSolidColor(thickness, 520, (0, 0, 0, 0))
            left.center_x = SCREEN_WIDTH // 2 - 250
            left.center_y = SCREEN_HEIGHT // 2
            self.walls.append(left)

            right = arcade.SpriteSolidColor(thickness, 520, (0, 0, 0, 0))
            right.center_x = SCREEN_WIDTH // 2 + 250
            right.center_y = SCREEN_HEIGHT // 2
            self.walls.append(right)

    def draw(self):
        arcade.draw_sprite(self.bg_sprite)
        self.text.draw()
        self.enemies.draw()
        for e in self.enemies:
            e.draw_label()
        self.chest_list.draw()



    def draw_chest_ui(self):
        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH // 2 - 200, SCREEN_WIDTH // 2 + 200,
            SCREEN_HEIGHT // 2 - 150, SCREEN_HEIGHT // 2 + 150,
            (0, 0, 0, 180)
        )

        arcade.draw_text(
            "Вы открыли сундук!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 60,
            arcade.color.WHITE,
            20,
            font_name='Minecraft Rus',
            anchor_x="center",
            anchor_y="center"
        )

        item_name = self.chest_list[0].item[1]
        item_description = self.chest_list[0].item[3]

        arcade.draw_text(
            f"Предмет: {item_name}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            18,
            font_name='Minecraft Rus',
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            f"Описание: {item_description}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 30,
            arcade.color.WHITE,
            14,
            font_name='Minecraft Rus',
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH // 2 - 80, SCREEN_WIDTH // 2 + 80,
            SCREEN_HEIGHT // 2 - 100, SCREEN_HEIGHT // 2 - 70,
            arcade.color.DARK_RED
        )

        arcade.draw_text(
            "Закрыть",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 85,
            arcade.color.WHITE,
            16,
            font_name='Minecraft Rus',
            anchor_x="center",
            anchor_y="center"
        )


class RoomManager:
    def __init__(self):
        self.start_room = Room("start", 0)
        self.rooms = []
        self.current_index = -1
        self.current_room = self.start_room
        self._init_db()
        self._load_rooms()

    def go_to_start(self):
        self.current_index = -1
        self.current_room = self.start_room

    def _init_db(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                pos INTEGER PRIMARY KEY,
                type TEXT,
                cleared INTEGER,
                chest_opened INTEGER
            )
        """)
        con.commit()
        con.close()

    def _load_rooms(self):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        rows = cur.execute(
            "SELECT pos, type, cleared, chest_opened FROM rooms ORDER BY pos"
        ).fetchall()
        con.close()

        self.rooms = [
            Room(r[1], r[0], bool(r[2]), bool(r[3]))
            for r in rows
        ]

    def _save_room(self, room):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO rooms
            (pos, type, cleared, chest_opened)
            VALUES (?, ?, ?, ?)
        """, (room.number, room.type, int(room.cleared), int(room.chest_opened)))
        con.commit()
        con.close()

    def start_new_run(self):
        if not self.rooms:
            room = Room(random_room_type(), 1)
            self.rooms.append(room)
            self._save_room(room)

        self.current_index = 0
        self.current_room = self.rooms[0]

    def continue_run(self):
        if not self.rooms:
            self.start_new_run()
        else:
            self.current_index = len(self.rooms) - 1
            self.current_room = self.rooms[self.current_index]

    def next_room(self):
        self.current_index += 1
        number = self.current_index + 1

        if self.current_index < len(self.rooms):
            self.current_room = self.rooms[self.current_index]
        else:
            room = Room(random_room_type(), number)
            self.rooms.append(room)
            self._save_room(room)
            self.current_room = room

    def previous_room(self):
        if self.current_index == 0:
            self.go_to_start()
        elif self.current_index > 0:
            self.current_index -= 1
            self.current_room = self.rooms[self.current_index]
