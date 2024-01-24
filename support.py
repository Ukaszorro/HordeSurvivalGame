from os import walk
import re

import pygame


def ctoi(text):
    """ turn digits in a text to int """
    return int(text) if text.isdigit() else text


def human_sorting(text):
    return [ctoi(c) for c in re.split(r'(\d+)', text)]


def import_folder(path):
    surface_list = []

    # walk through directory, turn images in that directory to surfaces, add them to the list
    for first, second, img_files in walk(path):
        img_files.sort(key=human_sorting)
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


#import_folder("images/Top_Down_Survivor/handgun/idle")