from json import loads, dumps


def load_devteamtask_json():
    data: any
    with open("devteamtask.json") as file:
        data = loads(file.read())
        file.close()

    return data


def get_data_json(key):
    data = load_devteamtask_json()
    return data[key]


def write_devteamtask_json(key: str, value: str | dict):
    data = load_devteamtask_json()
    new_data = {}
    key_already_exists = False

    for k, v in data.items():
        if k == key:
            key_already_exists = True
            new_data[k] = value
        else:
            new_data[k] = v

    if not key_already_exists:
        new_data[key] = value

    # Serializing json
    json_object = dumps(new_data, indent=2)

    with open("devteamtask.json", "w") as outfile:
        outfile.write(json_object)
        outfile.close()


# write_devteamtask_json(
#     "credentials",
#     {
#         "username": "talismar",
#         "password": "admin123",
#     },
# )
