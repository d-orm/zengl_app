from typing import TYPE_CHECKING

import pygame as pg
import numpy as np

if TYPE_CHECKING:
    from src.render_pipeline import RenderPipeline


class Camera:
    def __init__(self):
        self.position = pg.Vector2(0, 0)

    def move(self, delta_x, delta_y):
        self.position.x += delta_x
        self.position.y += delta_y

    def apply(self, render_pipeline: "RenderPipeline"):
        modified_vertices = np.array(render_pipeline.vertices)
        
        for i in range(0, len(modified_vertices), render_pipeline.stride):
            modified_vertices[i] -= self.position.x
            modified_vertices[i + 1] -= self.position.y

        return modified_vertices
        
 