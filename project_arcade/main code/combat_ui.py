import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class CombatChoiceUI:
    def __init__(self):
        self.active = False
        self.timer = 0.0
        self.enemies = []
        self.info_active = False

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

    def start(self, enemies):
        self.active = True
        self.timer = 3.0
        self.enemies = enemies
        self.info_active = False

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
        if not self.active:
            return

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

        if not self.info_active:
            return

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

    def on_mouse_press(self, x, y):
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
