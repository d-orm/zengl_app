from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.app import App
    from src.render_obj import RenderObject


class StateMachine:
    def __init__(self, app: "App", render_object: "RenderObject"):
        self.app = app
        self.render_obj = render_object
        self.render_pipeline = self.render_obj.render_pipeline
        self.animations = self.render_pipeline.animations

    def update(self):
        if not self.animations:
            return
        
        moving_left = self.render_obj.dx < 0
        moving_right = self.render_obj.dx > 0

        if moving_left or moving_right:
            self.set_state('Walk')
            self.set_flip(moving_left)
        else:
            self.set_state('Idle')

    def set_state(self, new_state):
        frame_index_map = self.animations.frames_index_map
        current_state = self.animations.anim_state

        if new_state != current_state:
            self.animations.anim_state = new_state
            self.animations.frame_idx = frame_index_map[new_state][0]

    def set_flip(self, flip_x):
        if flip_x != self.animations.x_flip:
            self.animations.x_flip = flip_x
            self.animations.update_texture_flip()
