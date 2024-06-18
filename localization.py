def say(what):
    localization_file = open("localization.txt", "r")
    for line in localization_file:
        if f"{what} = " in line:
            dialog = line.replace(f"{what} = ", "")
            return dialog
