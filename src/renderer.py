from typing import TYPE_CHECKING

import pygame as pg
import zengl

from src.shader_programs import ShaderPrograms

if TYPE_CHECKING:
    from src.app import App

from src.camera import Camera


class Renderer:
    def __init__(self, app: "App"):
        self.app = app
        self.window_init()
        self.aspect_ratio = app.screen_size[0] / app.screen_size[1]
        self.shaders = ShaderPrograms()
        self.camera = Camera(self)
        self.ctx = zengl.context()
        self.framebuffer = self.ctx.image(
            (int(app.screen_size.x), int(app.screen_size.y)), 
            'rgba8unorm', 
            samples=4
        )
        self.framebuffer.clear_value = (0.5, 0.0, 0.0, 1.0)

    def window_init(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)  
        pg.display.set_mode(self.app.screen_size, pg.OPENGL | pg.DOUBLEBUF) 

    def render(self):
        self.ctx.new_frame()
        self.framebuffer.clear()
        self.app.curr_scene.render()
        self.framebuffer.blit()
        self.ctx.end_frame()
        pg.display.flip()
