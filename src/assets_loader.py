import os

import pygame as pg


class Assets:
    def __init__(self):
        self.images = self.load_images()

    def load_images(self) -> dict[str, list[pg.Surface]]:
        return {
            "grass_1": {"Idle": [pg.image.load('assets/grass10.jpg')]},
            "player": {
                "Idle": [
                    pg.image.load(f'assets/Player/Idle/Idle Blinking_00{i}.png')
                    for i in range(0, 18)
                    ],
                "Walk": [
                    pg.image.load(f'assets/Player/Walk/Running_00{i}.png')
                    for i in range(0, 14)
                    ]
            }
        }
    
