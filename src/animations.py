from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from src.app import App
    from src.render_pipeline import RenderPipeline


class Animations:
    def __init__(self, app: "App", render_pipeline: "RenderPipeline"):
        self.app = app
        self.render_pipeline = render_pipeline
        self.render_obj = render_pipeline.render_obj
        self.images: dict[str, list[pg.Surface]] = app.assets.images[self.render_obj.images_id]
        self.frames, self.frames_index_map = self.get_frames_map()
        self.anim_state = 'Idle'
        self.frame_idx = self.frames_index_map[self.anim_state][0]
        self.anim_speed = 20
        self.x_flip = False
        self.y_flip = False

    def get_frames_map(self):
        frames: list[pg.Surface] = []
        frames_index_map = {}
        frame_counter = 0
        for anim_name, frame_list in self.images.items():
            frames_index_map[anim_name] = (frame_counter, frame_counter + len(frame_list) -1)
            frame_counter += len(frame_list)
            frames.extend(frame_list) 
        return frames, frames_index_map
    
    def animate_frames(self):
        render_pipeline = self.render_obj.render_pipeline
        first_frame, last_frame = self.frames_index_map[self.anim_state]

        self.frame_idx += self.app.dt / (1.0 / self.anim_speed)

        if self.frame_idx >= last_frame:
            self.frame_idx = first_frame

        for i in range(
            render_pipeline.frame_vert_pos, len(render_pipeline.vertices), render_pipeline.stride):
            render_pipeline.vertices[i] = int(self.frame_idx)

    def update_texture_flip(self):
        render_pipeline = self.render_obj.render_pipeline
        stride = render_pipeline.stride
        
        for i in range(render_pipeline.tex_vert_pos, len(render_pipeline.vertices), stride):
            render_pipeline.vertices[i] = 1.0 - render_pipeline.vertices[i]
                