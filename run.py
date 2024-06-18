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

    while True:
        # Logically, this should only be run once at the beginning of every level...
        if len(player_list) < player_count:
            for i in range(player_count):
                player = monsters.initialize("player", player_count)
                player_list.update({player: [player.name, "Alive"]})

        # Initializes new players in place of dead ones
        number_of_carrion = 0
        for players, info in player_list.copy().items():
            if info[1] == "Dead":
                number_of_carrion += 1
                del player_list[players]
        if number_of_carrion > 0:
            new_player = monsters.initialize("player", number_of_carrion)
            player_list.update({new_player: [new_player.name, "Alive"]})

        print("--------------------------------------------------------------------------------")
        print(f"LEVEL {level_number}")
        monster = monsters.initialize("monster", 1)

        print("--------------------------------------------------------------------------------")
        print(f"LEVEL {level_number}")
        print("FIGHT !!")
        print("--------------------------------------------------------------------------------")

        while True:
            result = turn.turn(player_list, monster)  # Go play the game.

            if result == "win":
                level_number += 1
                for player in player_list:
                    player.effect = "None"  # Resets all effects
                break
            elif result == "defeated":
                continue


main_menu()
