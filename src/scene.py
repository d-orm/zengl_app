from typing import TYPE_CHECKING

from src.camera import Camera
from src.render_obj import RenderObject
from src.world import World

if TYPE_CHECKING:
    from src.app import App


class Scene:
    def __init__(self, app: "App"):
        self.app = app
        self.entities: list["RenderObject"] = []
        self.world = World(app, self)

    def update(self):
        for entity in self.entities:
            entity.update()

        # if self.world.player.rect.colliderect(self.world.bg0.rect):
        #     print('Collision!')

    def render(self):
        for entity in self.entities:
            entity.render()

    def destroy(self):
        for entity in self.entities:
            entity.render_pipeline.destroy()
