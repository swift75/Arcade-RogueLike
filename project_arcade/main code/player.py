import arcade

PLAYER_SPEED = 4

#ВРЕМЕННО
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0

    def draw(self):
        arcade.draw.rect_filled(
            arcade.rect.XYWH(self.x - 15, self.y - 15, 30, 30),
            arcade.color.BLUE
        )

    def update(self):
        self.x += self.dx
        self.y += self.dy
