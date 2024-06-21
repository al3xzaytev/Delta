import copy

import turn
import config
import monsters


def main_menu():
    print("D E L T A\nThe turn-based terminal dungeon crawler from hell.")
    print("Select what to do:")
    print("1. Play")
    print("2. Configure game")
    while True:
        user_input = input("alexei@delta:~$ ")
        if user_input == "1":
            start_level(config.read_config("PLAYER_COUNT"))
        elif user_input == "2":
            config.set_config()


def start_level(player_count):
    player_count = int(player_count)
    player_list = {}

    level_number = 1
    new_level = True
    player_storage = []

    while True:
        # Logically, this should only be run once at the beginning of every level...
        if len(player_list) < player_count:
            for i in range(player_count):
                player = monsters.initialize("player")
                player_storage.append(copy.deepcopy(player))
                player_list.update({player: [player.name, "Alive"]})

        # Remove players from player_storage if all players are dead
        if not new_level:
            player_storage.clear()

        # Initializes new players in place of dead ones
        for players, info in player_list.copy().items():
            if info[1] == "Dead":
                new_player = monsters.initialize("player")
                player_storage.append(copy.deepcopy(new_player))
                player_list[new_player] = player_list.pop(players)
                player_list[new_player] = [new_player.name, "Alive"]

        # Convoluted player stat reset after finishing a level
        z = 0
        while z < player_count:
            for player_object in player_list.keys():
                if player_object.name == player_storage[z].name:
                    if not monsters.compare_with_base(player_storage[z], player_object):
                        replacement = copy.deepcopy(player_storage[z])
                        player_list[replacement] = player_list.pop(player_object)
                        z += 1
                        break
                    else:
                        z += 1
                        continue
                else:
                    continue

        if new_level:
            print("--------------------------------------------------------------------------------")
            print(f"LEVEL {level_number}")
            monster = monsters.initialize("monster")

            print("--------------------------------------------------------------------------------")
            print(f"LEVEL {level_number}")
            print("FIGHT !!")
            print("--------------------------------------------------------------------------------")

        while True:
            result = turn.turn(player_list, monster)  # Go play the game.
            if result == "win":
                for player in player_list:
                    player.effect = "None"  # Resets all effects
                level_number += 1
                new_level = True
                break
            elif result == "defeated":
                new_level = False
                break


main_menu()
