import arcade

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

    def on_draw(self):
        self.clear()
        self.room_manager.current_room.draw()
        self.player_list.draw()
        self.player.draw_ui()
        self.combat_ui.draw()
        self.start_ui.draw()
        self.pause_menu.draw()

    def on_update(self, delta_time):
        room = self.room_manager.current_room

        if self.pause_menu.active or self.player.character_ui_active:
            return

        combat_result = self.combat_ui.update(delta_time)
        if combat_result == "fight":
            self.in_combat = True
            self.combat_timer = 2.5

        if self.combat_ui.active:
            return

        if self.in_combat:
            self.combat_timer -= delta_time
            if self.combat_timer <= 0:
                room.enemies.clear()
                room.cleared = True
                room.exit_forward.active = True
                self.room_manager._save_room(room)
                self.player.add_exp(50)
                self.in_combat = False
            return

        self.player.update()

        if room.type == "start" and arcade.check_for_collision(self.player.sprite, room.exit_forward):
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
            self.combat_ui.start(room.enemies)

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

        if self.pause_menu.active or self.combat_ui.active or self.in_combat:
            return

        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key)

    def on_mouse_press(self, x, y, button, modifiers):
        self.player.on_mouse_press(x, y)

        if self.player.character_ui_active:
            return

        if self.pause_menu.active:
            if self.pause_menu.on_mouse_press(x, y) == "menu":
                self.room_manager.go_to_start()
                self.player.set_position(PLAYER_SPAWN_X, PLAYER_SPAWN_Y)
            return

        if self.combat_ui.active:
            result = self.combat_ui.on_mouse_press(x, y)
            if result == "fight":
                self.in_combat = True
                self.combat_timer = 2.5
            elif result == "escape":
                self.room_manager.previous_room()
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
    
