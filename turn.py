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
            lc.say("PLAYER_ATTACK_PROMPT", [])
            input()
            if monster.type == "Knight":
                if random.random() < monster.ability_amount:
                    lc.say("PLAYER_ATTACK_BLOCKED", [monster.type])
                    return "blocked"

            player_damage = random.randrange(1, 7)

            if player.modifier != 0:
                lc.say("PLAYER_ATTACK_DAMAGE_MODIFIED", [player.name, player_damage, player.modifier])
                player_damage = player_damage + player.modifier
            else:
                lc.say("PLAYER_ATTACK_DAMAGE", [player.name, player_damage])

            monster.health -= player_damage

            return "attack"

        # Healing
        elif command == "heal":
            if player.heal > 0:
                lc.say("PLAYER_HEAL_PROMPT", [])
                input()
                heal = random.randrange(1, 7)
                lc.say("PLAYER_HEAL_AMOUNT", [player.name, heal])
                player.health += heal
                player.heal -= 1
                return "heal"
            else:
                lc.say("PLAYER_HEAL_FAIL", [])
                return "fail"

        # Blocking attack
        elif command == "block":
            if player.block > 0:
                lc.say("PLAYER_BLOCK", [player.name, monster.type])
                player.block -= 1
                monster.effect = "Blocked"
                return "block"
            else:
                lc.say("PLAYER_BLOCK_FAIL", [])
                return "fail"

    def monster_attack(targets):  # Processes monster attacks
        lc.say("PLAYER_ATTACK_PROMPT", [])
        input()

        monster_damage = random.randrange(1, 7)

        if monster.type == "Orc":
            lc.say("MONSTER_ATTACK_DAMAGE_ORC", [monster.type, monster_damage, monster.ability_amount])
            monster_damage += monster.ability_amount
        else:
            lc.say("MONSTER_ATTACK_DAMAGE", [monster.type, monster_damage])

        if monster.type == "Skeleton":  # Skeleton lifesteal
            lc.say("MONSTER_ATTACK_LIFESTEAL_AMOUNT", [monster.type, monster_damage])
            monster.lifesteal(monster_damage)

        if monster.type == "Spider":  # Select a random player to root
            while True:
                root_target = random.choice(list(targets.keys()))
                root_target_status = targets[root_target][1]
                print(root_target_status)
                if root_target_status == "Alive":  # Root target has to be alive
                    root_target.effect = "Rooted"
                    break
                else:
                    continue
            lc.say("MONSTER_ROOT", [monster.type, root_target.name])

        for player in targets:  # Deal damage
            player.health -= monster_damage
            if monster.type == "Mage":  # Poison all players
                player.effect = "Poisoned"

        if monster.type == "Spider":
            return root_target.name

    def process_turn(players_turn, player, player_type, name):  # Processes the turn for players and monsters
        # Reminder: players_turn takes player_list dictionary

        # Player's turn
        if player_type == "player":
            print(f"\n{name}'s turn.")
            while True:
                lc.say("PLAYER_ACTION_PROMPT", [])
                action = input()
                turn_result = process_action(player, action)
                if turn_result == "block":
                    continue
                elif turn_result == "fail":
                    continue
                else:
                    if check_health(monster.health) == "dead":
                        lc.say("VICTORY_MESSAGE", [monster.type])
                        input("Press Enter to continue...")
                        return "win"
                    else:
                        return None

        # Monster's turn
        elif player_type == "monster":
            print(f"\n{monster.type}'s turn.")
            result = monster_attack(player_list)
            return result

    def interface(players_display, turn_no):  # Prints player and monster info
        print(f"-------------------- TURN {turn_no} --------------------")

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
                lc.say("PLAYER_POISONED", [player_object.name, monster.type, poison_damage])
            elif player_object.effect == "Rooted":
                lc.say("PLAYER_ROOTED", [player_object.name, monster.type])
            if players_display[player_object][1] == "Dead":
                lc.say("DEFEAT_MESSAGE", [monster.type])
            print()

        # Monster info
        print(monster.type)
        print(f"MONSTER HP: {monster.health}")
        print(f"MONSTER TYPE: {monster.type}")
        print(f"MONSTER ABILITY AMOUNT: {monster.ability_amount}")
        print(f"MONSTER EFFECT: {monster.effect}")
        if monster.effect == "Blocked":
            lc.say("MONSTER_BLOCKED_UI", [monster.type])
        print(f"-------------------- TURN {turn_no} --------------------")
        return None

    turn_count = 1

    rooted_dict = {}  # Keep track of who's rooted
    for players in list(player_list.keys()):
        rooted_dict.update({players.name: "No"})

    while True:
        # ======================================== BEFORE START OF TURN ========================================

        # Check if monster is dead before turn
        if check_health(monster.health) == "dead":
            lc.say("VICTORY_MESSAGE", [monster.type])
            input("Press Enter to continue...")
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

        # ======================================== INTERFACE DISPLAY ========================================

        # Display interface
        interface(player_list, turn_count)

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
            input("Defeated! Press Enter to continue by calling in new characters...")
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
                    interface(player_list, turn_count)
                    if check_health(monster.health) == "dead":
                        lc.say("VICTORY_MESSAGE", [monster.type])
                        input("Press Enter to continue...")
                        return "win"

            if monster.effect != "Blocked":
                monster_target = process_turn(player_list, monster, "monster", monster.type)
            else:
                lc.say("MONSTER_BLOCKED", [monster.type])

        # ======================================== END OF TURN ========================================

            if monster.type == "Spider":
                for players in player_list:
                    if players.effect == "Rooted":  # Rooted next turn
                        if rooted_dict[players.name] == "No":
                            rooted_dict[players.name] = "Yes"  # Set a flag that keeps player in root
                            continue

                        elif rooted_dict[players.name] == "Yes":  # Rooted for this turn
                            if monster_target != players.name:  # If he wasn't rooted again next turn...
                                players.effect = "None"  # Un-root
                                rooted_dict[players.name] = "No"  # Bring the flag down
                                continue

            # Remove blocked effect for the monster after the turn ends
            if monster.effect == "Blocked":
                monster.effect = "None"

            turn_count += 1
            continue
