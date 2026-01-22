import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_text_shadow(text, x, y, color, size, anchor_x="center", anchor_y="center"):
    arcade.draw_text(
        text,
        x + 2, y - 2,
        (0, 0, 0, 180),
        size,
        font_name="Minecraft Rus",
        anchor_x=anchor_x,
        anchor_y=anchor_y
    )
    arcade.draw_text(
        text,
        x, y,
        color,
        size,
        font_name="Minecraft Rus",
        anchor_x=anchor_x,
        anchor_y=anchor_y
    )


class DeathUI:
    def __init__(self):
        self.active = False

        self.new_game_rect = (
            SCREEN_WIDTH // 2 - 180,
            SCREEN_WIDTH // 2 + 180,
            SCREEN_HEIGHT // 2 - 20,
            SCREEN_HEIGHT // 2 + 40
        )

        self.revive_rect = (
            SCREEN_WIDTH // 2 - 180,
            SCREEN_WIDTH // 2 + 180,
            SCREEN_HEIGHT // 2 - 80,
            SCREEN_HEIGHT // 2 - 40
        )

    def draw(self, can_revive):
        if not self.active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )

        draw_text_shadow(
            "ВЫ ПОГИБЛИ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 120,
            arcade.color.RED,
            32
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.new_game_rect,
            arcade.color.DARK_RED
        )

        draw_text_shadow(
            "НОВАЯ ИГРА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 10,
            arcade.color.WHITE,
            18
        )

        color = arcade.color.DARK_GREEN if can_revive else arcade.color.DARK_GRAY

        arcade.draw_lrbt_rectangle_filled(
            *self.revive_rect,
            color
        )

        draw_text_shadow(
            "ВОЗРОДИТЬСЯ ЗА 1000 ЗОЛОТА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 60,
            arcade.color.WHITE if can_revive else arcade.color.LIGHT_GRAY,
            16
        )

    def on_mouse_press(self, x, y, can_revive):
        if not self.active:
            return None

        l, r, b, t = self.new_game_rect
        if l < x < r and b < y < t:
            return "new_game"

        if can_revive:
            l, r, b, t = self.revive_rect
            if l < x < r and b < y < t:
                return "revive"

        return None

    def close(self):
        self.active = False
