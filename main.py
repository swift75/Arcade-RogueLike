import arcade
from room import RoomManager

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roguelike"

PLAYER_SPEED = 7


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.paused = False
        self.room_manager = RoomManager()

        self.player_list = arcade.SpriteList()
        self.player = arcade.Sprite("assets/test_player.png", scale=3.5)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 100
        self.player.change_x = 0
        self.player.change_y = 0
        self.player_list.append(self.player)

        self.pause_title = arcade.Text(
            "PAUSE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 120,
            arcade.color.WHITE,
            36,
            anchor_x="center"
        )

        self.pause_continue_text = arcade.Text(
            "CONTINUE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 15,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

        self.pause_to_start_text = arcade.Text(
            "TO START",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - 75,
            arcade.color.WHITE,
            22,
            anchor_x="center"
        )

    def on_draw(self):
        self.clear()
        self.room_manager.current_room.draw()
        self.player_list.draw()

        if self.paused:
            self.draw_pause_menu()

    def draw_pause_menu(self):
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        arcade.draw_lbwh_rectangle_filled(
            SCREEN_WIDTH / 2 - 130, SCREEN_HEIGHT / 2 + 30 - 30,
            260, 60,
            arcade.color.DARK_GREEN
        )

        arcade.draw_lbwh_rectangle_filled(
            SCREEN_WIDTH / 2 - 130, SCREEN_HEIGHT / 2 - 60 - 30,
            260, 60,
            arcade.color.DARK_RED
        )

        self.pause_title.draw()
        self.pause_continue_text.draw()
        self.pause_to_start_text.draw()

    def on_update(self, delta_time):
        if self.paused:
            return

        self.player.center_x += self.player.change_x
        self.player.center_y += self.player.change_y

        half_w = self.player.width / 2
        half_h = self.player.height / 2

        self.player.center_x = max(
            half_w, min(SCREEN_WIDTH - half_w, self.player.center_x)
        )
        self.player.center_y = max(
            half_h, min(SCREEN_HEIGHT - half_h, self.player.center_y)
        )

        exit_portal = self.room_manager.current_room.exit
        if exit_portal.active and arcade.check_for_collision(self.player, exit_portal):
            self.room_manager.next_room()
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = 100

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            return

        if key == arcade.key.F:
            room = self.room_manager.current_room
            if room.type == "enemy":
                room.exit.active = True

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
        if not self.paused:
            return

        if (
            SCREEN_WIDTH // 2 - 130 < x < SCREEN_WIDTH // 2 + 130 and
            SCREEN_HEIGHT // 2 < y < SCREEN_HEIGHT // 2 + 60
        ):
            self.paused = False

        if (
            SCREEN_WIDTH // 2 - 130 < x < SCREEN_WIDTH // 2 + 130 and
            SCREEN_HEIGHT // 2 - 90 < y < SCREEN_HEIGHT // 2 - 30
        ):
            self.room_manager.reset()
            self.player.center_x = SCREEN_WIDTH // 2
            self.player.center_y = 100
            self.paused = False


if __name__ == "__main__":
    Game()
    arcade.run()
