from typing import TYPE_CHECKING

import pygame as pg
import zengl
import numpy as np

if TYPE_CHECKING:
    from src.app import App
    from src.render_obj import RenderObject

from src.shader_programs import Uniforms
from src.animations import Animations


class RenderPipeline:
    def __init__(self, app: "App", render_obj: "RenderObject"):
        self.app = app
        self.render_obj = render_obj
        self.renderer = app.renderer
        self.vert_shader = self.renderer.shaders.programs[render_obj.vert_shader_id]
        self.frag_shader = self.renderer.shaders.programs[render_obj.frag_shader_id]
        self.camera = app.renderer.camera
        self.animations = self.get_animations()
        self.px_size = self.get_px_size()
        self.aspect_ratio = self.px_size.x / self.px_size.y
        self.gl_size = self.get_gl_size()
        self.gl_pos = self.get_gl_pos()
        self.texture = self.get_tex_array()
        self.vertices = self.get_vertices()
        self.uniforms = Uniforms(app, self)
        self.vbo = self.renderer.ctx.buffer(data=self.vertices.tobytes())
        self.vao = self.create_vao()
        self.xy_vert_pos = 0
        self.tex_vert_pos = 2
        self.frame_vert_pos = 4
        self.stride = 5 if self.texture else 2
        self.resize(*self.get_size_ratio())

    def render(self):
        if self.render_obj.scrollable and self.camera.moving:
            modified_vertices = self.camera.apply(self)
        else:
            modified_vertices = self.vertices
        self.vbo.write(modified_vertices.tobytes())        
        self.uniforms.update()
        self.vao.render() 

    def animate(self):
        if self.texture:
            self.animations.animate_frames()

    def get_px_size(self) -> pg.Vector2:
        if isinstance(self.render_obj.images_id, list | tuple | pg.Vector2):
            return pg.Vector2(self.render_obj.images_id)
        else:
            return pg.Vector2(self.animations.frames[0].get_size())
        
    def get_animations(self) -> Animations | None:
        if isinstance(self.render_obj.images_id, list | tuple | pg.Vector2):
            return None
        return Animations(self.app, self)
    
    def get_tex_array(self) -> zengl.Image | None:
        if isinstance(self.render_obj.images_id, list | tuple | pg.Vector2):
            return None
        
        texture = self.renderer.ctx.image(
            (int(self.px_size.x), int(self.px_size.y)), 
            'rgba8unorm', 
            array=len(self.animations.frames)
        )
        for i in range(len(self.animations.frames)):
            texture.write(
                pg.image.tobytes(self.animations.frames[i], 'RGBA', True), 
                layer=i
            )
        texture.mipmaps()
        return texture
    
    def get_vertices(self) -> np.ndarray:
        screen_aspect = self.renderer.aspect_ratio
        x = self.aspect_ratio / screen_aspect if self.aspect_ratio < screen_aspect else 1.0
        y = screen_aspect / self.aspect_ratio if self.aspect_ratio > screen_aspect else 1.0
        w = self.gl_pos.x + self.gl_size.x / 2
        h = -self.gl_pos.y - self.gl_size.y / 2

        if self.texture:
            tx, ty = self.animations.x_flip, self.animations.y_flip
            frame_idx = self.animations.frame_idx
            return np.array([ 
                -x + w,  y - h,     tx,     ty, frame_idx,
                 x + w,  y - h, not tx,     ty, frame_idx,
                -x + w, -y - h,     tx, not ty, frame_idx,
                -x + w, -y - h,     tx, not ty, frame_idx,
                 x + w,  y - h, not tx,     ty, frame_idx,
                 x + w, -y - h, not tx, not ty, frame_idx,
            ], dtype='f4')
        
        else:
            return np.array([ 
            -x + w,  y - h,
             x + w,  y - h,
            -x + w, -y - h,
            -x + w, -y - h,
             x + w,  y - h,
             x + w, -y - h,
        ], dtype='f4')
                  
    def create_vao(self) -> zengl.Pipeline:
        tex_sampler = [{
                    'type': 'sampler', 
                    'binding': 0, 
                    'image': self.texture,
                    'min_filter': 'linear_mipmap_nearest',
                    'mag_filter': 'linear',
        }] if self.texture else []
        
        tex_layout = [{'name': 'Texture', 'binding': 0}] if self.texture else []
        buffer_format = '2f 2f 1f' if self.texture else '2f'
        buffer_layout = (0, 1, 2) if self.texture else (0,)

        return self.renderer.ctx.pipeline(
            vertex_shader=self.vert_shader,
            fragment_shader=self.frag_shader,
            layout=[{'name': 'Common', 'binding': 0}
                ] + tex_layout,
            resources=[{'type': 'uniform_buffer', 'binding': 0, 'buffer': self.uniforms.ubo}
                ] + tex_sampler,
            blend={"enable": True,"src_color": "src_alpha", "dst_color": "one_minus_src_alpha"},                
            framebuffer=[self.renderer.framebuffer],
            topology='triangles',
            vertex_buffers=zengl.bind(self.vbo, buffer_format, *buffer_layout),
            vertex_count=self.vbo.size // zengl.calcsize(buffer_format),
        )       

    def move(self, delta_x: float, delta_y: float):
        for i in range(self.xy_vert_pos, len(self.vertices), self.stride):
            self.vertices[i] += delta_x
            self.vertices[i + 1] += delta_y
        self.gl_pos.x = self.vertices[0]
        self.gl_pos.y = self.vertices[1] - self.gl_size.y

    def resize(self, scale_x: float, scale_y: float):
        for i in range(self.xy_vert_pos, len(self.vertices), self.stride):
            self.vertices[i] = (self.vertices[i] - self.gl_pos.x) * scale_x + self.gl_pos.x
            self.vertices[i + 1] = (self.vertices[i+1] - self.gl_pos.y) * scale_y + self.gl_pos.y
        self.gl_size.x *= scale_x
        self.gl_size.y *= scale_y
        self.px_size.x = self.gl_size.x * self.app.screen_size.x / 2
        self.px_size.y = self.gl_size.y * -self.app.screen_size.y / 2

    def get_gl_size(self) -> pg.Vector2:
        if self.aspect_ratio > self.renderer.aspect_ratio:
            return pg.Vector2(1.0, self.renderer.aspect_ratio / self.aspect_ratio) * 2
        else:
            return pg.Vector2(self.aspect_ratio / self.renderer.aspect_ratio, 1.0) * 2  
    
    def get_gl_pos(self) -> pg.Vector2:
        gl_pos_x = (self.render_obj.px_pos.x / self.app.screen_size.x) * 2 - 1
        gl_pos_y = (-self.render_obj.px_pos.y / self.app.screen_size.y) * 2 + 1
        return pg.Vector2(gl_pos_x, gl_pos_y)

    def get_size_ratio(self) -> tuple[float, float]:
        scale = max(
            self.render_obj.scale.x * self.px_size.x / self.app.screen_size.x,
            self.render_obj.scale.y * self.px_size.y / self.app.screen_size.y,
        )
        return scale, -scale
        
    def get_rect(self) -> pg.FRect:
        return pg.FRect(*self.gl_pos, *self.gl_size)
    
    def destroy(self):
        for resource in [self.vao, self.vbo, self.uniforms.ubo, self.texture]:
            self.renderer.ctx.release(resource)
