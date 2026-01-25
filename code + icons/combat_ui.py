import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UI_OFFSET_Y = -60


def draw_text_shadow(text, x, y, color, size, anchor_x="center", anchor_y="baseline"):
    arcade.draw_text(
        text,
        x + 2,
        y - 2,
        (0, 0, 0, 180),
        size,
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        font_name="Minecraft Rus"
    )
    arcade.draw_text(
        text,
        x,
        y,
        color,
        size,
        anchor_x=anchor_x,
        anchor_y=anchor_y,
        font_name="Minecraft Rus"
    )


class CombatChoiceUI:
    def __init__(self):
        self.active = False
        self.timer = 0.0
        self.enemies = []
        self.info_active = False
        self.win_chance = 0.0

        self.result_active = False
        self.victory = True
        self.hp_loss = 0
        self.exp_gain = 0
        self.gold_gain = 0

        self.fight_rect = (
            SCREEN_WIDTH // 2 - 190,
            SCREEN_WIDTH // 2 - 30,
            SCREEN_HEIGHT // 2 - 36 + UI_OFFSET_Y,
            SCREEN_HEIGHT // 2 + 36 + UI_OFFSET_Y
        )

        self.escape_rect = (
            SCREEN_WIDTH // 2 + 30,
            SCREEN_WIDTH // 2 + 190,
            SCREEN_HEIGHT // 2 - 36 + UI_OFFSET_Y,
            SCREEN_HEIGHT // 2 + 36 + UI_OFFSET_Y
        )

        self.info_button_rect = (
            20,
            160,
            SCREEN_HEIGHT // 2 - 28 + UI_OFFSET_Y,
            SCREEN_HEIGHT // 2 + 28 + UI_OFFSET_Y
        )

        self.ok_rect = (
            SCREEN_WIDTH // 2 - 130,
            SCREEN_WIDTH // 2 + 130,
            SCREEN_HEIGHT // 2 - 140 + UI_OFFSET_Y,
            SCREEN_HEIGHT // 2 - 80 + UI_OFFSET_Y
        )

        self.enemies_back = arcade.Sprite(
            "back_enemies.png",
            center_x=SCREEN_WIDTH // 2,
            center_y=SCREEN_HEIGHT // 2
        )
        self.enemies_back.width = 560
        self.enemies_back.height = 400

    def start(self, enemies, win_chance=0.0):
        self.active = True
        self.timer = 3.0
        self.enemies = enemies
        self.info_active = False
        self.win_chance = win_chance

    def start_result(self, victory, hp_loss, exp_gain, gold_gain):
        self.result_active = True
        self.victory = victory
        self.hp_loss = hp_loss
        self.exp_gain = exp_gain
        self.gold_gain = gold_gain

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
        if self.active:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 170)
            )

            draw_text_shadow(
                "ВРАГИ ПРЕГРАЖДАЮТ ПУТЬ",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 125 + UI_OFFSET_Y,
                arcade.color.GOLD,
                22
            )

            draw_text_shadow(
                f"РЕШЕНИЕ ЧЕРЕЗ {int(self.timer) + 1}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 85 + UI_OFFSET_Y,
                arcade.color.LIGHT_GRAY,
                14
            )

            percent = round(self.win_chance * 100, 1)
            draw_text_shadow(
                f"ШАНС ПОБЕДЫ: {percent}%",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 60 + UI_OFFSET_Y,
                arcade.color.GOLD,
                13
            )

            arcade.draw_lrbt_rectangle_filled(*self.fight_rect, (90, 40, 40))
            arcade.draw_lrbt_rectangle_filled(*self.escape_rect, (40, 80, 40))

            draw_text_shadow(
                "ДРАТЬСЯ",
                SCREEN_WIDTH // 2 - 110,
                SCREEN_HEIGHT // 2 + UI_OFFSET_Y - 2,
                arcade.color.WHITE,
                17,
                anchor_y="center"
            )

            draw_text_shadow(
                "БЕЖАТЬ",
                SCREEN_WIDTH // 2 + 110,
                SCREEN_HEIGHT // 2 + UI_OFFSET_Y - 2,
                arcade.color.WHITE,
                17,
                anchor_y="center"
            )

            arcade.draw_lrbt_rectangle_filled(*self.info_button_rect, (45, 45, 90))

            draw_text_shadow(
                "ВРАГИ",
                90,
                SCREEN_HEIGHT // 2 + UI_OFFSET_Y,
                arcade.color.WHITE,
                13,
                anchor_y="center"
            )

            if self.info_active:
                arcade.draw_sprite(self.enemies_back)

                y = SCREEN_HEIGHT // 2 + 120
                for e in self.enemies:
                    draw_text_shadow(
                        e.enemy_type.upper(),
                        SCREEN_WIDTH // 2,
                        y,
                        arcade.color.YELLOW,
                        16
                    )

                    draw_text_shadow(
                        f"АТК {e.attack}   ЗЩТ {e.defense}   ЗДОРОВЬЕ {e.max_hp}",
                        SCREEN_WIDTH // 2,
                        y - 22,
                        arcade.color.WHITE,
                        14
                    )

                    y -= 55

        if self.result_active:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 180)
            )

            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2

            box_w = 520
            box_h = 300

            left = cx - box_w // 2
            right = cx + box_w // 2
            bottom = cy - box_h // 2
            top = cy + box_h // 2

            arcade.draw_lrbt_rectangle_filled(
                left, right, bottom, top,
                (30, 30, 30)
            )

            arcade.draw_lrbt_rectangle_outline(
                left, right, bottom, top,
                (160, 160, 160),
                2
            )

            title = "ПОБЕДА" if self.victory else "ПОРАЖЕНИЕ"
            title_color = arcade.color.GOLD if self.victory else arcade.color.RED

            draw_text_shadow(
                title,
                cx,
                top - 48,
                title_color,
                28
            )

            y = cy + 40

            draw_text_shadow(
                f"ПОТЕРЯНО HP: {self.hp_loss}",
                cx,
                y,
                arcade.color.LIGHT_RED_OCHRE,
                16
            )

            draw_text_shadow(
                f"ПОЛУЧЕНО ОПЫТА: {self.exp_gain}",
                cx,
                y - 32,
                arcade.color.LIGHT_GREEN,
                16
            )

            if self.victory:
                draw_text_shadow(
                    f"ПОЛУЧЕНО ЗОЛОТА: {self.gold_gain}",
                    cx,
                    y - 64,
                    arcade.color.GOLD,
                    16
                )

            self.ok_rect = (
                cx - 130,
                cx + 130,
                bottom + 28,
                bottom + 78
            )

            arcade.draw_lrbt_rectangle_filled(
                *self.ok_rect,
                (60, 90, 60)
            )

            draw_text_shadow(
                "ПРОДОЛЖИТЬ",
                cx,
                bottom + 53,
                arcade.color.WHITE,
                15,
                anchor_y="center"
            )

    def on_mouse_press(self, x, y):
        if self.result_active:
            l, r, b, t = self.ok_rect
            if l < x < r and b < y < t:
                self.result_active = False
                return "result_close"
            return None

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
