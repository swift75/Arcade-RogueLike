import arcade
import math
import sqlite3
from animations import AnimatedKnight
from items import (get_item_name_ru,get_stat_name_ru,get_stat_short_ru)
import sys
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 6
DB_FILE = "player.db"

arcade.load_font("minecraft.ttf")


class Player:
    def __init__(self, x, y):
        self.sprite = AnimatedKnight(x, y, scale=0.75)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.char_back = arcade.Sprite("char_back.png")
        self.char_back.width = 440
        self.char_back.height = 270
        self.char_back.center_x = SCREEN_WIDTH // 2
        self.char_back.center_y = SCREEN_HEIGHT // 2 + 10

        self.item_textures = {
            "Rusty Dagger": arcade.load_texture("dagger.png"),
            "Short Sword": arcade.load_texture("short sword.png"),
            "Knight Sword": arcade.load_texture("knight sword.png"),
            "War Axe": arcade.load_texture("axe.png"),
            "Legendary Blade": arcade.load_texture("legendary blade.png"),

            "Cloth Armor": arcade.load_texture("cloth armor.png"),
            "Leather Armor": arcade.load_texture("leather armor.png"),
            "Chainmail": arcade.load_texture("chainmail.png"),
            "Plate Armor": arcade.load_texture("plate armor.png"),
            "Dragon Armor": arcade.load_texture("dragon armor.png"),
        }

        self.inventory_icon = arcade.Sprite("inventory.png", scale=0.2)
        self.inventory_icon.right = SCREEN_WIDTH - 5
        self.inventory_icon.bottom = 115

        self.inv_button_rect = (
            self.inventory_icon.left,
            self.inventory_icon.right,
            self.inventory_icon.bottom,
            self.inventory_icon.top
        )

        self.shop_icon = arcade.Sprite("shop.png", scale=0.2)
        self.shop_icon.right = SCREEN_WIDTH - 5
        self.shop_icon.top = self.inventory_icon.bottom - 5

        self.shop_button_rect = (
            self.shop_icon.left,
            self.shop_icon.right,
            self.shop_icon.bottom,
            self.shop_icon.top
        )
        self.behind_sprite = arcade.Sprite("behind.png")
        self.weapon_icon = None
        self.armor_icon = None

        self.change_x = 0
        self.change_y = 0

        self.level = 1
        self.exp = 0
        self.gold = 0
        self.exp_to_next = 200

        self.max_hp = 100
        self.hp = 100
        self.attack = 12
        self.defense = 6
        self.luck = 3

        self.weapon = None
        self.armor = None

        self.inventory_active = False
        self.character_ui_active = False
        self.item_action_active = False

        self.selected_item = None
        self.selected_kind = None

        self.inventory = {
            "weapon": [],
            "armor": [],
            "consumable": []
        }


        self.char_icon = arcade.Sprite("char.png", scale=0.15)
        self.char_icon.center_x = SCREEN_WIDTH - 38
        self.char_icon.center_y = SCREEN_HEIGHT // 2 + 75

        self.inv_box_1 = arcade.Sprite("inventory_box.png", scale=0.5)
        self.inv_box_1.center_x = self.char_icon.center_x - 5
        self.inv_box_1.center_y = (
                self.char_icon.center_y
                - self.char_icon.height // 2
                - self.inv_box_1.height // 2
                - 6
        )

        self.inv_box_2 = arcade.Sprite("inventory_box.png", scale=0.5)
        self.inv_box_2.center_x = self.inv_box_1.center_x
        self.inv_box_2.center_y = self.inv_box_1.center_y - self.inv_box_1.height - 4

        self.button_rect = (
            self.char_icon.left,
            self.char_icon.right,
            self.char_icon.bottom,
            self.char_icon.top
        )

        self.close_rect = (
            SCREEN_WIDTH // 2 + 180,
            SCREEN_WIDTH // 2 + 210,
            SCREEN_HEIGHT // 2 + 115,
            SCREEN_HEIGHT // 2 + 145
        )


        self.inv_close_rect = (
            SCREEN_WIDTH // 2 + 200,
            SCREEN_WIDTH // 2 + 230,
            SCREEN_HEIGHT // 2 + 230,
            SCREEN_HEIGHT // 2 + 260
        )

        self.use_rect = (
            SCREEN_WIDTH // 2 - 120,
            SCREEN_WIDTH // 2 - 10,
            SCREEN_HEIGHT // 2 - 40,
            SCREEN_HEIGHT // 2 + 10
        )

        self.drop_rect = (
            SCREEN_WIDTH // 2 + 10,
            SCREEN_WIDTH // 2 + 120,
            SCREEN_HEIGHT // 2 - 40,
            SCREEN_HEIGHT // 2 + 10
        )

        self.action_close_rect = (
            SCREEN_WIDTH // 2 + 130,
            SCREEN_WIDTH // 2 + 160,
            SCREEN_HEIGHT // 2 + 20,
            SCREEN_HEIGHT // 2 + 50
        )

        if self.weapon:
            self.weapon_icon = self.create_ui_icon(
                self.weapon[1],
                self.inv_box_1
            )

        if self.armor:
            self.armor_icon = self.create_ui_icon(
                self.armor[1],
                self.inv_box_2
            )

        self.active_buffs = []

        self.init_db()
        self.load_progress()

    def set_position(self, x, y):
        self.sprite.center_x = x
        self.sprite.center_y = y

    def init_db(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS player (
                id INTEGER PRIMARY KEY,
                level INTEGER,
                exp INTEGER,
                exp_to_next INTEGER,
                gold INTEGER,
                max_hp INTEGER,
                hp INTEGER,
                attack INTEGER,
                defense INTEGER,
                luck INTEGER,
                weapon TEXT,
                armor TEXT,
                inventory TEXT,
                buffs TEXT
            )
        """)
        conn.commit()
        conn.close()

    def load_progress(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            SELECT level, exp, exp_to_next, gold, max_hp, hp,
                   attack, defense, luck,
                   weapon, armor, inventory, buffs
            FROM player WHERE id = 1
        """)
        row = cur.fetchone()
        if row:
            (
                self.level,
                self.exp,
                self.exp_to_next,
                self.gold,
                self.max_hp,
                self.hp,
                self.attack,
                self.defense,
                self.luck,
                weapon,
                armor,
                inventory,
                buffs
            ) = row
            self.weapon = eval(weapon) if weapon else None
            self.armor = eval(armor) if armor else None
            self.inventory = eval(inventory)
            self.active_buffs = eval(buffs) if buffs else []
        else:
            cur.execute(
                "INSERT INTO player VALUES (1,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    self.level,
                    self.exp,
                    self.exp_to_next,
                    self.gold,
                    self.max_hp,
                    self.hp,
                    self.attack,
                    self.defense,
                    self.luck,
                    None,
                    None,
                    str(self.inventory),
                    str(self.active_buffs)
                )
            )
            conn.commit()
        conn.close()

    def save_progress(self):
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("""
            UPDATE player SET
                level=?, exp=?, exp_to_next=?, gold=?,
                max_hp=?, hp=?, attack=?, defense=?, luck=?,
                weapon=?, armor=?, inventory=?, buffs=?
            WHERE id=1
        """, (
            self.level,
            self.exp,
            self.exp_to_next,
            self.gold,
            self.max_hp,
            self.hp,
            self.attack,
            self.defense,
            self.luck,
            str(self.weapon),
            str(self.armor),
            str(self.inventory),
            str(self.active_buffs)
        ))
        conn.commit()
        conn.close()

    def add_to_inventory(self, item):
        kind = item[0]
        if len(self.inventory[kind]) >= 5:
            return False
        self.inventory[kind].append(item)
        self.save_progress()
        return True

    def apply_stats(self, stats, sign):
        for k, v in stats.items():
            if k == "attack":
                self.attack += v * sign
            elif k == "defense":
                self.defense += v * sign
            elif k == "max_hp":
                self.max_hp += v * sign
                self.hp = min(self.hp, self.max_hp)
            elif k == "luck":
                self.luck += v * sign

    def create_ui_icon(self, name, box_sprite):
        texture = self.item_textures.get(name)
        if not texture:
            return None

        icon = arcade.Sprite()
        icon.texture = texture

        icon.center_x = box_sprite.center_x
        icon.center_y = box_sprite.center_y

        icon.scale = min(
            box_sprite.width / texture.width,
            box_sprite.height / texture.height
        ) * 0.85

        return icon

    def equip_item(self, item):
        kind, name, stats, _ = item

        if kind == "weapon":
            if self.weapon:
                self.apply_stats(self.weapon[2], -1)

            self.weapon = item
            self.weapon_icon = self.create_ui_icon(
                name, self.inv_box_1
            )

        else:
            if self.armor:
                self.apply_stats(self.armor[2], -1)

            self.armor = item
            self.armor_icon = self.create_ui_icon(
                name, self.inv_box_2
            )

        self.apply_stats(stats, 1)
        self.save_progress()

    def use_consumable(self, item):
        _, name, stats, rooms = item

        for buff in self.active_buffs:
            if buff["name"] == name:
                buff["rooms_left"] = rooms
                self.inventory["consumable"].remove(item)
                self.save_progress()
                return

        self.apply_stats(stats, 1)
        self.active_buffs.append({
            "name": name,
            "stats": stats,
            "rooms_left": rooms
        })

        self.inventory["consumable"].remove(item)
        self.save_progress()

    def on_enemy_room_cleared(self):
        expired = []
        for buff in self.active_buffs:
            buff["rooms_left"] -= 1
            if buff["rooms_left"] <= 0:
                expired.append(buff)

        for buff in expired:
            self.apply_stats(buff["stats"], -1)
            self.active_buffs.remove(buff)

        self.save_progress()

    def update(self):
        dx = self.change_x
        dy = self.change_y
        self.sprite.center_x += dx
        self.sprite.center_y += dy
        self.sprite.center_x = max(20, min(SCREEN_WIDTH - 20, self.sprite.center_x))
        self.sprite.center_y = max(20, min(SCREEN_HEIGHT - 20, self.sprite.center_y))
        self.sprite.is_walking = bool(dx or dy)
        self.sprite.set_direction(dx)

    def update_animation(self, delta_time):
        self.sprite.update_animation(delta_time)

    def add_exp(self, exp_amount, gold_amount=0):
        self.exp += exp_amount
        self.gold += gold_amount

        while self.exp >= self.exp_to_next:
            self.exp -= self.exp_to_next
            self.level += 1
            self.exp_to_next = math.ceil(self.exp_to_next * 1.25)

            self.max_hp += 20
            self.hp = self.max_hp
            self.attack += 4
            self.defense += 3
            self.luck += 1

        self.save_progress()

    def format_item_stats(self, stats):
        parts = []
        for k, v in stats.items():
            if k == "attack":
                parts.append(f"+АТК {v}")
            elif k == "defense":
                parts.append(f"+ЗАЩ {v}")
            elif k == "max_hp":
                parts.append(f"+ЗДР {v}")
            elif k == "luck":
                parts.append(f"+УДАЧА {v}")
        return ", ".join(parts)

    def on_key_press(self, key):
        if key == arcade.key.W:
            self.change_y = PLAYER_SPEED
        elif key == arcade.key.S:
            self.change_y = -PLAYER_SPEED
        elif key == arcade.key.A:
            self.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.change_x = PLAYER_SPEED

    def on_key_release(self, key):
        if key in (arcade.key.W, arcade.key.S):
            self.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.change_x = 0

    def on_mouse_press(self, x, y):
        l, r, b, t = self.shop_button_rect
        if l < x < r and b < y < t:
            return "open_shop"

        l, r, b, t = self.inv_button_rect
        if l < x < r and b < y < t:
            self.inventory_active = not self.inventory_active
            self.item_action_active = False
            return

        l, r, b, t = self.button_rect
        if l < x < r and b < y < t:
            self.character_ui_active = not self.character_ui_active
            self.inventory_active = False
            self.item_action_active = False
            return

        if self.character_ui_active:
            l, r, b, t = self.close_rect
            if l < x < r and b < y < t:
                self.character_ui_active = False
                return

        if self.inventory_active:
            l, r, b, t = self.inv_close_rect
            if l < x < r and b < y < t:
                self.inventory_active = False
                self.item_action_active = False
                return

        if self.item_action_active:
            l, r, b, t = self.action_close_rect
            if l < x < r and b < y < t:
                self.item_action_active = False
                return

        if not self.inventory_active:
            return

        if self.item_action_active:
            l, r, b, t = self.use_rect
            if l < x < r and b < y < t:
                if self.selected_kind in ("weapon", "armor"):
                    self.equip_item(self.selected_item)
                else:
                    self.use_consumable(self.selected_item)
                self.item_action_active = False
                self.save_progress()
                return

            l, r, b, t = self.drop_rect
            if l < x < r and b < y < t:

                if self.selected_kind == "weapon" and self.weapon == self.selected_item:
                    self.apply_stats(self.weapon[2], -1)
                    self.weapon = None
                    self.weapon_icon = None
                if self.selected_kind == "armor" and self.armor == self.selected_item:
                    self.apply_stats(self.armor[2], -1)
                    self.armor = None
                    self.armor_icon = None

                self.inventory[self.selected_kind].remove(self.selected_item)
                self.selected_item = None
                self.item_action_active = False
                self.save_progress()
                return

        draw_y = SCREEN_HEIGHT // 2 + 200
        for kind in ("weapon", "armor", "consumable"):
            draw_y -= 24
            for item in self.inventory[kind]:
                text_height = 14
                hit_top = draw_y + text_height // 2
                hit_bottom = draw_y - text_height // 2

                if (
                    SCREEN_WIDTH // 2 - 200 < x < SCREEN_WIDTH // 2 + 200
                    and hit_bottom < y < hit_top
                ):
                    self.selected_item = item
                    self.selected_kind = kind
                    self.item_action_active = True
                    return

                draw_y -= 22
            draw_y -= 10

    def draw_text_shadow(
            self,
            text,
            x,
            y,
            color,
            font_size,
            *,
            shadow_color=(0, 0, 0, 180),
            offset=2,
            anchor_x="center",
            anchor_y="center"
    ):
        arcade.draw_text(
            text,
            x + offset,
            y - offset,
            shadow_color,
            font_size,
            font_name="Minecraft Rus",
            anchor_x=anchor_x,
            anchor_y=anchor_y
        )

        arcade.draw_text(
            text,
            x,
            y,
            color,
            font_size,
            font_name="Minecraft Rus",
            anchor_x=anchor_x,
            anchor_y=anchor_y
        )

    def draw_ui(self):
        arcade.draw_sprite(self.inventory_icon)
        arcade.draw_sprite(self.shop_icon)

        min_x = min(
            self.char_icon.left,
            self.inv_box_1.left,
            self.inv_box_2.left
        ) - 6

        max_x = max(
            self.char_icon.right,
            self.inv_box_1.right,
            self.inv_box_2.right
        ) + 6

        min_y = min(
            self.char_icon.bottom,
            self.inv_box_1.bottom,
            self.inv_box_2.bottom
        ) - 6

        max_y = max(
            self.char_icon.top,
            self.inv_box_1.top,
            self.inv_box_2.top
        ) + 6

        self.behind_sprite.center_x = (min_x + max_x) // 2
        self.behind_sprite.center_y = (min_y + max_y) // 2
        self.behind_sprite.width = max_x - min_x
        self.behind_sprite.height = max_y - min_y

        arcade.draw_sprite(self.behind_sprite)

        arcade.draw_sprite(self.char_icon)
        arcade.draw_sprite(self.inv_box_1)
        arcade.draw_sprite(self.inv_box_2)

        if self.weapon_icon:
            arcade.draw_sprite(self.weapon_icon)

        if self.armor_icon:
            arcade.draw_sprite(self.armor_icon)

        if self.character_ui_active:
            arcade.draw_lrbt_rectangle_filled(
                0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
                (0, 0, 0, 180)
            )
            self.char_back.center_x = SCREEN_WIDTH // 2
            self.char_back.center_y = SCREEN_HEIGHT // 2 + 10
            self.char_back.width = 440
            self.char_back.height = 270
            arcade.draw_sprite(self.char_back)
            arcade.draw_sprite(self.char_back)

            arcade.draw_lrbt_rectangle_filled(
                *self.close_rect,
                arcade.color.DARK_RED
            )

            arcade.draw_text(
                "X",
                SCREEN_WIDTH // 2 + 195,
                SCREEN_HEIGHT // 2 + 128,
                arcade.color.WHITE,
                16,
                font_name="Minecraft Rus",
                anchor_x="center",
                anchor_y="center"
            )

            stats = [
                f"Уровень: {self.level}",
                f"Опыт: {self.exp}/{self.exp_to_next}",
                f"Здоровье: {self.hp}/{self.max_hp}",
                f"Атака: {self.attack}",
                f"Защита: {self.defense}",
                f"Удача: {self.luck}",
                f"Оружие: {get_item_name_ru(self.weapon[1]) if self.weapon else 'Нет'}",
                f"Броня: {get_item_name_ru(self.armor[1]) if self.armor else 'Нет'}",
            ]

            y = SCREEN_HEIGHT // 2 + 110
            for line in stats:
                self.draw_text_shadow(
                    line,
                    SCREEN_WIDTH // 2,
                    y,
                    arcade.color.WHITE,
                    18
                )
                y -= 28

        if not self.inventory_active:
            return

        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )

        self.char_back.center_x = SCREEN_WIDTH // 2
        self.char_back.center_y = SCREEN_HEIGHT // 2
        self.char_back.width = 475
        self.char_back.height = 490
        arcade.draw_sprite(self.char_back)

        arcade.draw_lrbt_rectangle_filled(
            *self.inv_close_rect,
            arcade.color.DARK_RED
        )

        arcade.draw_text(
            "X",
            SCREEN_WIDTH // 2 + 215,
            SCREEN_HEIGHT // 2 + 245,
            arcade.color.WHITE,
            16,
            font_name="Minecraft Rus",
            anchor_x="center",
            anchor_y="center"
        )

        draw_y = SCREEN_HEIGHT // 2 + 200

        for kind, title in (
                ("weapon", "Оружие"),
                ("armor", "Броня"),
                ("consumable", "Расходные предметы")):
            self.draw_text_shadow(
                title,
                SCREEN_WIDTH // 2,
                draw_y,
                arcade.color.YELLOW,
                18
            )

            draw_y -= 24

            for item in self.inventory[kind]:
                text = f"- {get_item_name_ru(item[1])}"

                if len(item) > 2 and item[2]:
                    stats = self.format_item_stats(item[2])
                    if stats:
                        text += f" ({stats})"

                self.draw_text_shadow(
                    text,
                    SCREEN_WIDTH // 2,
                    draw_y,
                    arcade.color.WHITE,
                    14
                )

                draw_y -= 22

            draw_y -= 10

        if self.item_action_active:
            arcade.draw_lrbt_rectangle_filled(
                *self.use_rect,
                arcade.color.DARK_GREEN
            )

            arcade.draw_lrbt_rectangle_filled(
                *self.drop_rect,
                arcade.color.DARK_RED
            )

            arcade.draw_lrbt_rectangle_filled(
                *self.action_close_rect,
                arcade.color.DARK_RED
            )

            arcade.draw_text(
                "ИСПОЛЬЗ",
                SCREEN_WIDTH // 2 - 65,
                SCREEN_HEIGHT // 2 - 15,
                arcade.color.WHITE,
                14,
                font_name="Minecraft Rus",
                anchor_x="center",
                anchor_y="center"
            )

            arcade.draw_text(
                "БРОСИТЬ",
                SCREEN_WIDTH // 2 + 65,
                SCREEN_HEIGHT // 2 - 15,
                arcade.color.WHITE,
                14,
                font_name="Minecraft Rus",
                anchor_x="center",
                anchor_y="center"
            )

            arcade.draw_text(
                "X",
                SCREEN_WIDTH // 2 + 145,
                SCREEN_HEIGHT // 2 + 35,
                arcade.color.WHITE,
                14,
                font_name="Minecraft Rus",
                anchor_x="center",
                anchor_y="center"
            )

    def reset_full(self):
        self.level = 1
        self.exp = 0
        self.exp_to_next = 200
        self.gold = 0

        self.max_hp = 100
        self.hp = 100
        self.attack = 12
        self.defense = 6
        self.luck = 3

        self.weapon = None
        self.armor = None
        self.weapon_icon = None
        self.armor_icon = None

        self.inventory = {
            "weapon": [],
            "armor": [],
            "consumable": []
        }

        self.active_buffs = []

        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute("DELETE FROM player WHERE id = 1")
        conn.commit()
        conn.close()

        self.init_db()
        self.load_progress()