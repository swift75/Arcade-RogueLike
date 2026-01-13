import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class StartChoiceUI:
    def __init__(self):
        self.active = False
        self.choice = None

        self.begin_rect = (
            SCREEN_WIDTH // 2 - 220,
            SCREEN_WIDTH // 2 - 20,
            SCREEN_HEIGHT // 2 - 30,
            SCREEN_HEIGHT // 2 + 30
        )

        self.continue_rect = (
            SCREEN_WIDTH // 2 + 20,
            SCREEN_WIDTH // 2 + 220,
            SCREEN_HEIGHT // 2 - 30,
            SCREEN_HEIGHT // 2 + 30
        )

        self.close_rect = (
            SCREEN_WIDTH // 2 - 120,
            SCREEN_WIDTH // 2 + 120,
            SCREEN_HEIGHT // 2 - 100,
            SCREEN_HEIGHT // 2 - 60
        )

        self.title_text = arcade.Text(
            "START GAME",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 120,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        self.begin_text = arcade.Text(
            "TEMP",
            SCREEN_WIDTH // 2 - 120,
            SCREEN_HEIGHT // 2 - 10,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        self.continue_text = arcade.Text(
            "CONTINUE",
            SCREEN_WIDTH // 2 + 120,
            SCREEN_HEIGHT // 2 - 10,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        self.close_text = arcade.Text(
            "CLOSE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 90,
            arcade.color.WHITE,
            16,
            anchor_x="center"
        )

    def start(self):
        self.active = True
        self.choice = None

    def close(self):
        self.active = False

    def draw(self):
        if not self.active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        self.title_text.draw()

        arcade.draw_lrbt_rectangle_filled(
            *self.begin_rect,
            arcade.color.DARK_BLUE
        )
        self.begin_text.draw()

        arcade.draw_lrbt_rectangle_filled(
            *self.continue_rect,
            arcade.color.DARK_GREEN
        )
        self.continue_text.draw()

        arcade.draw_lrbt_rectangle_filled(
            *self.close_rect,
            arcade.color.DARK_GRAY
        )
        self.close_text.draw()

    def on_mouse_press(self, x, y):
        if not self.active:
            return None
#BEGIN
        # l, r, b, t = self.begin_rect
        # if l < x < r and b < y < t:
        #     self.close()
        #     return "new"

        l, r, b, t = self.continue_rect
        if l < x < r and b < y < t:
            self.close()
            return "continue"

        l, r, b, t = self.close_rect
        if l < x < r and b < y < t:
            self.close()
            return None

        return None
