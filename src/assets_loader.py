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
            },
            "button": {
                "Idle": [self.create_button_image((200, 50), (255, 255, 255), (0, 0, 0), 3, 10)],
                "Hover": [self.create_button_image((200, 50), (255, 0, 0), (0, 0, 0), 3, 10)],
            }
        }
    
    def create_button_image(self, size, bg_color, border_color, border_width, border_radius):
        button = pg.Surface(size, pg.SRCALPHA)
        button_rect = button.get_rect()
        pg.draw.rect(button, bg_color, button_rect, border_radius=border_radius)
        pg.draw.rect(button, border_color, button_rect, border_width, border_radius=border_radius)
        return button
