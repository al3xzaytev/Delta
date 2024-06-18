class Player:
    def __init__(self, name, health, modifier, heal, block, effect):
        self.name = name
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


def init_new_player():
    print("\n== PLAYER ==")
    input_name = input("Player name: ")
    input_health = int(input("Input player health: "))
    input_modifier = int(input("Input damage modifier: "))
    input_heals = int(input("Input amount of heals: "))
    input_blocks = int(input("Input amount of blocks: "))
    effects = "None"

    player = Player(input_name, input_health, input_modifier, input_heals, input_blocks, effects)
    print("==========")
    print(f"{player.name}")
    print()

    print("HP:", player.health)
    print("Damage modifier:", player.modifier)
    print("Heals:", player.heal)
    print("Blocks:", player.block)
    print("==========")
    print()

    return player


def init_new_monster():
    print("\n== MONSTER ==")
    monster_health = int(input("Input monster health: "))
    monster_type = input("Monster type (skeleton, knight, mage, orc): ")

    if monster_type == "skeleton":
        print("\nSkeletons have the \"Lifesteal\" ability: "
              "They can steal HP from the player through attacks.\n")
        monster = Monster(monster_health, "Skeleton", 0)

    elif monster_type == "knight":
        block_chance = str(input("\nKnights have the \"Swordsman\" ability: "
                                 "Their adept sword-fighting skills give them a chance to block attacks.\n"
                                 "Set the blocking chance in percentage (e.g. 20): "))
        block_chance = float(block_chance)/100
        monster = Monster(monster_health, "Knight", block_chance)

    elif monster_type == "mage":
        poison = int(input("\nMages have the \"Poison\" ability: "
                           "They throw out a poisonous potion which damages the player every turn.\n"
                           "Set the poison damage: "))
        monster = Monster(monster_health, "Mage", poison)

    elif monster_type == "orc":
        attack_modifier = int(input("\nOrcs wield mighty greatswords, "
                                    "adding damage to their base attack.\n"
                                    "Set the added damage bonus: "))
        monster = Monster(monster_health, "Orc", attack_modifier)
    else:
        monster = Monster(monster_health, monster_type, 0)

    print("HP:", monster.health)
    print("Monster type:", monster_type)
    print("Ability amount:", monster.ability_amount)
    print("==========")
    input("Press Enter to continue...")
    return monster


def initialize(character, amount):
    if character == "player":
        for i in range(0, amount):
            player = init_new_player()
            return player

    if character == "monster":
        monster = init_new_monster()
        return monster
