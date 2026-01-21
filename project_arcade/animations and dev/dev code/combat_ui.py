import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class CombatChoiceUI:
    def __init__(self):
        self.active = False
        self.timer = 0.0
        self.enemies = []
        self.info_active = False
        self.win_chance = 0.0

        self.result_active = False
        self.victory = True
        self.hp_loss = 0
        self.exp_gain = 0
        self.gold_gain = 0

        self.fight_rect = (
            SCREEN_WIDTH // 2 - 160,
            SCREEN_WIDTH // 2 - 40,
            SCREEN_HEIGHT // 2 - 30,
            SCREEN_HEIGHT // 2 + 30
        )

        self.escape_rect = (
            SCREEN_WIDTH // 2 + 40,
            SCREEN_WIDTH // 2 + 160,
            SCREEN_HEIGHT // 2 - 30,
            SCREEN_HEIGHT // 2 + 30
        )

        self.info_button_rect = (
            20,
            140,
            SCREEN_HEIGHT // 2 - 30,
            SCREEN_HEIGHT // 2 + 30
        )

        self.info_window_rect = (
            SCREEN_WIDTH // 2 - 260,
            SCREEN_WIDTH // 2 + 260,
            SCREEN_HEIGHT // 2 - 180,
            SCREEN_HEIGHT // 2 + 180
        )

        self.ok_rect = (
            SCREEN_WIDTH // 2 - 120,
            SCREEN_WIDTH // 2 + 120,
            SCREEN_HEIGHT // 2 - 120,
            SCREEN_HEIGHT // 2 - 60
        )

        self.time_text = arcade.Text(
            "",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 60,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        self.fight_text = arcade.Text(
            "FIGHT",
            SCREEN_WIDTH // 2 - 100,
            SCREEN_HEIGHT // 2,
            arcade.color.RED,
            20,
            anchor_x="center"
        )

        self.escape_text = arcade.Text(
            "ESCAPE",
            SCREEN_WIDTH // 2 + 100,
            SCREEN_HEIGHT // 2,
            arcade.color.GREEN,
            20,
            anchor_x="center"
        )

        self.chance_text = arcade.Text(
            "",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 100,
            arcade.color.YELLOW,
            16,
            anchor_x="center"
        )

        self.result_title = arcade.Text(
            "",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 140,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

    def start(self, enemies, win_chance=0.0):
        self.active = True
        self.timer = 3.0
        self.enemies = enemies
        self.info_active = False
        self.win_chance = win_chance

    def start_result(self, victory, hp_loss, exp_gain, gold_gain):
        self.result_active = True
        self.victory = victory
        self.hp_loss = hp_loss
        self.exp_gain = exp_gain
        self.gold_gain = gold_gain
        self.result_title.text = "VICTORY" if victory else "DEFEAT"

    def update(self, delta_time):
        if not self.active:
            return None

        if not self.info_active:
            self.timer -= delta_time

        if self.timer <= 0:
            self.active = False
            return "fight"

        return None

    def draw(self):
        if self.active:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 180)
            )

            arcade.draw_lrbt_rectangle_filled(
                *self.info_button_rect,
                (40, 60, 120, 160)
            )

            arcade.draw_text(
                "ENEMIES",
                80,
                SCREEN_HEIGHT // 2,
                arcade.color.WHITE,
                14,
                anchor_x="center",
                anchor_y="center"
            )

            self.time_text.text = f"TIME: {int(self.timer) + 1}"
            self.time_text.draw()
            self.fight_text.draw()
            self.escape_text.draw()

            percent = round(self.win_chance * 100, 1)
            self.chance_text.text = f"WIN CHANCE: {percent}%"
            self.chance_text.draw()

            if self.info_active:
                arcade.draw_lrbt_rectangle_filled(
                    *self.info_window_rect,
                    arcade.color.DARK_GRAY
                )

                y = SCREEN_HEIGHT // 2 + 130
                for e in self.enemies:
                    arcade.draw_text(
                        f"{e.enemy_type.upper()}  ATK:{e.attack}  DEF:{e.defense}  HP:{e.max_hp}",
                        SCREEN_WIDTH // 2,
                        y,
                        arcade.color.WHITE,
                        16,
                        anchor_x="center"
                    )
                    y -= 32

        if self.result_active:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 200)
            )

            arcade.draw_lrbt_rectangle_filled(
                SCREEN_WIDTH // 2 - 260,
                SCREEN_WIDTH // 2 + 260,
                SCREEN_HEIGHT // 2 - 180,
                SCREEN_HEIGHT // 2 + 180,
                arcade.color.DARK_GRAY
            )

            self.result_title.draw()

            arcade.draw_text(
                f"HP LOST: {self.hp_loss}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 60,
                arcade.color.RED,
                20,
                anchor_x="center"
            )

            arcade.draw_text(
                f"EXP GAINED: {self.exp_gain}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 20,
                arcade.color.GREEN,
                20,
                anchor_x="center"
            )

            if self.victory:
                arcade.draw_text(
                    f"GOLD GAINED: {self.gold_gain}",
                    SCREEN_WIDTH // 2,
                    SCREEN_HEIGHT // 2 - 20,
                    arcade.color.GOLD,
                    20,
                    anchor_x="center"
                )

            arcade.draw_lrbt_rectangle_filled(
                *self.ok_rect,
                arcade.color.DARK_GREEN
            )

            arcade.draw_text(
                "OK",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 90,
                arcade.color.WHITE,
                20,
                anchor_x="center",
                anchor_y="center"
            )

    def on_mouse_press(self, x, y):
        if self.result_active:
            l, r, b, t = self.ok_rect
            if l < x < r and b < y < t:
                self.result_active = False
                return "result_close"
            return None

        if not self.active:
            return None

        l, r, b, t = self.info_button_rect
        if l < x < r and b < y < t:
            self.info_active = not self.info_active
            return None

        if self.info_active:
            return None

        l, r, b, t = self.fight_rect
        if l < x < r and b < y < t:
            self.active = False
            return "fight"

        l, r, b, t = self.escape_rect
        if l < x < r and b < y < t:
            self.active = False
            return "escape"

        return None
