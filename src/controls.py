from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from src.app import App


class Controls:
    def __init__(self, app: "App"):
        self.app = app
        self.keys = pg.key.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_buttons = pg.mouse.get_pressed()

    def move_camera(self):
        speed = 1.0 * self.app.dt
        dx, dy = 0.0, 0.0
        if self.keys[pg.K_j]:
            dx -= speed
        if self.keys[pg.K_l]:
            dx += speed
        if self.keys[pg.K_i]:
            dy += speed
        if self.keys[pg.K_k]:
            dy -= speed
        if dx != 0.0 or dy != 0.0:
            self.app.curr_scene.camera.move(dx, dy)

    def move_player(self):
        player = self.app.curr_scene.world.player
        player.dx, player.dy = 0, 0
        speed = 1.0 * self.app.dt

        if self.keys[pg.K_LEFT]:
            player.dx -= speed
        if self.keys[pg.K_RIGHT]:
            player.dx += speed
        if self.keys[pg.K_UP]:
            player.dy += speed
        if self.keys[pg.K_DOWN]:
            player.dy -= speed

        if player.dx != 0 or player.dy != 0:
            player.move(player.dx, player.dy)

    def resize_player(self):
        dx, dy = 1.0, 1.0
        speed = 1.0 * self.app.dt
        if self.keys[pg.K_a]:
            dx -= speed
        if self.keys[pg.K_d]:
            dx += speed
        if self.keys[pg.K_w]:
            dy -= speed
        if self.keys[pg.K_s]:
            dy += speed
        if dx != 1.0 or dy != 1.0:
            self.app.curr_scene.world.player.resize(dx, dy)

    def update(self):
        self.keys = pg.key.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse_buttons = pg.mouse.get_pressed()
        self.move_camera()
        self.move_player()
        self.resize_player()

