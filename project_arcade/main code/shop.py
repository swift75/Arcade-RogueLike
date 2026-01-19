import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class ShopUI:
    def __init__(self, player):
        self.player = player
        self.active = False

        self.button_rect = (20, 140, 20, 60)

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
            ("heal", "FULL HEAL", {}, 30),

            ("consumable", "Rage Potion", {"attack": 5}, 60),
            ("consumable", "Iron Skin", {"defense": 4}, 60),
            ("consumable", "Vital Elixir", {"max_hp": 70}, ),
            ("consumable", "Lucky Charm", {"luck": 5}, 70),
            ("consumable", "Battle Focus", {"attack": 3, "defense": 2}, 80),

            ("weapon", "Legendary Blade", {"attack": 15, "luck": 3}, 250),
            ("armor", "Dragon Armor", {"defense": 14, "max_hp": 60, "luck": 2}, 250),
        ]

        self.item_rects = []

    def draw(self):
        arcade.draw_lrbt_rectangle_filled(
            self.button_rect[0],
            self.button_rect[1],
            self.button_rect[2],
            self.button_rect[3],
            arcade.color.DARK_GREEN
        )

        arcade.draw_text(
            "SHOP",
            (self.button_rect[0] + self.button_rect[1]) // 2,
            (self.button_rect[2] + self.button_rect[3]) // 2,
            arcade.color.WHITE,
            16,
            anchor_x="center",
            anchor_y="center"
        )

        if not self.active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 200)
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.window_rect,
            arcade.color.DARK_BLUE_GRAY
        )

        arcade.draw_lrbt_rectangle_filled(
            *self.close_rect,
            arcade.color.DARK_RED
        )

        arcade.draw_text(
            "X",
            SCREEN_WIDTH // 2 + 275,
            SCREEN_HEIGHT // 2 + 195,
            arcade.color.WHITE,
            16,
            anchor_x="center",
            anchor_y="center"
        )

        arcade.draw_text(
            "SHOP",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 190,
            arcade.color.YELLOW,
            26,
            anchor_x="center"
        )

        arcade.draw_text(
            f"GOLD: {self.player.gold}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 150,
            arcade.color.WHITE,
            18,
            anchor_x="center",
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

            arcade.draw_lrbt_rectangle_filled(*rect, arcade.color.DARK_GRAY)

            arcade.draw_text(
                f"{name} — {price} GOLD",
                SCREEN_WIDTH // 2,
                y,
                arcade.color.WHITE,
                14,
                anchor_x="center",
                anchor_y="center"
            )

            y -= 42

    def on_mouse_press(self, x, y):
        l, r, b, t = self.button_rect
        if l < x < r and b < y < t:
            self.active = not self.active
            return True

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

