import random

WEAPONS = [
    {"name": "Rusty Dagger", "stats": {"attack": 2, "luck": 1}, "chance": 0.30},
    {"name": "Short Sword", "stats": {"attack": 4}, "chance": 0.25},
    {"name": "Knight Sword", "stats": {"attack": 6, "defense": 1}, "chance": 0.20},
    {"name": "War Axe", "stats": {"attack": 9}, "chance": 0.15},
    {"name": "Legendary Blade", "stats": {"attack": 13, "luck": 2}, "chance": 0.10},
]

ARMORS = [
    {"name": "Cloth Armor", "stats": {"defense": 1, "max_hp": 5}, "chance": 0.30},
    {"name": "Leather Armor", "stats": {"defense": 3, "max_hp": 10}, "chance": 0.25},
    {"name": "Chainmail", "stats": {"defense": 5, "max_hp": 20}, "chance": 0.20},
    {"name": "Plate Armor", "stats": {"defense": 8, "max_hp": 30}, "chance": 0.15},
    {"name": "Dragon Armor", "stats": {"defense": 12, "max_hp": 50, "luck": 1}, "chance": 0.10},
]

CONSUMABLES = [
    ("consumable", "Rage Potion", {"attack": 5}, 3),
    ("consumable", "Iron Skin", {"defense": 4}, 3),
    ("consumable", "Vital Elixir", {"max_hp": 40}, 2),
    ("consumable", "Lucky Charm", {"luck": 5}, 4),
    ("consumable", "Battle Focus", {"attack": 3, "defense": 2}, 3),
]

ITEM_NAME_RU = {
    "Rusty Dagger": "Ржавый кинжал",
    "Short Sword": "Короткий меч",
    "Knight Sword": "Рыцарский меч",
    "War Axe": "Боевой топор",
    "Legendary Blade": "Легендарный клинок",

    "Cloth Armor": "Тканевая броня",
    "Leather Armor": "Кожаная броня",
    "Chainmail": "Кольчуга",
    "Plate Armor": "Латная броня",
    "Dragon Armor": "Драконья броня",

    "Rage Potion": "Зелье ярости",
    "Iron Skin": "Железная кожа",
    "Vital Elixir": "Эликсир жизни",
    "Lucky Charm": "Талисман удачи",
    "Battle Focus": "Боевой фокус",
}

STAT_NAME_RU = {
    "attack": "Атака",
    "defense": "Защита",
    "max_hp": "Здоровье",
    "luck": "Удача",
}

STAT_SHORT_RU = {
    "attack": "ATK",
    "defense": "DEF",
    "max_hp": "HP",
    "luck": "LCK",
}


def weighted_choice(items):
    r = random.random()
    s = 0
    for item in items:
        s += item["chance"]
        if r <= s:
            return item
    return items[-1]

def roll_item():
    roll = random.random()

    if roll < 0.25:
        item = weighted_choice(WEAPONS)
        return ("weapon", item["name"], item["stats"], 0)

    if roll < 0.50:
        item = weighted_choice(ARMORS)
        return ("armor", item["name"], item["stats"], 0)

    return random.choice(CONSUMABLES)

def get_item_name_ru(name: str):
    return ITEM_NAME_RU.get(name, name)


def get_stat_name_ru(stat: str):
    return STAT_NAME_RU.get(stat, stat)


def get_stat_short_ru(stat: str):
    return STAT_SHORT_RU.get(stat, stat.upper())
