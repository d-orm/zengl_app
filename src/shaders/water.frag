#version 330

#include "uniforms"
out vec4 fragColor;
in vec2 fragCoord;

vec2 camOffsetFragCoord = vec2(fragCoord.x + 1 + iCameraPos.x, fragCoord.y + 1 + iCameraPos.y) / (iResolution.y / iScreenSize.y);

vec2 random2( vec2 p ) {
    return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(0.670,0.330))))*43758.5453);
}

void main()
{
    vec2 st = camOffsetFragCoord.xy;
    st.x *= iResolution.x / iResolution.y;

    vec3 color = vec3(0.129,0.454,0.925);
    // Tile the space
    vec2 i_st = floor(st);
    vec2 f_st = fract(st);

    float m_dist = 1.;  // minimum distance

    for (int y= -1; y <= 1; y++) {
        for (int x= -1; x <= 1; x++) {
            // Neighbor place in the grid
            vec2 neighbor = vec2(float(x),float(y));

            // Random position from current + neighbor place in the grid
            vec2 point = random2(i_st + neighbor);

			// Animate the point
            point = 0.5 + 0.5*sin(iTime + 6.2831*point);

			// Vector between the pixel and the point
            vec2 diff = neighbor + point - f_st;

            // Distance to the point
            float dist = length(diff);

            // Keep the closer distance
            m_dist = min(m_dist, dist * m_dist);
        }
    }

    // Draw the min distance (distance field)
    color += m_dist;
    
    // Show isolines
    color -= step(0.988,abs(sin(30.*m_dist)))*.5;

    fragColor = vec4(color,1.0);
}