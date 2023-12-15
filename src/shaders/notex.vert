#version 330 core

layout (location = 0) in vec2 in_vert;
out vec2 fragCoord;

#include "uniforms"

void main() {
    vec2 wolrdPos = vec2(iWorldPos.x + 1.0, iWorldPos.y - 1.0);
    fragCoord = in_vert - wolrdPos;
    gl_Position = vec4(in_vert, 0.0, 1.0);
}