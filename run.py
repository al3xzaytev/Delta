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
    for i in range(player_count):
        player = monsters.initialize("player", player_count)
        player_list.update({player: [player.name, "Alive"]})

    print(player_list)
    for i in player_list:
        print(type(i))

    level_number = 1

    while True:
        print(f"LEVEL {level_number}")

        monster = monsters.initialize("monster", 1)

        print("==============================")
        print(f"LEVEL {level_number}")
        print("FIGHT !!")

        result = turn.turn(player_list, monster)

        if result == "win":
            level_number += 1
            continue
        elif result == "defeated":
            while True:
                number_of_dead_motherfuckers = 1
                for players, status in player_list.items():
                    if status == "Dead":
                        new_player = monsters.initialize("player", 1)
                        player_list.update({new_player: ["player{0}".format(number_of_dead_motherfuckers), "Alive"]})
                        number_of_dead_motherfuckers += 1
                result = turn.turn(player_list, monster)
                if result == "win":
                    level_number += 1
                    break
                else:
                    continue


main_menu()
