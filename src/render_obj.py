from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from src.app import App

from src.render_pipeline import RenderPipeline
from src.state_machine import StateMachine


class RenderObject:
    def __init__(
            self, 
            app: "App", 
            groups: list[list],
            images_id: str, 
            vert_shader_id: str, 
            frag_shader_id: str, 
            px_pos: list[int], 
            scale: list[float]=[1.0, 1.0],
            scrollable: bool=True,
        ):
        self.app = app
        self.groups = groups
        self.images_id = images_id
        self.vert_shader_id = vert_shader_id
        self.frag_shader_id = frag_shader_id
        self.px_pos = pg.Vector2(px_pos)
        self.scale = pg.Vector2(scale)
        self.scrollable = scrollable
        self.render_pipeline = RenderPipeline(app, self)
        self.state_machine = StateMachine(app, self)
        self.rect = self.render_pipeline.get_px_rect()
        self.dx, self.dy = 0.0, 0.0
        self.add_to_groups()

    def update(self):
        self.state_machine.update()
        self.render_pipeline.animate()

    def render(self):
        self.render_pipeline.render()

    def move(self, delta_x: float, delta_y: float):
        self.render_pipeline.move(delta_x, delta_y)
        self.update_rect()

    def resize(self, scale_x: float, scale_y: float):
        self.render_pipeline.resize(scale_x, scale_y)
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = self.px_pos
        self.rect.size = self.render_pipeline.px_size

    def add_to_groups(self):
        for group in self.groups:
            group.append(self)
