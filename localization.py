import re


def say(what, replace_with):
    # Convert all in replace_with to str
    spare_parts = [str(x) for x in replace_with]

    # Open localization file
    localization_file = open("localization.txt", "r")
    try:  # Find title text "what" in file
        for line in localization_file:
            if f"{what} = " in line:
                dialog = line.replace(f"{what} = ", "")
                dialog = dialog.encode().decode('unicode_escape')
        number_of_placeholders = len(re.findall(r"\[\d]", dialog))

    except UnboundLocalError:  # Can't find the "what" text supposed to display
        print(f"[localization.py] ERROR: Can't find title text \"{what}\".")

    else:
        if number_of_placeholders == 0:  # No text to replace
            print(dialog, end="")
            return
        else:  # Fill in the blanks...
            i = 0
            for replacement in spare_parts:
                dialog = dialog.replace(f"[{i}]", replacement)
                i += 1

            print(dialog, end="")
            return
