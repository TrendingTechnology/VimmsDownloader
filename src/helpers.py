"""Helper functions for the main script"""
from typing import List
import os
import sys
from src import models

selections: list[dict[int, str]] = [
    {
        0: 'NES'
    },
    {
        1: 'Genesis'
    },
    {
        2: 'SNES'
    },
    {
        3: 'Saturn'
    },
    {
        4: 'Playstation'
    },
    {
        5: 'N64'
    },
    {
        6: 'Dreamcast'
    },
    {
        7: 'Playstation-2'
    },
    {
        8: 'Xbox'
    },
    {
        9: 'Gamecube'
    },
    {
        10: 'Playstation-3'
    },
    {
        11: 'Wii'
    },
    {
        12: 'WiiWare'
    },
    {
        13: 'Game-Boy'
    },
    {
        14: 'Game-Boy-Color'
    },
    {
        15: 'Game-Boy-Advanced'
    },
    {
        16: 'Nintendo-DS'
    },
    {
        17: 'PSP'
    },
]

__to_uri: dict[str, str] = {
    'NES': 'NES',
    'Genesis': 'Genesis',
    'SNES': 'SNES',
    'Saturn': 'Saturn',
    'Playstation': 'PS1',
    'N64': 'N64',
    'Dreamcast': 'Dreamcast',
    'Playstation-2': 'PS2',
    'Xbox': 'Xbox',
    'Gamecube': 'GameCube',
    'Playstation-3': 'PS3',
    'Wii': 'Wii',
    'WiiWare': 'WiiWare',
    'Game-Boy': 'GB',
    'Game-Boy-Color': 'GBC',
    'Game-Boy-Advanced': 'GBA',
    'Nintendo-DS': 'DS',
    'PSP': 'PSP',
}


def __create_alpha_num_structure(path: str, system: str):
    dirnames: list[str] = [
        '#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    try:
        for x in dirnames:
            os.mkdir(os.path.join(path, 'ROMS', system, x))
    except:
        e = sys.exc_info()[0]
        print('Failed Creating AlphaNum Structure')
        print(e)


def __create_rom_home_dir(path: str):
    try:
        os.mkdir(os.path.join(path, 'ROMS'))
    except:
        e = sys.exc_info()[0]
        print('Failed Creating Home Directory')
        print(e)


def __create_rom_system_dir(path: str, system: str):
    try:
        os.mkdir(os.path.join(path, 'ROMS', system))
    except:
        e = sys.exc_info()[0]
        print('Failed Creating ROM System Directory')
        print(e)


def __check_if_home_dir_created(path: str):
    for x in os.listdir(path):
        if x == 'ROMS':
            return True


def __check_if_system_dir_created(path: str, system: str):
    for x in os.listdir(os.path.join(path, 'ROMS')):
        if x == system:
            return True


def __create_all_no_home(path):
    __create_rom_home_dir(path)
    for x in selections:
        for value in x:
            if not __check_if_system_dir_created(path, x[value]):
                __create_rom_system_dir(path, x[value])
                __create_alpha_num_structure(path, x[value])


def __create_all_w_home(path):
    for x in selections:
        for value in x:
            if not __check_if_system_dir_created(path, x[value]):
                __create_rom_system_dir(path, x[value])
                __create_alpha_num_structure(path, x[value])


def __create_sel_w_home(path, userselections: List[str]):
    for x in userselections:
        if not __check_if_system_dir_created(path, selections[int(x)][int(x)]):
            __create_rom_system_dir(path, selections[int(x)][int(x)])
            __create_alpha_num_structure(path, selections[int(x)][int(x)])


def __create_sel_no_home(path, userselections: List[str]):
    __create_rom_home_dir(path)
    for x in userselections:
        if not __check_if_system_dir_created(path, selections[int(x)][int(x)]):
            __create_rom_system_dir(path, selections[int(x)][int(x)])
            __create_alpha_num_structure(path, selections[int(x)][int(x)])


def create_directory_structure(config: models.Config, path: str):
    if config.All:
        if not __check_if_home_dir_created(path):
            __create_all_no_home(path)
        if __check_if_home_dir_created(path):
            __create_all_w_home(path)
    if not config.All:
        if not __check_if_home_dir_created(path):
            __create_sel_no_home(path, config.Selections)
        if __check_if_home_dir_created(path):
            __create_sel_w_home(path, config.Selections)


def selection_to_uri(selection: str):
    return __to_uri[selection]


def print_console_list():
    for x in range(0, 9):
        print(
            f'{x:5d} ==> {selections[x][x]:15} | {x+9:5d} ==> {selections[x+9][x+9]:10}'
        )
