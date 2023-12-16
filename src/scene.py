from typing import TYPE_CHECKING

from src.world import World

if TYPE_CHECKING:
    from src.app import App
    from src.render_obj import RenderObject

from src.render_obj import RenderObject
from src.font_obj import FontObject


class Scene:
    def __init__(self, app: "App"):
        self.app = app
        self.entities: list["RenderObject"] = []
        self.world = World(app, self)
        self.buttons = [
            RenderObject(
                app,
                [self.entities],
                'button', 
                'default.vert', 
                'default.frag', 
                [20, 20 + 75+i*75], 
                scrollable=False,
            ) for i in range(10)
        ]
        self.fps_text = FontObject(
            app, 
            [self.entities], 
            'FPS:000',
            'font_32', 
            [10, 10]
        )            

    def update(self):
        for entity in self.entities:
            entity.update()

        for button in self.buttons:
            if button.rect.collidepoint(self.app.controls.px_mouse_pos):
                button.state_machine.set_state('Hover')
            else:
                button.state_machine.set_state('Idle')

        if self.world.player.rect.colliderect(self.world.water.rect):
            print('Collision!')

        self.fps_text.update(f'FPS:{self.app.clock.get_fps():.0f}')
        

    def render(self):
        for entity in self.entities:
            entity.render()

    def destroy(self):
        for entity in self.entities:
            entity.render_pipeline.destroy()
