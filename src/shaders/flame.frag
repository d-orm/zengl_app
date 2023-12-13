#version 330

#include "uniforms"
out vec4 outColor;
in vec2 fragCoord;
vec2 camOffset = vec2(fragCoord.x + 1 + iCameraPos.x, fragCoord.y + 1 + iCameraPos.y);

void main() {
    
    vec3 color = vec3(camOffset, 0.0);
    outColor = vec4(color, 1.0);
}
