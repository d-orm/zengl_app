import asyncio
import sys

import pygame as pg

from src.assets_loader import Assets
from src.renderer import Renderer
from src.controls import Controls
from src.scene import Scene


class App:
    def __init__(self, screen_size = (1600, 900)):
        self.screen_size = pg.Vector2(screen_size)
        self.assets = Assets()
        self.renderer = Renderer(self)
        self.controls = Controls(self)
        self.clock = pg.time.Clock()
        self.running = True
        self.dt = 0.0
        self.elapsed_time = 0.0
        self.curr_scene = Scene(self)

    def update(self):
        self.controls.update()
        self.curr_scene.update()

    async def run(self):
        while self.running:
            await asyncio.sleep(0)
            self.events = pg.event.get()
            for e in self.events:
                self.exit_event(e)
            self.update()
            self.renderer.render()
            self.dt = self.clock.tick() / 1000
            self.elapsed_time = pg.time.get_ticks() / 1000

    def exit_event(self, e: pg.Event):
        esc_key = e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE
        if e.type == pg.QUIT or esc_key:
            self.running = False
            self.curr_scene.destroy()
            pg.quit()
            sys.exit()
