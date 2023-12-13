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
            'src/shaders/flame.frag',
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
            'iWorldPos': {
                'value': lambda: np.array(self.render_pipeline.gl_pos, dtype='f4'), 
                'glsl_type': 'vec2'
            },     
            'iCameraPos': {
                'value': lambda: np.array(self.app.renderer.camera.position, dtype='f4'), 
                'glsl_type': 'vec2'
            },                         
        }       

        self.shaders_map = {
            'default.vert': ['iCameraPos'],
            'default.frag': [],
            'notex.frag': ['iTime', 'iResolution', 'iWorldPos'],
            'waving.frag': ['iTime'],
            'flame.frag': ['iTime', 'iResolution', 'iCameraPos'],
        }

        self.uniforms = self.get_uniforms()
        self.ubo = app.renderer.ctx.buffer(size=16+self.buffer_size)

    def get_uniforms(self):
        uniforms = {}
        includes_string = ""
        offset = 0
        for name, uniform in self.uniforms_map.items():
            if name not in self.shaders_map[self.render_pipeline.render_obj.frag_shader_id]:
                continue

            if uniform['glsl_type'] == 'float':
                align = 4
            elif uniform['glsl_type'] == 'vec2':
                align = 8
            elif uniform['glsl_type'] in ['vec3', 'vec4']:
                align = 16
            else:
                raise ValueError(f"Unknown GLSL type: {uniform['glsl_type']}")

            # Add padding for alignment
            if offset % align != 0:
                offset += align - (offset % align)

            uniforms[name] = {
                "value": uniform['value'],
                "glsl_type": uniform['glsl_type'],
                "offset": offset
            }
            uf_array = uniform['value']()
            offset += uf_array.nbytes
            includes_string += f"{uniform['glsl_type']} {name};\n"

        self.buffer_size = offset

        if not uniforms:
            includes_string = "float _pass;"

        self.app.renderer.ctx.includes['uniforms'] = f'''
            layout (std140) uniform Common {{{includes_string}}};
        '''
            
        return uniforms

    def update(self):
        print(self.app.renderer.camera.position)
        for uniform in self.uniforms.values():
            self.ubo.write(uniform['value'](), offset=uniform['offset'])

