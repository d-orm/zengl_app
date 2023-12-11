#version 330 core

uniform sampler2DArray Texture;
in vec3 v_text;

#include "uniforms"

void main() {
    vec3 uv = v_text;
    uv.x += sin(uv.y * 10.0 + iTime) * 0.1;
    gl_FragColor = vec4(texture(Texture, uv));
}