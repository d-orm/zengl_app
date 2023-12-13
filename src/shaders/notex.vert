#version 330 core

layout (location = 0) in vec2 in_vert;
out vec2 fragCoord;

void main() {
    fragCoord = in_vert;
    gl_Position = vec4(in_vert, 0.0, 1.0);
}