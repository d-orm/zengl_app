import pygame as pg

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.app import App

from src.render_obj import RenderObject


class FontObject:
    def __init__(
            self, 
            app: "App", 
            groups: list[list], 
            text: str, 
            font_id: str,
            px_pos: list[int],
            max_line_len: int = 7,
            x_pad: int = 10,
            y_pad: int = 10,
        ):
        self.app = app
        self.groups = groups
        self.text = text
        self.pos = pg.Vector2(px_pos)
        self.font_id = font_id
        self.num_chars = len(text)
        self.max_line_len = max_line_len if max_line_len > self.num_chars else self.num_chars
        self.px_char_size = int(font_id.split('_')[-1])
        self.x_pad = x_pad
        self.y_pad = y_pad
        self.num_lines = self.num_chars // self.max_line_len
        self.lines: list["RenderObject"] = []
        self.create_lines()
        self.update(text)

    def create_lines(self):
        for line_idx in range(self.num_lines + 1):
            self.lines.extend([RenderObject(
                self.app,
                self.groups,
                self.font_id, 
                'default.vert', 
                'default.frag', 
                [
                    (i * (self.px_char_size + self.x_pad) // 2) + self.pos.x, 
                    (line_idx * (self.px_char_size + self.y_pad)) + self.pos.y
                ], 
                scrollable=False,
                ) for i in range(self.max_line_len)
            ])

    def update(self, text: str):
        self.text = text
        for i, char in enumerate(self.text):
            self.lines[i].state_machine.set_state(char)