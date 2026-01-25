import arcade
import enum


class FaceDirection(enum.Enum):
    LEFT = 0
    RIGHT = 1



class AnimatedKnight(arcade.Sprite):
    def __init__(self, x, y, scale=1):
        super().__init__()

        self.scale = scale
        self.speed = 0
        self.face_direction = FaceDirection.RIGHT

        self.idle_textures = [
            arcade.load_texture(f"Knight_idle_0{i}.png")
            for i in range(1, 7)
        ]

        self.walk_textures = [
            arcade.load_texture(f"Knight_walk_0{i}.png")
            for i in range(1, 7)
        ]

        self.texture = self.idle_textures[0]

        self.current_texture = 0
        self.texture_timer = 0.0
        self.texture_delay = 0.08
        self.is_walking = False

        self.center_x = x
        self.center_y = y

    def update_animation(self, delta_time: float = 1 / 60):
        textures = self.walk_textures if self.is_walking else self.idle_textures

        self.texture_timer += delta_time
        if self.texture_timer < self.texture_delay:
            return

        self.texture_timer = 0
        self.current_texture = (self.current_texture + 1) % len(textures)
        texture = textures[self.current_texture]

        if self.face_direction == FaceDirection.LEFT:
            texture = texture.flip_horizontally()

        self.texture = texture

    def set_direction(self, dx):
        if dx < 0:
            self.face_direction = FaceDirection.LEFT
        elif dx > 0:
            self.face_direction = FaceDirection.RIGHT


class AnimatedEnemy(arcade.Sprite):
    def __init__(self, x, y, texture_path, frames, scale=2.0, speed=0.25):
        super().__init__()

        self.scale = scale

        self.textures_idle = []
        texture = arcade.load_texture(texture_path)
        frame_width = texture.width // frames
        frame_height = texture.height

        for i in range(frames):
            self.textures_idle.append(
                texture.crop(
                    x=i * frame_width,
                    y=0,
                    width=frame_width,
                    height=frame_height
                )
            )

        self.texture = self.textures_idle[0]

        self.current_texture = 0
        self.timer = 0.0
        self.speed = speed

        self.center_x = x
        self.center_y = y

    def update_animation(self, delta_time):
        self.timer += delta_time
        if self.timer >= self.speed:
            self.timer = 0
            self.current_texture = (self.current_texture + 1) % len(self.textures_idle)
            self.texture = self.textures_idle[self.current_texture]


class Fly(AnimatedEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "IdleFly.png", 8, speed=0.2)


class Goblin(AnimatedEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "IdleGoblin.png", 4, speed=0.25)


class Skeleton(AnimatedEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "IdleSkeleton.png", 4, speed=0.25)


class Mushroom(AnimatedEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, "IdleMushroom.png", 4, speed=0.2)


