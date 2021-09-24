import configparser


def get_config_obj(cfg_path="./config.ini"):
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path)
    return cfg


def read_config(session, option):
    cfg = get_config_obj()
    value = cfg.get(session, option)
    return value


# if __name__ == "__main__":
#     cfg = get_config_obj("../config.ini")
#     secs=cfg.sections()
#     options = cfg.options(secs[0])
#     items = cfg.items(secs[0], options[0])
#     item = cfg.get(secs[0], options[0])
#     print(item)