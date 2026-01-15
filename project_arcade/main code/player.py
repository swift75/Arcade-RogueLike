import arcade
import math
import sqlite3

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 6
DB_FILE = "player.db"


class Player:
    def __init__(self, x, y):
        self.sprite = arcade.SpriteSolidColor(40, 40, arcade.color.BLUE)
        self.sprite.center_x = x
        self.sprite.center_y = y

        self.change_x = 0
        self.change_y = 0

        self.level = 1
        self.exp = 0
        self.exp_to_next = 200

        self.max_hp = 100
        self.hp = 100
        self.attack = 12
        self.defense = 6
        self.luck = 3

        self.character_ui_active = False

        self.button_rect = (
            SCREEN_WIDTH - 110,
            SCREEN_WIDTH - 20,
            SCREEN_HEIGHT // 2 - 40,
            SCREEN_HEIGHT // 2 + 40
        )

        self.close_rect = (
            SCREEN_WIDTH // 2 + 180,
            SCREEN_WIDTH // 2 + 210,
            SCREEN_HEIGHT // 2 + 140,
            SCREEN_HEIGHT // 2 + 170
        )

        self.init_db()
        self.load_progress()

    def init_db(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY,
                level INTEGER,
                exp INTEGER,
                exp_to_next INTEGER,
                max_hp INTEGER,
                hp INTEGER,
                attack INTEGER,
                defense INTEGER,
                luck INTEGER
            )
        """)
        conn.commit()
        conn.close()

    def load_progress(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            SELECT level, exp, exp_to_next, max_hp, hp, attack, defense, luck
            FROM player WHERE id = 1
        """)
        row = cur.fetchone()
        if row:
            (
                self.level,
                self.exp,
                self.exp_to_next,
                self.max_hp,
                self.hp,
                self.attack,
                self.defense,
                self.luck
            ) = row
        else:
            cur.execute("""
                INSERT INTO player
                (id, level, exp, exp_to_next, max_hp, hp, attack, defense, luck)
                VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.level,
                self.exp,
                self.exp_to_next,
                self.max_hp,
                self.hp,
                self.attack,
                self.defense,
                self.luck
            ))
            conn.commit()
        conn.close()

    def save_progress(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            UPDATE player SET
                level = ?,
                exp = ?,
                exp_to_next = ?,
                max_hp = ?,
                hp = ?,
                attack = ?,
                defense = ?,
                luck = ?
            WHERE id = 1
        """, (
            self.level,
            self.exp,
            self.exp_to_next,
            self.max_hp,
            self.hp,
            self.attack,
            self.defense,
            self.luck
        ))
        conn.commit()
        conn.close()

    def set_position(self, x, y):
        self.sprite.center_x = x
        self.sprite.center_y = y

    def update(self):
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

        self.sprite.center_x = max(20, min(SCREEN_WIDTH - 20, self.sprite.center_x))
        self.sprite.center_y = max(20, min(SCREEN_HEIGHT - 20, self.sprite.center_y))

    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.exp_to_next = math.ceil(self.exp_to_next * 1.25)
            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 4
            self.defense += 3
            self.luck += 1
        self.save_progress()

    def on_key_press(self, key):
        if key == arcade.key.W:
            self.change_y = PLAYER_SPEED
        elif key == arcade.key.S:
            self.change_y = -PLAYER_SPEED
        elif key == arcade.key.A:
            self.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.change_x = PLAYER_SPEED

    def on_key_release(self, key):
        if key in (arcade.key.W, arcade.key.S):
            self.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.change_x = 0

    def on_mouse_press(self, x, y):
        l, r, b, t = self.button_rect
        if l < x < r and b < y < t:
            self.character_ui_active = not self.character_ui_active
            return

        if not self.character_ui_active:
            return

        l, r, b, t = self.close_rect
        if l < x < r and b < y < t:
            self.character_ui_active = False

    def draw_ui(self):
        arcade.draw_lrbt_rectangle_filled(
            *self.button_rect,
            (90, 60, 140)
        )
        arcade.draw_text(
            "CHAR",
            SCREEN_WIDTH - 65,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            14,
            anchor_x="center",
            anchor_y="center"
        )

        bar_width = 200
        bar_height = 10
        right = SCREEN_WIDTH - 20
        left = right - bar_width
        top = SCREEN_HEIGHT - 20
        bottom = top - bar_height

        arcade.draw_lrbt_rectangle_filled(
            left,
            right,
            bottom,
            top,
            arcade.color.DARK_GRAY
        )

        fill = int(bar_width * (self.exp / self.exp_to_next))
        arcade.draw_lrbt_rectangle_filled(
            left,
            left + fill,
            bottom,
            top,
            arcade.color.GREEN
        )

        arcade.draw_text(
            f"LVL {self.level}",
            left,
            top + 5,
            arcade.color.WHITE,
            12
        )

        if not self.character_ui_active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        arcade.draw_lrbt_rectangle_filled(
            SCREEN_WIDTH // 2 - 220,
            SCREEN_WIDTH // 2 + 220,
            SCREEN_HEIGHT // 2 - 170,
            SCREEN_HEIGHT // 2 + 170,
            arcade.color.DARK_BLUE_GRAY
        )

        arcade.draw_text(
            "CHARACTER",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 140,
            arcade.color.WHITE,
            28,
            anchor_x="center"
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.close_rect,
            arcade.color.DARK_RED
        )
        arcade.draw_text(
            "X",
            SCREEN_WIDTH // 2 + 195,
            SCREEN_HEIGHT // 2 + 155,
            arcade.color.WHITE,
            16,
            anchor_x="center",
            anchor_y="center"
        )

        stats = [
            f"Level: {self.level}",
            f"EXP: {self.exp}/{self.exp_to_next}",
            f"HP: {self.hp}/{self.max_hp}",
            f"Attack: {self.attack}",
            f"Defense: {self.defense}",
            f"Luck: {self.luck}",
        ]

        y = SCREEN_HEIGHT // 2 + 80
        for s in stats:
            arcade.draw_text(
                s,
                SCREEN_WIDTH // 2,
                y,
                arcade.color.WHITE,
                18,
                anchor_x="center"
            )
            y -= 32
