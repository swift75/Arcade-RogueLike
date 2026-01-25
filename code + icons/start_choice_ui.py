import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_text_shadow(text, x, y, color, size, anchor_x="center"):
    arcade.draw_text(
        text,
        x + 2, y - 2,
        arcade.color.BLACK,
        size,
        font_name="Minecraft Rus",
        anchor_x=anchor_x
    )
    arcade.draw_text(
        text,
        x, y,
        color,
        size,
        font_name="Minecraft Rus",
        anchor_x=anchor_x
    )


class StartChoiceUI:
    def __init__(self):
        self.active = False

        self.continue_rect = (
            SCREEN_WIDTH // 2 - 160,
            SCREEN_WIDTH // 2 + 160,
            SCREEN_HEIGHT // 2 - 20,
            SCREEN_HEIGHT // 2 + 40
        )

        self.close_rect = (
            SCREEN_WIDTH // 2 - 120,
            SCREEN_WIDTH // 2 + 120,
            SCREEN_HEIGHT // 2 - 90,
            SCREEN_HEIGHT // 2 - 50
        )

    def start(self):
        self.active = True

    def close(self):
        self.active = False

    def draw(self):
        if not self.active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )



        draw_text_shadow(
            "ПОРТАЛ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 110,
            arcade.color.GOLD,
            30
        )

        draw_text_shadow(
            "НАЧАЛО ПУТИ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 80,
            arcade.color.WHITE,
            18
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.continue_rect,
            arcade.color.DARK_GREEN
        )

        arcade.draw_lrbt_rectangle_outline(
            *self.continue_rect,
            arcade.color.BLACK,
            2
        )

        draw_text_shadow(
            "ВОЙТИ В ПОДЗЕМЕЛЬЕ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 1,
            arcade.color.WHITE,
            18
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.close_rect,
            arcade.color.DARK_GRAY
        )

        arcade.draw_lrbt_rectangle_outline(
            *self.close_rect,
            arcade.color.BLACK,
            2
        )

        draw_text_shadow(
            "ОТМЕНА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 76,
            arcade.color.WHITE,
            16
        )

    def on_mouse_press(self, x, y):
        if not self.active:
            return None

        l, r, b, t = self.continue_rect
        if l < x < r and b < y < t:
            self.close()
            return "continue"

        l, r, b, t = self.close_rect
        if l < x < r and b < y < t:
            self.close()
            return None

        return None
