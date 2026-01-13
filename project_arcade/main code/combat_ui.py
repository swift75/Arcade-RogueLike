import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class CombatChoiceUI:
    def __init__(self):
        self.active = False
        self.timer = 0.0

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

    def start(self):
        self.active = True
        self.timer = 3.0

    def update(self, delta_time):
        if not self.active:
            return None

        self.timer -= delta_time

        if self.timer <= 0:
            self.active = False
            return "fight"

        return None

    def draw(self):
        if not self.active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, (0, 0, 0, 180)
        )

        self.time_text.text = f"TIME: {int(self.timer) + 1}"

        self.time_text.draw()
        self.fight_text.draw()
        self.escape_text.draw()

    def on_mouse_press(self, x, y):
        if not self.active:
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
