

def read_config():
    with open("config_bot.txt", "r") as f:
        config_dict = {}

        for line in f:
            (key, val) = line.split()[0:2] # может измениться

            if val in ["True", "False"]:
                config_dict[key] = bool(val)

            elif val.isdigit():
                config_dict[key] = int(val)

            else:
                config_dict[key] = val
        
    return config_dict

  
def update_config(key, val):
    config_dict = read_config()

    if key in config_dict.keys():
        config_dict[key] = val
    else:
        print("there is no that key")

    with open("config_bot.txt", "w") as f:
        for key in config_dict.keys():
            f.write(f"{key} {config_dict[key]} \n")

    return


if __name__ == "__main__":
    print(read_config())
    print(update_config('prefix', "!"))