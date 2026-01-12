import arcade
import random
import sqlite3
from enemy import Enemy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

DB_NAME = "rooms.db"

ROOM_WEIGHTS = [
    ("enemy", 0.35),
    ("empty", 0.4),
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


class ExitPortal(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(80, 60, arcade.color.PURPLE)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT - 60
        self.active = True

    def update_color(self):
        self.color = arcade.color.PURPLE if self.active else arcade.color.GRAY


class Chest(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(50, 40, arcade.color.GOLD)
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2


class Room:
    def __init__(self, room_type, number, cleared=False, chest_opened=False):
        self.number = number
        self.type = room_type
        self.cleared = cleared
        self.chest_opened = chest_opened

        self.exit = ExitPortal()
        self.exit_list = arcade.SpriteList()
        self.exit_list.append(self.exit)

        self.enemies = arcade.SpriteList()
        self.chest_list = arcade.SpriteList()
        self.chest = None

        if self.type == "enemy":
            if not self.cleared:
                self.enemies.append(Enemy())
                self.exit.active = False
            else:
                self.exit.active = True

        elif self.type == "empty":
            self.exit.active = True

        elif self.type == "chest":
            if not self.chest_opened:
                self.chest = Chest()
                self.chest_list.append(self.chest)
                self.exit.active = False
            else:
                self.exit.active = True

        self.text = arcade.Text(
            f"ROOM #{self.number} — {self.type.upper()}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

    def draw(self):
        bg = {
            "start": arcade.color.DARK_BLUE,
            "enemy": arcade.color.DARK_RED,
            "chest": arcade.color.DARK_GREEN,
            "empty": arcade.color.DARK_GRAY,
        }.get(self.type, arcade.color.BLACK)

        arcade.draw_lrbt_rectangle_filled(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, bg)
        self.text.draw()

        if self.enemies:
            self.enemies.draw()
            for e in self.enemies:
                e.draw_label()

        if self.type == "chest" and not self.chest_opened:
            self.chest_list.draw()

        self.exit.update_color()
        self.exit_list.draw()


class RoomManager:
    def __init__(self):
        self.start_room = Room("start", 0)
        self.rooms = []
        self.current_index = 0
        self.current_room = self.start_room
        self._init_db()
        self._load_rooms()

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
            Room(
                r[1],
                r[0],
                cleared=bool(r[2]),
                chest_opened=bool(r[3])
            )
            for r in rows
        ]

        self.current_index = 0
        self.current_room = self.start_room

    def _save_room(self, room):
        con = sqlite3.connect(DB_NAME)
        cur = con.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO rooms
            (pos, type, cleared, chest_opened)
            VALUES (?, ?, ?, ?)
        """, (
            room.number,
            room.type,
            int(room.cleared),
            int(room.chest_opened)
        ))
        con.commit()
        con.close()

    def start_new_run(self):
        if not self.rooms:
            t = random_room_type()
            room = Room(t, 1)
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
        room_number = self.current_index + 1

        if self.current_index < len(self.rooms):
            self.current_room = self.rooms[self.current_index]
        else:
            t = random_room_type()
            room = Room(t, room_number)
            self.rooms.append(room)
            self._save_room(room)
            self.current_room = room

    def go_to_start(self):
        self.current_room = self.start_room
