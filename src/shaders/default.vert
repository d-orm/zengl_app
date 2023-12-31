#version 330 core

layout (location = 0) in vec2 in_vert;
layout (location = 1) in vec2 in_tex;
layout (location = 2) in float frameIdx;

out vec3 v_text;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    v_text = vec3(in_tex, frameIdx);
}