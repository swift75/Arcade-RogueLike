import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class PauseMenu:
    def __init__(self):
        self.active = False

        self.continue_rect = (
            SCREEN_WIDTH // 2 - 180,
            SCREEN_WIDTH // 2 + 180,
            SCREEN_HEIGHT // 2 + 10,
            SCREEN_HEIGHT // 2 + 70
        )

        self.menu_rect = (
            SCREEN_WIDTH // 2 - 180,
            SCREEN_WIDTH // 2 + 180,
            SCREEN_HEIGHT // 2 - 70,
            SCREEN_HEIGHT // 2 - 10
        )

        self.title_text = arcade.Text(
            "PAUSED",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 120,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        self.continue_text = arcade.Text(
            "CONTINUE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 30,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

        self.menu_text = arcade.Text(
            "BACK TO MAIN MENU",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 50,
            arcade.color.WHITE,
            18,
            anchor_x="center"
        )

    def toggle(self):
        self.active = not self.active

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
            *self.continue_rect,
            arcade.color.DARK_GREEN
        )
        self.continue_text.draw()

        arcade.draw_lrbt_rectangle_filled(
            *self.menu_rect,
            arcade.color.DARK_BLUE
        )
        self.menu_text.draw()

    def on_mouse_press(self, x, y):
        if not self.active:
            return None

        l, r, b, t = self.continue_rect
        if l < x < r and b < y < t:
            self.close()
            return "continue"

        l, r, b, t = self.menu_rect
        if l < x < r and b < y < t:
            self.close()
            return "menu"

        return None