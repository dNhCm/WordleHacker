import os


def get_root() -> str:
    return "/".join(os.path.abspath(__file__).split('\\')[:-2])
