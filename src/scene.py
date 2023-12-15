from typing import TYPE_CHECKING

from src.world import World

if TYPE_CHECKING:
    from src.app import App
    from src.render_obj import RenderObject

from src.render_obj import RenderObject


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
                [20, 20], 
                scrollable=False,
            ),
            RenderObject(
                app,
                [self.entities],
                'button', 
                'default.vert', 
                'default.frag', 
                [20, 100], 
                scrollable=False,
            ),
            RenderObject(
                app,
                [self.entities],
                'button', 
                'default.vert', 
                'default.frag', 
                [20, 180], 
                scrollable=False,
            ),
        ]

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

    def render(self):
        for entity in self.entities:
            entity.render()

    def destroy(self):
        for entity in self.entities:
            entity.render_pipeline.destroy()
