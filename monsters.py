class Player:
    def __init__(self, health, modifier, heal, block, effect):
        self.health = health
        self.modifier = modifier
        self.heal = heal
        self.block = block
        self.effect = effect


class Monster:
    def __init__(self, health, monster_type, ability_amount):
        self.health = health
        self.type = monster_type
        self.ability_amount = ability_amount

    def lifesteal(self, amount):
        self.health += amount


def set_player_attributes():
    print("== NEW PLAYER ==")
    input_health = int(input("Input player health: "))
    input_modifier = int(input("Input damage modifier: "))
    input_heals = int(input("Input amount of heals: "))
    input_blocks = int(input("Input amount of blocks: "))
    effects = "None"

    player = Player(input_health, input_modifier, input_heals, input_blocks, effects)
    print("==========")
    print("PLAYER STATS:")
    print()

    print("HP:", player.health)
    print("Damage modifier:", player.modifier)
    print("Heals:", player.heal)
    print("Blocks:", player.block)
    print("==========")
    print()

    return player


def init_new_monster():
    print("== MONSTER ==")
    monster_health = int(input("Input monster health: "))
    monster_type = input("Monster type (skeleton, knight, mage, orc): ")

    if monster_type == "skeleton":
        print("\nSkeletons have the \"Lifesteal\" ability: "
              "They can steal HP from the player through attacks.\n")
        monster = Monster(monster_health, "Skeleton", 0)

    elif monster_type == "knight":
        block_chance = str(input("\nKnights have the \"Armor\" ability: "
                                 "They are armored, giving them a chance to block player attacks.\n"
                                 "Set the blocking chance in percentage (e.g. 20): "))
        block_chance = float(block_chance)/100
        monster = Monster(monster_health, "Knight", block_chance)

    elif monster_type == "mage":
        poison = int(input("\nMages have the \"Poison\" ability: "
                           "They throw out a potion which damages the player every turn.\n"
                           "Set the poison damage: "))
        monster = Monster(monster_health, "Mage", poison)

    elif monster_type == "orc":
        attack_modifier = int(input("\nOrcs wield mighty greatswords: "
                                    "They add damage to their base attack.\n"
                                    "Set the added damage bonus: "))
        monster = Monster(monster_health, "Orc", attack_modifier)
    else:
        monster = Monster(monster_health, monster_type, 0)

    print("HP:", monster.health)
    print("Monster type:", monster_type)
    print("==========")
    input("Press Enter to continue...")
    return monster
