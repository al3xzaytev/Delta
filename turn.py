import random
import monsters


def initialize(character):
    if character == "player":
        player = monsters.init_new_player()
        return player

    if character == "monster":
        monster = monsters.init_new_monster()
        return monster


def turn(player, monster):
    def check_health(health):
        if health <= 0:
            return "dead"
        else:
            return "no"

    def process_action(command):
        if command == "attack":
            input("Attack: press Enter!")

            if monster.type == "Knight":
                if random.random() < monster.ability_amount:
                    print("The Knight has blocked your attack !!")
                    return "blocked"

            player_damage = random.randrange(1, 7)

            if player.modifier != 0:
                print(f"Player attacked and did {player_damage} + {player.modifier} damage!")
                player_damage = player_damage + player.modifier
            else:
                print(f"Player attacked and did {player_damage} damage!")

            monster.health -= player_damage

            return "attack"
        elif command == "heal":
            if player.heal > 0:
                input("Heal: press Enter!")
                heal = random.randrange(1, 7)
                print(f"Player healed for {heal} HP!")
                player.health += heal
                player.heal -= 1
                return "heal"
            else:
                print("Can't heal - no heals left!!")
                return "fail"
        elif command == "block":
            if player.block > 0:
                print("Player has blocked Monster's next attack!")
                player.block -= 1
                return "block"
            else:
                print("Can't block - no blocks left!!")
                return "fail"

    def monster_attack():
        input("Attack: press Enter!")
        monster_damage = random.randrange(1, 7)
        if monster.type == "Orc":
            print(f"{monster.type} attacked Player and did {monster_damage} + {monster.ability_amount} damage!")
            monster_damage += monster.ability_amount
        else:
            print(f"{monster.type} attacked Player and did {monster_damage} damage!")
        player.health -= monster_damage

        if monster.type == "Skeleton":
            print(f"The Skeleton has stolen {monster_damage} HP !!")
            monster.lifesteal(monster_damage)
        elif monster.type == "Mage":
            player.effect = "Poisoned"

    current_player = "player"
    while True:
        if player.effect == "Poisoned":
            poison_damage = monster.ability_amount
            print(f"Player is being poisoned by the Mage!! They will lose {poison_damage} HP every turn.")
            player.health -= poison_damage

        print()
        print(f"PLAYER HP: {player.health}")
        print(f"PLAYER DAMAGE MODIFIER: {player.modifier}")

        print(f"PLAYER EFFECT: {player.effect}")
        print()
        print(f"MONSTER HP: {monster.health}")
        print(f"MONSTER TYPE: {monster.type}")
        print(f"MONSTER ABILITY AMOUNT: {monster.ability_amount}")

        if check_health(player.health) == "dead":
            print("DEFEATED!\nYou have been defeated by the monster !!")
            return "defeated"

        if check_health(monster.health) == "dead":
            print(f"VICTORY!\n{monster.type} defeated !!")
            return "win"

        if current_player == "player":
            print("Player's turn.")
            while True:
                action = input("What do you want to do (attack, heal, block): ")

                result = process_action(action)
                if result == "block":
                    current_player = "player"
                    break
                elif result == "fail":
                    continue
                else:
                    current_player = "monster"
                    break

        elif current_player == "monster":
            print(f"\n{monster.type}'s turn.")

            monster_attack()

            current_player = "player"
