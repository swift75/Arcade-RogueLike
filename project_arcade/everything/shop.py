import arcade
from items import get_item_name_ru
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_text_shadow(self, text, x, y, color, size, anchor_x="center"):
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

class ShopUI:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.back_sprite = arcade.Sprite(
            "char_back.png",
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2
        )
        self.back_sprite.width = 550
        self.back_sprite.height = 500
        self.window_rect = (
            SCREEN_WIDTH // 2 - 300,
            SCREEN_WIDTH // 2 + 300,
            SCREEN_HEIGHT // 2 - 220,
            SCREEN_HEIGHT // 2 + 220
        )

        self.close_rect = (
            SCREEN_WIDTH // 2 + 260,
            SCREEN_WIDTH // 2 + 290,
            SCREEN_HEIGHT // 2 + 180,
            SCREEN_HEIGHT // 2 + 210
        )

        self.items = [
            ("heal", "Полное лечение", {}, 30),

            ("consumable", "Зелье ярости", {"attack": 5}, 25),
            ("consumable", "Железная кожа", {"defense": 4}, 25),
            ("consumable", "Эликсир жизни", {"max_hp": 40}, 30),
            ("consumable", "Талисман удачи", {"luck": 5}, 30),
            ("consumable", "Боевой фокус", {"attack": 3, "defense": 2}, 35),

            ("weapon", "Legendary Blade", {"attack": 15, "luck": 3}, 120),
            ("armor", "Dragon Armor", {"defense": 14, "max_hp": 60, "luck": 2}, 120),
        ]

        self.item_rects = []

    def draw(self):
        if not self.active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )
        arcade.draw_sprite(self.back_sprite)

        arcade.draw_lrbt_rectangle_filled(*self.close_rect, arcade.color.DARK_RED)
        arcade.draw_lrbt_rectangle_outline(*self.close_rect, arcade.color.BLACK, 2)

        draw_text_shadow(
            self,
            "X",
            SCREEN_WIDTH // 2 + 275,
            SCREEN_HEIGHT // 2 + 188,
            arcade.color.WHITE,
            16
        )

        draw_text_shadow(
            self,
            "МАГАЗИН",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 190,
            arcade.color.GOLD,
            26
        )

        draw_text_shadow(
            self,
            f"ЗОЛОТО - {self.player.gold}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 150,
            arcade.color.WHITE,
            20
        )

        self.item_rects.clear()
        y = SCREEN_HEIGHT // 2 + 110

        for item in self.items:
            kind, name, stats, price = item

            rect = (
                SCREEN_WIDTH // 2 - 260,
                SCREEN_WIDTH // 2 + 260,
                y - 18,
                y + 18
            )
            self.item_rects.append((rect, item))

            arcade.draw_lrbt_rectangle_filled(
                rect[0], rect[1], rect[2], rect[3],
                arcade.color.DARK_SLATE_GRAY
            )

            arcade.draw_lrbt_rectangle_outline(
                rect[0] + 2, rect[1] - 2, rect[2] + 2, rect[3] - 2,
                arcade.color.GRAY,
                2
            )

            arcade.draw_lrbt_rectangle_outline(
                *rect,
                arcade.color.BLACK,
                2
            )

            draw_text_shadow(
                self,
                f"{get_item_name_ru(name)} — {price} ЗОЛОТА",
                SCREEN_WIDTH // 2,
                y - 6.5 ,
                arcade.color.WHITE,
                14
            )

            y -= 42

    def on_mouse_press(self, x, y):
        if not self.active:
            return False

        l, r, b, t = self.close_rect
        if l < x < r and b < y < t:
            self.active = False
            return True

        for rect, item in self.item_rects:
            l, r, b, t = rect
            if l < x < r and b < y < t:
                self.buy(item)
                return True

        return True

    def buy(self, item):
        kind, name, stats, price = item

        if self.player.gold < price:
            return

        self.player.gold -= price

        if kind == "heal":
            self.player.hp = self.player.max_hp
            self.player.save_progress()
            return

        if kind == "consumable":
            self.player.inventory["consumable"].append(
                ("consumable", name, stats, 3)
            )
            self.player.save_progress()
            return

        if kind == "weapon":
            self.player.inventory["weapon"].append(
                ("weapon", name, stats, 0)
            )
            self.player.save_progress()
            return

        if kind == "armor":
            self.player.inventory["armor"].append(
                ("armor", name, stats, 0)
            )
            self.player.save_progress()
            return
