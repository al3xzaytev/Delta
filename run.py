import turn
import monsters

player = turn.initialize("player")

level_number = 1

while True:
    print(f"LEVEL {level_number}")

    monster = turn.initialize("monster")

    print("==============================")
    print(f"LEVEL {level_number}")
    print("FIGHT !!")

    result = turn.turn(player, monster)
    if result == "win":
        level_number += 1
        continue
    else:
        while True:
            player = turn.initialize("player")
            result = turn.turn(player, monster)
            if result == "win":
                level_number += 1
                break
            else:
                continue
