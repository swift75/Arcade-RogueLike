import arcade
import random

from room import RoomManager
from combat_ui import CombatChoiceUI
from start_choice_ui import StartChoiceUI
from pause_menu import PauseMenu
from player import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roguelike"

PLAYER_SPAWN_X = SCREEN_WIDTH // 2
PLAYER_SPAWN_Y = SCREEN_HEIGHT // 2


def calc_player_power(player):
    return (
        player.attack * 2.2
        + player.defense * 4.5
        + player.max_hp * 0.6
        + player.level * 25
        + player.luck * 3
    )


def calc_enemies_power(enemies):
    total = 0
    for e in enemies:
        total += (
            e.attack * 2.4
            + e.defense * 5
            + e.max_hp * 0.8
        )
    return total


def calc_combat_time(player, enemies):
    player_power = calc_player_power(player)
    enemies_power = calc_enemies_power(enemies)
    difficulty = enemies_power / max(1, player_power)
    time_sec = 1.2 + difficulty * 1.5
    return max(0.8, min(4.0, time_sec))


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

        self.room_manager = RoomManager()

        self.player = Player(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player.sprite)

        self.combat_ui = CombatChoiceUI()
        self.start_ui = StartChoiceUI()
        self.pause_menu = PauseMenu()

        self.in_combat = False
        self.combat_timer = 0.0
        self.combat_timer_max = 0.0

        self.resolve_box = (
            SCREEN_WIDTH // 2 - 220,
            SCREEN_WIDTH // 2 + 220,
            SCREEN_HEIGHT // 2 - 140,
            SCREEN_HEIGHT // 2 + 140
        )

    def on_draw(self):
        self.clear()

        self.room_manager.current_room.draw()
        self.player_list.draw()
        self.player.draw_ui()

        if self.in_combat:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 160)
            )

            arcade.draw_lrbt_rectangle_filled(
                *self.resolve_box,
                arcade.color.DARK_SLATE_GRAY
            )

            arcade.draw_lrbt_rectangle_outline(
                *self.resolve_box,
                arcade.color.WHITE,
                2
            )

            arcade.draw_text(
                "RESOLVING COMBAT",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 90,
                arcade.color.WHITE,
                26,
                anchor_x="center"
            )

            arcade.draw_text(
                f"{self.combat_timer:.1f}s",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 20,
                arcade.color.YELLOW,
                36,
                anchor_x="center"
            )

            bar_width = 300
            bar_height = 16
            progress = self.combat_timer / self.combat_timer_max

            left = SCREEN_WIDTH // 2 - bar_width // 2
            right = SCREEN_WIDTH // 2 + bar_width // 2
            bottom = SCREEN_HEIGHT // 2 - 40
            top = bottom + bar_height

            arcade.draw_lrbt_rectangle_filled(
                left, right, bottom, top,
                arcade.color.DARK_GRAY
            )

            arcade.draw_lrbt_rectangle_filled(
                left,
                left + bar_width * progress,
                bottom,
                top,
                arcade.color.ORANGE
            )

        self.combat_ui.draw()
        self.start_ui.draw()
        self.pause_menu.draw()

    def on_update(self, delta_time):
        room = self.room_manager.current_room

        if self.pause_menu.active or self.player.character_ui_active or self.combat_ui.result_active:
            return

        combat_result = self.combat_ui.update(delta_time)
        if combat_result == "fight":
            self.in_combat = True
            self.combat_timer_max = calc_combat_time(self.player, room.enemies)
            self.combat_timer = self.combat_timer_max

        if self.combat_ui.active:
            return

        if self.in_combat:
            self.combat_timer -= delta_time
            if self.combat_timer <= 0:
                victory_loss = calc_victory_hp_loss(self.player, room.enemies)

                if self.player.hp < victory_loss:
                    luck_chance = self.player.luck / 100.0

                    if random.random() < luck_chance:
                        room.enemies.clear()
                        room.cleared = True
                        room.exit_forward.active = True
                        self.room_manager._save_room(room)
                        self.player.add_exp(50)
                        self.combat_ui.start_result(True, 0, 50)
                        self.in_combat = False
                        return

                    lost = self.player.hp - int(self.player.hp * 0.25)
                    self.player.hp = int(self.player.hp * 0.25)
                    self.room_manager.previous_room()
                    self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
                    self.combat_ui.start_result(False, lost, 0)
                    self.in_combat = False
                    return

                self.player.hp -= victory_loss
                room.enemies.clear()
                room.cleared = True
                room.exit_forward.active = True
                self.room_manager._save_room(room)
                self.player.add_exp(50)
                self.combat_ui.start_result(True, victory_loss, 50)
                self.in_combat = False
            return

        self.player.update()

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

        if room.enemies and not self.combat_ui.active and not self.in_combat:
            chance = calc_win_chance(self.player, room.enemies)
            self.combat_ui.start(room.enemies, chance)
            return

        if room.type == "chest" and not room.chest_opened:
            if room.chest_list and arcade.check_for_collision(self.player.sprite, room.chest_list[0]):
                room.chest_opened = True
                room.chest_list.clear()
                room.exit_forward.active = True
                self.player.add_exp(20)
                self.room_manager._save_room(room)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.pause_menu.toggle()
            return

        if self.pause_menu.active or self.combat_ui.active or self.in_combat or self.combat_ui.result_active:
            return

        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key)

    def on_mouse_press(self, x, y, button, modifiers):
        result = self.combat_ui.on_mouse_press(x, y)

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

        self.player.on_mouse_press(x, y)

        if self.player.character_ui_active:
            return

        if self.pause_menu.active:
            if self.pause_menu.on_mouse_press(x, y) == "menu":
                self.room_manager.go_to_start()
                self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
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
