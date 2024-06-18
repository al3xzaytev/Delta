import random
import localization as lc


def turn(player_list, monster):
    def check_health(health):
        if health <= 0:
            return "dead"
        else:
            return "no"

    def process_action(player, command):
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
                print(f"Player has blocked {monster.type}'s next attack!")
                player.block -= 1
                return "block"
            else:
                print("Can't block - no blocks left!!")
                return "fail"

    def monster_attack(targets):
        input("Attack: press Enter!")

        monster_damage = random.randrange(1, 7)

        if monster.type == "Orc":
            print(f"{monster.type} attacked the players and did {monster_damage} + {monster.ability_amount} damage!")
            monster_damage += monster.ability_amount
        else:
            print(f"{monster.type} attacked the players and did {monster_damage} damage!")

        if monster.type == "Skeleton":
            print(f"The Skeleton has stolen {monster_damage} HP !!")
            monster.lifesteal(monster_damage)

        for player in targets:
            player.health -= monster_damage
            if monster.type == "Mage":
                player.effect = "Poisoned"

    def process_turn(players_turn, player, player_type, name):  # Reminder: players_turn takes player_list dictionary
        if player_type == "player":
            print(f"\n{name}'s turn.")
            while True:
                action = input("What do you want to do? (attack, heal, block): ")
                turn_result = process_action(player, action)
                if turn_result == "block":
                    continue
                elif turn_result == "fail":
                    continue
                else:
                    if check_health(monster.health) == "dead":
                        print(lc.say("VICTORY_MESSAGE").format(monster.type))
                        return "win"
                    else:
                        return None

        elif player_type == "monster":
            print(f"\n{monster.type}'s turn.")
            monster_attack(player_list)
            return "done"

    def interface(players_display, monster_display, turn_no):
        print(f"==================== TURN {turn_no} ====================")
        for player_object in players_display:
            print()
            print(player_object.name)
            print(f"PLAYER HP: {player_object.health}")
            print(f"PLAYER DAMAGE MODIFIER: {player_object.modifier}")
            print(f"PLAYER EFFECT: {player_object.effect}")
            print(f"PLAYER STATUS: {players_display[player_object][1]}")
            if player_object.effect == "Poisoned":
                poison_damage = monster.ability_amount
                print(f"Player is being poisoned by the Mage!! They will lose {poison_damage} HP every turn.")
            if players_display[player_object][1] == "Dead":
                print(lc.say("DEFEAT_MESSAGE").format(monster_display.type))

        print()
        print(monster_display.type)
        print(f"MONSTER HP: {monster_display.health}")
        print(f"MONSTER TYPE: {monster_display.type}")
        print(f"MONSTER ABILITY AMOUNT: {monster_display.ability_amount}")
        return None

    turn_count = 1

    while True:
        # Check if monster is dead before turn
        if check_health(monster.health) == "dead":
            print(lc.say("VICTORY_MESSAGE").format(monster.type))
            return "win"

        # Poison each player every new turn
        for players in player_list:
            if players.effect == "Poisoned":
                players.health -= monster.ability_amount
                continue

        # Check if players are alive before turn
        for players in player_list:
            if check_health(players.health) == "dead":
                player_list[players][1] = "Dead"
                continue
            else:
                continue

        # Display interface
        interface(player_list, monster, turn_count)

        # Check if all players are dead
        dead_count = 0
        for players in player_list:
            player_info = player_list[players]
            player_status = player_info[1]

            if player_status == "Dead":
                dead_count += 1
                continue

        if dead_count == len(player_list):
            return "defeated"

        # Play normally if at least 1 player is alive
        else:
            for players in player_list:
                player_info = player_list[players]
                player_name = player_info[0]
                player_status = player_info[1]

                if player_status == "Alive":
                    result = process_turn(player_list, players, "player", player_name)
                    if result == "win":
                        return "win"
                    else:
                        interface(player_list, monster, turn_count)
            process_turn(player_list, monster, "monster", monster.type)
            turn_count += 1
            continue
