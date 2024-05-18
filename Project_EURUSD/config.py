import toml

def get_config(config_path='config.toml'):
    return toml.load(config_path)