# Handles configuration files
def set_config():  # Modifies the configuration file
    print("GAME CONFIGURATIONS")
    print("Select the parameter you want to modify.\n")

    configs = open("config.cfg", "r")

    param_list = []
    for param in configs:
        print(param, end="")
        param_list.append(param.replace("\n", ""))

    configs = open("config.cfg", "r")
    file_content = configs.read()

    choose = input("\n\nChoose parameter to modify: ")

    found = False
    for stuff in param_list:
        if choose in stuff:
            parameter = stuff.split(sep="=")
            print(f"PARAMETER: {parameter[0]}={parameter[1]}")
            found = True
        else:
            continue

    if found:
        old_value = f"{parameter[0]}={parameter[1]}"
        mod = input(f"Choose new value for parameter {parameter[0]}: ")
        new_value = f"{parameter[0]}={mod}"
        config_file = open("config.cfg", "w")
        new_file_content = file_content.replace(old_value, new_value)
        config_file.write(new_file_content)
        config_file.close()
        print("Config saved.")
    else:
        print("Cannot find parameter.")
    return


def read_config(parameter):  # Returns a value of the configuration parameter specified
    configs = open("config.cfg", "r")
    found = False
    for param in configs:
        if parameter in param:
            param = param.replace("\n", "")
            isolated_parameter = param.split(sep="=")
            value = isolated_parameter[1]
            found = True
        else:
            continue
    if found:
        print(f"{isolated_parameter[0]}={isolated_parameter[1]}")
        return value
    else:
        print(f"ERROR: Cannot find parameter \"{parameter}\".")
        return None
