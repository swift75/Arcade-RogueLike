import arcade
import random

from room import RoomManager
from combat_ui import CombatChoiceUI
from start_choice_ui import StartChoiceUI
from pause_menu import PauseMenu
from player import Player
from shop import ShopUI
from death_ui import DeathUI
from items import get_item_name_ru, get_stat_name_ru
from main_menu import MainMenu


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Circle of Challenges"

PLAYER_SPAWN_X = SCREEN_WIDTH // 2
PLAYER_SPAWN_Y = SCREEN_HEIGHT // 2


# сила игрока
def calc_player_power(player):
    return (
            player.attack * 2.2 + player.defense * 4.5 + player.max_hp * 0.6 + player.level * 25 + player.luck * 3
    )


# сила врагов
def calc_enemies_power(enemies):
    total = 0
    for e in enemies:
        total += (e.attack * 2.4 + e.defense * 5 + e.max_hp * 0.8)
    return total


# время битвы
def calc_combat_time(player, enemies):
    player_power = calc_player_power(player)
    enemies_power = calc_enemies_power(enemies)
    difficulty = enemies_power / max(1, player_power)
    time_sec = 1.2 + difficulty * 1.5
    return max(0.8, min(4.0, time_sec))


# шанс на победу
def calc_win_chance(player, enemies):
    if player.level <= 3:
        return 0.999
    if not enemies:
        return 0.981
    player_power = calc_player_power(player)
    enemies_power = calc_enemies_power(enemies)
    ratio = player_power / enemies_power
    level_bonus = 1 + player.level * 0.18
    adjusted = ratio * level_bonus
    base = adjusted / (adjusted + 0.8)
    chance = 0.981 * (base ** 0.75)
    min_chance = min(0.75, 0.35 + player.level * 0.05)
    return max(min_chance, min(0.981, chance))


# потеря здоровья
def calc_victory_hp_loss(player, enemies):
    player_power = calc_player_power(player)
    enemies_power = calc_enemies_power(enemies)
    ratio = enemies_power / player_power
    ratio = max(0.1, min(1.3, ratio))
    loss = player.max_hp * (0.04 + ratio * 0.12)
    loss = min(loss, player.max_hp * 0.25)
    return int(loss)


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.death_ui = DeathUI()
        self.room_manager = RoomManager()
        self.player = Player(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player.sprite)
        self.combat_ui = CombatChoiceUI()
        self.start_ui = StartChoiceUI()
        self.pause_menu = PauseMenu()
        self.main_menu = MainMenu()
        self.main_menu.active = True
        self.game_active = False
        self.shop = ShopUI(self.player)
        self.in_combat = False
        self.combat_timer = 0.0
        self.combat_timer_max = 0.0
        self.resolve_box = (
            SCREEN_WIDTH // 2 - 220,
            SCREEN_WIDTH // 2 + 220,
            SCREEN_HEIGHT // 2 - 140,
            SCREEN_HEIGHT // 2 + 140
        )
        self.chest_ui_active = False
        self.chest_item = None
        self.chest_take_rect = (
            SCREEN_WIDTH // 2 - 165,
            SCREEN_WIDTH // 2 - 4,
            SCREEN_HEIGHT // 2 - 115,
            SCREEN_HEIGHT // 2 - 75
        )

        self.chest_leave_rect = (
            SCREEN_WIDTH // 2 - 5,
            SCREEN_WIDTH // 2 + 165,
            SCREEN_HEIGHT // 2 - 115,
            SCREEN_HEIGHT // 2 - 75
        )

    # вывод активных эффектов (справа сверху)
    def draw_buffs(self):
        if not self.player.active_buffs:
            return

        x = SCREEN_WIDTH - 20
        y = SCREEN_HEIGHT - 20

        for buff in self.player.active_buffs:
            if 'item_name' in buff:
                buff_name = get_item_name_ru(buff['item_name'])
                text_color = arcade.color.YELLOW
            else:
                buff_name = get_item_name_ru(buff['name'])
                text_color = arcade.color.YELLOW
            arcade.draw_text(
                f"{buff_name} ({buff['rooms_left']})",
                x, y, text_color,
                14,
                anchor_x="right",
                anchor_y="top",
                font_name="Minecraft Rus"
            )
            y -= 22

    def on_draw(self):
        self.clear()
        if self.main_menu.active:
            self.main_menu.draw()
            return
        self.room_manager.current_room.draw()
        self.player_list.draw()
        self.player.draw_ui()
        self.draw_buffs()
        self.shop.draw()
        if self.in_combat:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 140)
            )

            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2 - 10

            box_w = 520
            box_h = 220

            left = cx - box_w // 2
            right = cx + box_w // 2
            bottom = cy - box_h // 2
            top = cy + box_h // 2

            arcade.draw_lrbt_rectangle_filled(
                left, right, bottom, top,
                (35, 35, 35, 220)
            )

            arcade.draw_lrbt_rectangle_outline(
                left, right, bottom, top,
                (160, 160, 160),
                2
            )

            arcade.draw_text(
                "РАСЧЕТ БОЯ",
                cx, top - 42,
                arcade.color.GOLD,
                24,
                anchor_x="center",
                font_name="Minecraft Rus"
            )

            arcade.draw_text(
                f"{self.combat_timer:.1f} сек",
                cx, cy + 6,
                arcade.color.WHITE,
                36,
                anchor_x="center",
                font_name="Minecraft Rus"
            )

            bar_width = 360
            bar_height = 14

            progress = max(0.0, min(1.0, self.combat_timer / self.combat_timer_max))

            bar_left = cx - bar_width // 2
            bar_right = cx + bar_width // 2
            bar_bottom = cy - 54
            bar_top = bar_bottom + bar_height

            arcade.draw_lrbt_rectangle_filled(
                bar_left, bar_right, bar_bottom, bar_top,
                (60, 60, 60)
            )

            arcade.draw_lrbt_rectangle_filled(
                bar_left,
                bar_left + bar_width * progress,
                bar_bottom,
                bar_top,
                arcade.color.GOLD
            )

            arcade.draw_lrbt_rectangle_outline(
                bar_left, bar_right, bar_bottom, bar_top,
                (120, 120, 120),
                1
            )

        if self.chest_ui_active and self.chest_item:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 180)
            )

            cx = SCREEN_WIDTH // 2
            cy = SCREEN_HEIGHT // 2

            box_w = 500
            box_h = 280

            left = cx - box_w // 2
            right = cx + box_w // 2
            bottom = cy - box_h // 2
            top = cy + box_h // 2

            arcade.draw_lrbt_rectangle_filled(
                left, right, bottom, top,
                (35, 35, 35, 220)
            )
            arcade.draw_lrbt_rectangle_outline(
                left, right, bottom, top,
                (160, 160, 160),
                2
            )

            kind, name, stats, duration = self.chest_item

            arcade.draw_text(
                get_item_name_ru(name),
                cx + 2,
                top - 42,
                (0, 0, 0),
                22,
                anchor_x="center",
                font_name="Minecraft Rus"
            )

            arcade.draw_text(
                get_item_name_ru(name),
                cx,
                top - 40,
                arcade.color.YELLOW,
                22,
                anchor_x="center",
                font_name="Minecraft Rus"
            )

            y = top - 90
            for k, v in stats.items():
                arcade.draw_text(
                    f"{get_stat_name_ru(k)}: +{v}",
                    cx,
                    y,
                    arcade.color.WHITE,
                    18,
                    anchor_x="center",
                    font_name="Minecraft Rus"
                )
                y -= 26

            if kind == "consumable":
                arcade.draw_text(
                    f"ДЕЙСТВУЕТ: {duration} КОМН.",
                    cx,
                    y - 4,
                    arcade.color.LIGHT_GRAY,
                    16,
                    anchor_x="center",
                    font_name="Minecraft Rus"
                )

            take_l, take_r, take_b, take_t = self.chest_take_rect
            leave_l, leave_r, leave_b, leave_t = self.chest_leave_rect

            arcade.draw_lrbt_rectangle_filled(
                take_l, take_r, take_b, take_t,
                arcade.color.DARK_GREEN
            )
            arcade.draw_lrbt_rectangle_outline(
                take_l, take_r, take_b, take_t,
                arcade.color.BLACK,
                2
            )

            arcade.draw_lrbt_rectangle_filled(
                leave_l, leave_r, leave_b, leave_t,
                arcade.color.DARK_RED
            )
            arcade.draw_lrbt_rectangle_outline(
                leave_l, leave_r, leave_b, leave_t,
                arcade.color.BLACK,
                2
            )

            arcade.draw_text(
                "ЗАБРАТЬ",
                (take_l + take_r) // 2,
                (take_b + take_t) // 2,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft Rus"
            )

            arcade.draw_text(
                "УЙТИ",
                (leave_l + leave_r) // 2,
                (leave_b + leave_t) // 2,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft Rus"
            )

            arcade.draw_lrbt_rectangle_filled(
                *self.chest_take_rect,
                arcade.color.DARK_GREEN
            )
            arcade.draw_lrbt_rectangle_outline(
                *self.chest_take_rect,
                arcade.color.BLACK,
                2
            )

            arcade.draw_lrbt_rectangle_filled(
                *self.chest_leave_rect,
                arcade.color.DARK_RED
            )
            arcade.draw_lrbt_rectangle_outline(
                *self.chest_leave_rect,
                arcade.color.BLACK,
                2
            )

            arcade.draw_text(
                "ЗАБРАТЬ",
                cx - 80,
                bottom + 44,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft Rus"
            )

            arcade.draw_text(
                "ОСТАВИТЬ",
                cx + 80,
                bottom + 44,
                arcade.color.WHITE,
                18,
                anchor_x="center",
                anchor_y="center",
                font_name="Minecraft Rus"
            )

        self.combat_ui.draw()
        self.start_ui.draw()
        self.pause_menu.draw()
        self.death_ui.draw(self.player.gold >= 1000)

    def on_update(self, delta_time):
        if self.main_menu.active:
            return
        if self.player.hp <= 0 and not self.death_ui.active:
            self.death_ui.active = True
            self.in_combat = False
            self.combat_ui.active = False
            return
        if self.death_ui.active:
            return
        room = self.room_manager.current_room

        room.enemies.update_animation(delta_time)

        combat_result = self.combat_ui.update(delta_time)
        if combat_result == "fight":
            self.in_combat = True
            self.combat_timer_max = calc_combat_time(self.player, room.enemies)
            self.combat_timer = self.combat_timer_max

        if self.pause_menu.active or self.combat_ui.result_active:
            return

        if self.in_combat:
            self.combat_timer -= delta_time
            if self.combat_timer <= 0:
                victory_loss = calc_victory_hp_loss(self.player, room.enemies)
                exp_reward = 50
                gold_reward = random.randint(10, 20)

                if self.player.hp < victory_loss:
                    luck_chance = self.player.luck / 100.0
                    if random.random() < luck_chance:
                        room.enemies.clear()
                        room.cleared = True
                        room.exit_forward.active = True
                        self.room_manager._save_room(room)
                        self.player.add_exp(exp_amount=exp_reward, gold_amount=gold_reward)
                        self.combat_ui.start_result(True, 0, exp_reward, gold_reward)
                        self.in_combat = False
                        self.player.on_enemy_room_cleared()
                        return

                    lost = self.player.hp - int(self.player.hp * 0.25)
                    self.player.hp = int(self.player.hp * 0.25)
                    self.room_manager.previous_room()
                    self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
                    self.combat_ui.start_result(False, lost, 0, 0)
                    self.in_combat = False
                    return

                self.player.hp -= victory_loss
                room.enemies.clear()
                room.cleared = True
                room.exit_forward.active = True
                self.room_manager._save_room(room)
                self.player.add_exp(exp_amount=exp_reward, gold_amount=gold_reward)
                self.combat_ui.start_result(True, victory_loss, exp_reward, gold_reward)
                self.in_combat = False
                self.player.on_enemy_room_cleared()
            return

        can_move = (
                not self.combat_ui.active
                and not self.player.character_ui_active
                and not self.chest_ui_active
        )

        if can_move:
            old_x = self.player.sprite.center_x
            old_y = self.player.sprite.center_y

            self.player.update()

            if arcade.check_for_collision_with_list(
                    self.player.sprite,
                    self.room_manager.current_room.walls
            ):
                self.player.sprite.center_x = old_x
                self.player.sprite.center_y = old_y
        else:
            self.player.change_x = 0
            self.player.change_y = 0
            self.player.sprite.is_walking = False

        self.player.update_animation(delta_time)

        if room.type == "start":
            if arcade.check_for_collision(self.player.sprite, room.exit_forward):
                if not self.start_ui.active:
                    self.start_ui.start()
                return

        if room.exit_forward.active:
            if arcade.check_for_collision(self.player.sprite, room.exit_forward):
                self.room_manager.next_room()
                self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
                return

        if hasattr(room, "exit_back"):
            if arcade.check_for_collision(self.player.sprite, room.exit_back):
                self.room_manager.previous_room()
                self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
                return

        if room.enemies and not self.combat_ui.active:
            chance = calc_win_chance(self.player, room.enemies)
            self.combat_ui.start(room.enemies, chance)
            return

        if room.type == "chest" and not room.chest_opened:
            if room.chest_list and arcade.check_for_collision(self.player.sprite, room.chest_list[0]):
                chest = room.chest_list[0]
                room.chest_opened = True
                room.chest_list.clear()
                room.exit_forward.active = True
                self.room_manager._save_room(room)
                self.chest_item = chest.item
                self.chest_ui_active = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.pause_menu.toggle()
            return
        if self.pause_menu.active or self.combat_ui.active or self.in_combat or self.combat_ui.result_active:
            return

        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        if self.pause_menu.active or self.combat_ui.active or self.in_combat:
            return
        self.player.on_key_release(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.main_menu.active:
            result = self.main_menu.on_mouse_press(x, y)

            if result == "continue":
                self.main_menu.active = False
                self.game_active = True
                return

            if result == "new_game":
                self.room_manager.go_to_start()
                self.room_manager.rooms.clear()
                self.player.reset_full()
                self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)

                self.main_menu.active = False
                self.game_active = True
                return

            return

        if self.death_ui.active:
            result = self.death_ui.on_mouse_press(
                x, y,
                self.player.gold >= 1000
            )

            if result == "new_game":
                self.death_ui.close()
                self.room_manager.go_to_start()
                self.room_manager.rooms.clear()
                self.player.reset_full()
                self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
                return

            if result == "revive":
                self.player.gold -= 1000
                self.player.hp = self.player.max_hp
                self.player.save_progress()
                self.death_ui.close()
                return

            return

        if self.shop.on_mouse_press(x, y):
            return
        if self.chest_ui_active:
            l, r, b, t = self.chest_take_rect
            if l < x < r and b < y < t:
                if self.player.add_to_inventory(self.chest_item):
                    self.player.add_exp(20, 0)
                self.chest_ui_active = False
                return
            l, r, b, t = self.chest_leave_rect
            if l < x < r and b < y < t:
                self.chest_ui_active = False
                return
        if self.combat_ui.active or self.combat_ui.result_active:
            result = self.combat_ui.on_mouse_press(x, y)
        else:
            result = None

        if result == "fight":
            self.in_combat = True
            self.combat_timer_max = calc_combat_time(
                self.player,
                self.room_manager.current_room.enemies
            )
            self.combat_timer = self.combat_timer_max
            return

        if result == "escape":
            self.room_manager.previous_room()
            self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
            return

        if result == "result_close":
            return

        player_result = self.player.on_mouse_press(x, y)

        if player_result == "open_shop":
            self.shop.active = True
            return

        if self.player.character_ui_active:
            return
        if self.pause_menu.active:
            result = self.pause_menu.on_mouse_press(x, y)

            if result == "menu":
                self.pause_menu.close()
                self.game_active = False
                self.main_menu.active = True

            return

        start_result = self.start_ui.on_mouse_press(x, y)
        if start_result == "new":
            self.room_manager.start_new_run()
            self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
        elif start_result == "continue":
            self.room_manager.continue_run()
            self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)


if __name__ == "__main__":
    Game()

    arcade.run()
