#version 330 core

uniform sampler2DArray Texture;
in vec3 v_text;

#include "uniforms"

void main() {
    vec3 uv = v_text;
    gl_FragColor = vec4(texture(Texture, uv));
}