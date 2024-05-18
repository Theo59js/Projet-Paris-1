import config

def get_config(config_path='config.toml'):
    return (config.load(config_path))