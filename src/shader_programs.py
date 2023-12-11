from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from src.app import App
    from src.render_pipeline import RenderPipeline


class ShaderPrograms:
    def __init__(self):
        self.paths = [
            'src/shaders/default.vert',
            'src/shaders/default.frag',
            'src/shaders/notex.vert',
            'src/shaders/notex.frag',
            'src/shaders/waving.frag',
        ]
        self.programs = self.load_programs()

    def load_programs(self):
        programs = {}
        for filepath in self.paths:
            shader_name = filepath.split('/')[-1]
            with open(filepath) as f:
                programs[shader_name] = f.read()
        return programs


class Uniforms:
    def __init__(self, app: "App", render_pipeline: "RenderPipeline"):
        self.app = app
        self.render_pipeline = render_pipeline
        self.uniforms_map = {
            'iTime': {
                'value': lambda: np.array(self.app.elapsed_time, dtype='f4'), 
                'glsl_type': 'float'
            },
            'iResolution': {
                'value': lambda: np.array(self.render_pipeline.px_size, dtype='f4'), 
                'glsl_type': 'vec2'
            },
        }       

        self.shaders_map = {
            'default.frag': [],
            'notex.frag': [],
            'waving.frag': ['iTime'],
        }

        self.uniforms = self.get_uniforms()
        self.ubo = app.renderer.ctx.buffer(size=16 + len(self.uniforms) * 8)

    def get_uniforms(self):
        uniforms = {}
        includes_string = ""
        bytes_offset = 0
        frag_shader_id = self.render_pipeline.render_obj.frag_shader_id
        for name, uniform in self.uniforms_map.items():
            if name not in self.shaders_map[frag_shader_id]:
                continue
            uniforms[name] = {
                "value": uniform['value'],
                "glsl_type": uniform['glsl_type'],
                "offset": bytes_offset
            }
            uf_array: np.ndarray = uniform['value']()
            bytes_offset += uf_array.nbytes
            includes_string += f"{uniform['glsl_type']} {name};\n"

        if not uniforms:
            includes_string = "float _pass;"

        self.app.renderer.ctx.includes['uniforms'] = f'''
            layout (std140) uniform Common {{{includes_string}}};
        '''
            
        return uniforms

    def update(self):
        for uniform in self.uniforms.values():
            self.ubo.write(uniform['value'](), offset=uniform['offset'])

