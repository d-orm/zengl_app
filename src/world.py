import pygame as pg

from typing import TYPE_CHECKING

from src.render_obj import RenderObject

if TYPE_CHECKING:
    from src.app import App
    from src.scene import Scene


class World:
    def __init__(self, app: "App", scene: "Scene"):
        self.app = app
        self.scene = scene
        self.bg0 = RenderObject(
            app,
            [self.scene.entities],
            'grass_1', 
            'default.vert', 
            'default.frag', 
            [0.0, 0.0], 
        )
        self.water = RenderObject(
            app,
            [self.scene.entities],
            app.screen_size/2, 
            'notex.vert', 
            'water2.frag', 
            [1500, 330],
            [1, 1],
        )
        self.fire = RenderObject(
            app,
            [self.scene.entities],
            app.screen_size, 
            'notex.vert', 
            'flame.frag', 
            [0, 0],
        )
        self.orb = RenderObject(
            app,
            [self.scene.entities],
            app.screen_size/2, 
            'notex.vert', 
            'electric_bolt.frag', 
            [400, 900],
        )
        self.player = RenderObject(
            app,
            [self.scene.entities],
            'player', 
            'default.vert', 
            'default.frag', 
            [800, 450], 
            [0.5, 0.5],
        )
        self.smoke = RenderObject(
            app,
            [self.scene.entities],
            app.screen_size/2, 
            'notex.vert', 
            'smoke.frag', 
            [600, 600],
        )