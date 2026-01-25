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


class PauseMenu:
    def __init__(self):
        self.active = False

        self.music = arcade.Sound("The_Bards_Tale.mp3", streaming=True)
        self.volume = 0.25
        self.last_volume = self.volume
        self.player = self.music.play(self.volume, loop=True)

        self.panel_rect = (
            SCREEN_WIDTH // 2 - 220,
            SCREEN_WIDTH // 2 + 220,
            SCREEN_HEIGHT // 2 - 190,
            SCREEN_HEIGHT // 2 + 190
        )

        self.continue_rect = (
            SCREEN_WIDTH // 2 - 160,
            SCREEN_WIDTH // 2 + 160,
            SCREEN_HEIGHT // 2 + 10,
            SCREEN_HEIGHT // 2 + 60
        )

        self.menu_rect = (
            SCREEN_WIDTH // 2 - 160,
            SCREEN_WIDTH // 2 + 160,
            SCREEN_HEIGHT // 2 - 70,
            SCREEN_HEIGHT // 2 - 20
        )

        self.slider_rect = (
            SCREEN_WIDTH // 2 - 140,
            SCREEN_WIDTH // 2 + 140,
            SCREEN_HEIGHT // 2 - 130,
            SCREEN_HEIGHT // 2 - 115
        )

        self.mute_rect = (
            SCREEN_WIDTH // 2 + 155,
            SCREEN_WIDTH // 2 + 195,
            SCREEN_HEIGHT // 2 - 138,
            SCREEN_HEIGHT // 2 - 102
        )

        self.dragging_slider = False
        self.muted = False

    def toggle(self):
        self.active = not self.active

    def close(self):
        self.active = False

    def set_volume_from_x(self, x):
        l, r, _, _ = self.slider_rect
        self.volume = max(0.0, min(1.0, (x - l) / (r - l)))

        if self.volume <= 0.0:
            self.muted = True
            if self.player:
                self.player.pause()
        else:
            self.muted = False
            if not self.player or not self.player.playing:
                self.player = self.music.play(self.volume, loop=True)
            else:
                self.player.volume = self.volume

    def toggle_mute(self):
        if not self.muted:
            self.last_volume = self.volume
            self.volume = 0.0
            self.muted = True
            if self.player:
                self.player.pause()
        else:
            self.volume = self.last_volume if self.last_volume > 0 else 0.25
            self.muted = False
            self.player = self.music.play(self.volume, loop=True)

    def draw(self):
        if not self.active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 160)
        )

        draw_text_shadow(
            "ПАУЗА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 130,
            arcade.color.GOLD,
            32
        )

        draw_text_shadow(
            "ГРОМКОСТЬ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 95,
            arcade.color.WHITE,
            16
        )

        l, r, b, t = self.slider_rect
        arcade.draw_lrbt_rectangle_filled(l, r, b, t, arcade.color.DARK_GRAY)

        knob_x = l + self.volume * (r - l)
        arcade.draw_circle_filled(knob_x, (b + t) // 2, 8, arcade.color.GOLD)

        arcade.draw_lrbt_rectangle_filled(*self.mute_rect, arcade.color.DARK_GRAY)
        icon = "🔇" if self.muted or self.volume == 0 else "🔊"
        draw_text_shadow(
            icon,
            (self.mute_rect[0] + self.mute_rect[1]) // 2,
            (self.mute_rect[2] + self.mute_rect[3]) // 2 - 10,
            arcade.color.WHITE,
            20
        )

        arcade.draw_lrbt_rectangle_filled(*self.continue_rect, arcade.color.DARK_GRAY)
        arcade.draw_lrbt_rectangle_outline(*self.continue_rect, arcade.color.BLACK, 2)

        draw_text_shadow(
            "ПРОДОЛЖИТЬ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 25,
            arcade.color.WHITE,
            18
        )

        arcade.draw_lrbt_rectangle_filled(*self.menu_rect, arcade.color.GRAY)
        arcade.draw_lrbt_rectangle_outline(*self.menu_rect, arcade.color.BLACK, 2)

        draw_text_shadow(
            "В ГЛАВНОЕ МЕНЮ",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 55,
            arcade.color.WHITE,
            18
        )

    def on_mouse_press(self, x, y):
        if not self.active:
            return None

        l, r, b, t = self.slider_rect
        if l < x < r and b < y < t:
            self.dragging_slider = True
            self.set_volume_from_x(x)
            return None

        l, r, b, t = self.mute_rect
        if l < x < r and b < y < t:
            self.toggle_mute()
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

    def on_mouse_release(self):
        self.dragging_slider = False

    def on_mouse_motion(self, x, y):
        if self.dragging_slider:
            self.set_volume_from_x(x)
