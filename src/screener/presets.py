import yaml


def load_preset(name):

    with open("config/presets.yaml", "r") as file:
        presets = yaml.safe_load(file)

    return presets[name]