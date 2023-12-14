#version 330

#include "uniforms"
out vec4 fragColor;
in vec2 fragCoord;

vec2 camOffsetFragCoord = vec2(fragCoord.x + 1 + iCameraPos.x, fragCoord.y + 1 + iCameraPos.y) / (iResolution.y / iScreenSize.y) / iResolution;

#define nCos(x)		(cos(x)+1.0)*0.5
#define bell(x)		(1.0/((x*x+1.0)*(x*x+1.0)))
//#define bell(x)		(1.0/((1.0+abs(x))*(1.0+abs(x))))
#define rayGen(x) 	((abs((fract(x)-0.5)*2.0)-0.5)*2.0)


#define ITERATIONS 6

//#define USE_BLUE
#define USE_RED
//#define USE_GREEN

float rand(in int x) {
    return fract(sin(0.123456 + 9.87654*float(x))*10000.0);
}
void main()
{
    // Normalized pixel coordinates (from 0 to 1)
    vec2 uv = camOffsetFragCoord;
    uv.x *= iResolution.x/iResolution.y;
    uv = uv - 1.0;
    
    // Ray
    float speed     = 1.5;
    float amplitude = 0.10;
    float freq      = 1.0;
    float parity    = 0.0;
    float dir       = 1.0;
    
    float halo = 0.7 * amplitude;
    
    float ray = 0.0;
    
    // Generate ray that evolve in X and Time with alternative directions (X+, X-)
    for (int i = 0; i < ITERATIONS; i++) {
        ray += amplitude * rayGen(rand(i) + uv.x * (freq + parity) + dir*speed*iTime);
        
        amplitude *=  0.5;
        freq	  *=  2.0;
        parity     =  0.5 - parity;
        dir       *= -1.0;
    }
    
    float intensity = bell(abs(uv.y - ray)/halo);
    
    vec4 color = vec4(0.0,0.0,0.0, 1.0);
    
    #ifdef USE_RED
    	color.x = intensity;
    #endif
    #ifdef USE_GREEN
    	color.y = intensity;
    #endif
    #ifdef USE_BLUE
    	color.z = intensity;
    #endif

    // Output to screen
    fragColor = vec4(color.rgb, color);
}