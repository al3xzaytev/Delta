import random
import localization as lc


def turn(player_list, monster):
    def check_health(health):  # Checks if the object's health is zero or below i.e. dead
        if health <= 0:
            return "dead"
        else:
            return "no"

    def process_action(player, command):  # Processes player actions

        # Attacking
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

        # Healing
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

        # Blocking attack
        elif command == "block":
            if player.block > 0:
                print(f"Player has blocked {monster.type}'s next attack!")
                player.block -= 1
                monster.effect = "Blocked"
                return "block"
            else:
                print("Can't block - no blocks left!!")
                return "fail"

    def monster_attack(targets):  # Processes monster attacks
        input("Attack: press Enter!")

        monster_damage = random.randrange(1, 7)

        if monster.type == "Orc":
            print(f"{monster.type} attacked the players and did {monster_damage} + {monster.ability_amount} damage!")
            monster_damage += monster.ability_amount
        else:
            print(f"{monster.type} attacked the players and did {monster_damage} damage!")

        if monster.type == "Skeleton":  # Skeleton lifesteal
            print(f"The Skeleton has stolen {monster_damage} HP !!")
            monster.lifesteal(monster_damage)

        if monster.type == "Spider":  # Select a random player to root
            root_target = random.choice(list(targets.keys()))
            root_target.effect = "Rooted"
            print(f"The Spider has rooted {root_target.name} !!")

        for player in targets:  # Deal damage
            player.health -= monster_damage
            if monster.type == "Mage":  # Poison all players
                player.effect = "Poisoned"

    def process_turn(players_turn, player, player_type, name):  # Processes the turn for players and monsters
        # Reminder: players_turn takes player_list dictionary

        # Player's turn
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

        # Monster's turn
        elif player_type == "monster":
            print(f"\n{monster.type}'s turn.")
            monster_attack(player_list)
            return "done"

    def interface(players_display, monster_display, turn_no):  # Prints player and monster info
        print(f"==================== TURN {turn_no} ====================")

        # Player info
        for player_object in players_display:
            print(player_object.name)
            print(f"PLAYER HP: {player_object.health}")
            print(f"PLAYER DAMAGE MODIFIER: {player_object.modifier}")
            print(f"PLAYER HEALS: {player_object.heal}")
            print(f"PLAYER BLOCKS: {player_object.block}")
            print(f"PLAYER EFFECT: {player_object.effect}")
            print(f"PLAYER STATUS: {players_display[player_object][1]}")
            if player_object.effect == "Poisoned":
                poison_damage = monster.ability_amount
                print(f"Player is being poisoned by the Mage!! They will lose {poison_damage} HP every turn.")
            elif player_object.effect == "Rooted":
                print(f"Player is being rooted by the Spider!! They cannot do anything this turn.")
            if players_display[player_object][1] == "Dead":
                print(lc.say("DEFEAT_MESSAGE").format(monster_display.type))
            print()

        # Monster info
        print(monster_display.type)
        print(f"MONSTER HP: {monster_display.health}")
        print(f"MONSTER TYPE: {monster_display.type}")
        print(f"MONSTER ABILITY AMOUNT: {monster_display.ability_amount}")
        print(f"MONSTER EFFECT: {monster_display.effect}")
        if monster_display.effect == "Blocked":
            print(f"Blocked!! The {monster_display.type} cannot attack this turn.")
        print(f"==================== TURN {turn_no} ====================")
        return None

    turn_count = 1
    rooted = False  # Magic switch that checks if a player has been rooted for one turn

    while True:
        # ======================================== BEFORE START OF TURN ========================================

        # Check if monster is dead before turn
        if check_health(monster.health) == "dead":
            print(lc.say("VICTORY_MESSAGE").format(monster.type))
            return "win"

        # Poison each player every new turn
        for players in player_list:
            if players.effect == "Poisoned":
                players.health -= monster.ability_amount
                continue

        # Check for rooted player
        for players in player_list:
            if players.effect == "Rooted":
                rooted = True
                continue

        # Check if players are alive before turn
        for players in player_list:
            if check_health(players.health) == "dead":
                player_list[players][1] = "Dead"
                continue
            else:
                continue

        # ======================================== INTERFACE DISPLAY ========================================

        # Display interface
        interface(player_list, monster, turn_count)

        # ======================================== LOSER CHECK ========================================

        # Check if all players are dead
        dead_count = 0
        for players in player_list:
            player_info = player_list[players]
            player_status = player_info[1]

            if player_status == "Dead":
                dead_count += 1
                continue

        # If all players are dead... You lost, Bobby! You lost! You're a loser, Bobby!
        if dead_count == len(player_list):
            return "defeated"

        # ======================================== START OF TURN ========================================

        # Play normally if at least 1 player is alive
        else:
            for players in player_list:
                player_info = player_list[players]
                player_name = player_info[0]
                player_status = player_info[1]

                if player_status == "Alive" and players.effect != "Rooted":
                    process_turn(player_list, players, "player", player_name)
                    interface(player_list, monster, turn_count)
                    if check_health(monster.health) == "dead":
                        print(lc.say("VICTORY_MESSAGE").format(monster.type))
                        return "win"

            if check_health(monster.health) == "dead":
                print(lc.say("VICTORY_MESSAGE").format(monster.type))
                return "win"
            elif monster.effect != "Blocked":
                process_turn(player_list, monster, "monster", monster.type)
            else:
                print(f"The {monster.type} is blocked and cannot attack this turn!")

        # ======================================== END OF TURN ========================================

            # Un-root the rooted player after the turn ends
            for players in player_list:
                if players.effect == "Rooted" and rooted:
                    players.effect = "None"
                    rooted = False
                    continue

            # Remove blocked effect for the monster after the turn ends
            if monster.effect == "Blocked":
                monster.effect = "None"

            turn_count += 1
            continue
