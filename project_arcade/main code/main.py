import arcade

from room import RoomManager
from combat_ui import CombatChoiceUI
from start_choice_ui import StartChoiceUI
from pause_menu import PauseMenu

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roguelike"

PLAYER_SPEED = 7


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.room_manager = RoomManager()

        self.player = arcade.SpriteSolidColor(40, 40, arcade.color.BLUE)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 100

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.combat_ui = CombatChoiceUI()
        self.start_ui = StartChoiceUI()
        self.pause_menu = PauseMenu()

        self.in_combat = False
        self.combat_timer = 0.0

    def on_draw(self):
        self.clear()
        self.room_manager.current_room.draw()
        self.player_list.draw()

        self.combat_ui.draw()
        self.start_ui.draw()
        self.pause_menu.draw()

    def on_update(self, delta_time):
        if self.pause_menu.active:
            return

        room = self.room_manager.current_room

        if self.in_combat:
            self.combat_timer -= delta_time
            if self.combat_timer <= 0:
                room.enemies.clear()
                room.cleared = True
                room.exit.active = True
                self.room_manager._save_room(room)
                self.in_combat = False
            return

        self.player.center_x += self.player.change_x
        self.player.center_y += self.player.change_y

        self.player.center_x = max(20, min(SCREEN_WIDTH - 20, self.player.center_x))
        self.player.center_y = max(20, min(SCREEN_HEIGHT - 20, self.player.center_y))

        if room.type == "start" and arcade.check_for_collision(self.player, room.exit):
            if not self.start_ui.active:
                self.start_ui.start()
            return

        if room.type != "start" and room.exit.active:
            if arcade.check_for_collision(self.player, room.exit):
                self.room_manager.next_room()
                self.player.center_x = SCREEN_WIDTH // 2
                self.player.center_y = 100
                return

        if room.enemies and not self.combat_ui.active and not self.in_combat:
            self.combat_ui.start()

        if room.type == "chest" and not room.chest_opened:
            if arcade.check_for_collision(self.player, room.chest):
                room.chest_opened = True
                room.chest_list.clear()
                room.exit.active = True
                self.room_manager._save_room(room)

        result = self.combat_ui.update(delta_time)
        if result == "fight":
            self.in_combat = True
            self.combat_timer = 2.5

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.pause_menu.toggle()
            return

        if self.pause_menu.active:
            return

        if key == arcade.key.W:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.S:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        if self.pause_menu.active:
            result = self.pause_menu.on_mouse_press(x, y)
            if result == "menu":
                self.room_manager.go_to_start()
                self.player.center_x = SCREEN_WIDTH // 2
                self.player.center_y = 100
            return

        combat_result = self.combat_ui.on_mouse_press(x, y)
        if combat_result == "fight":
            self.in_combat = True
            self.combat_timer = 2.5
        elif combat_result == "escape":
            self.room_manager.go_to_start()
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = 100

        start_result = self.start_ui.on_mouse_press(x, y)
        if start_result == "new":
            self.room_manager.start_new_run()
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = 100
        elif start_result == "continue":
            self.room_manager.continue_run()
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = 100


if __name__ == "__main__":
    Game()
    arcade.run()
