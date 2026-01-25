import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BACKGROUND_TEXTURE = arcade.load_texture("main_menu.png")


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


class MainMenu:
    def __init__(self):
        self.active = True

        self.bg_sprite = arcade.Sprite()
        self.bg_sprite.texture = BACKGROUND_TEXTURE
        self.bg_sprite.center_x = SCREEN_WIDTH // 2
        self.bg_sprite.center_y = SCREEN_HEIGHT // 2
        self.bg_sprite.scale = max(
            SCREEN_WIDTH / BACKGROUND_TEXTURE.width,
            SCREEN_HEIGHT / BACKGROUND_TEXTURE.height
        )

        self.continue_rect = (
            SCREEN_WIDTH // 2 - 180,
            SCREEN_WIDTH // 2 + 180,
            SCREEN_HEIGHT // 2 + 10,
            SCREEN_HEIGHT // 2 + 70
        )

        self.new_game_rect = (
            SCREEN_WIDTH // 2 - 180,
            SCREEN_WIDTH // 2 + 180,
            SCREEN_HEIGHT // 2 - 80,
            SCREEN_HEIGHT // 2 - 20
        )

    def draw(self):
        if not self.active:
            return

        arcade.draw_sprite(self.bg_sprite)

        draw_text_shadow(
            "КРУГ ИСПЫТАНИЙ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 150,
            arcade.color.GOLD,
            40
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.continue_rect,
            arcade.color.DARK_GRAY
        )
        arcade.draw_lrbt_rectangle_outline(
            *self.continue_rect,
            arcade.color.BLACK,
            2
        )

        draw_text_shadow(
            "ПРОДОЛЖИТЬ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 35,
            arcade.color.WHITE,
            20
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.new_game_rect,
            arcade.color.GRAY
        )
        arcade.draw_lrbt_rectangle_outline(
            *self.new_game_rect,
            arcade.color.BLACK,
            2
        )

        draw_text_shadow(
            "НОВАЯ ИГРА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 55,
            arcade.color.WHITE,
            20
        )

    def on_mouse_press(self, x, y):
        if not self.active:
            return None

        l, r, b, t = self.continue_rect
        if l < x < r and b < y < t:
            self.active = False
            return "continue"

        l, r, b, t = self.new_game_rect
        if l < x < r and b < y < t:
            self.active = False
            return "new_game"

        return None
