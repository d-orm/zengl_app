#version 330

in vec2 fragCoord;
out vec4 fragColor;

#include "uniforms"
#include "fragScaleAndScroll"

vec3 ellipsoidRadius = vec3(2., 4., 2.);      // Ellipsoid radius
vec3 lightSourceDirection = normalize(vec3(-.4, 0., 1.));  // Light source direction
#define AMBIENT_LUMINOSITY .4                 // Ambient luminosity

#define ANIMATION_ENABLED true
#define PI 3.1415927
vec4 accumulatedColor;

mat3 rotationMatrix = mat3( 0.00,  0.80,  0.60,
                            -0.80,  0.36, -0.48,
                            -0.60, -0.48,  0.64 );

float hash(float n) {
    return fract(sin(n) * 43758.5453);
}

float noise(in vec3 x) {
    vec3 p = floor(x);
    vec3 f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    float n = p.x + p.y * 57.0 + 113.0 * p.z;
    return mix(mix(mix(hash(n + 0.0), hash(n + 1.0), f.x),
                   mix(hash(n + 57.0), hash(n + 58.0), f.x), f.y),
               mix(mix(hash(n + 113.0), hash(n + 114.0), f.x),
                   mix(hash(n + 170.0), hash(n + 171.0), f.x), f.y), f.z);
}

float fractalBrownianMotion(vec3 p) {
    if (ANIMATION_ENABLED) p += iTime;
    float f = 0.5000 * noise(p); p = rotationMatrix * p * 2.02;
    f += 0.2500 * noise(p); p = rotationMatrix * p * 2.03;
    f += 0.1250 * noise(p); p = rotationMatrix * p * 2.01;
    f += 0.0625 * noise(p);
    return f;
}

float signedNoise(in vec3 x) {
    return 2.0 * noise(x) - 1.0;
}

float signedFractalBrownianMotion(vec3 p) {
    if (ANIMATION_ENABLED) p += iTime;
    float f = 0.5000 * signedNoise(p); p = rotationMatrix * p * 2.02;
    f += 0.2500 * signedNoise(p); p = rotationMatrix * p * 2.03;
    f += 0.1250 * signedNoise(p); p = rotationMatrix * p * 2.01;
    f += 0.0625 * signedNoise(p);
    return f;
}

mat3 lookAt(vec3 origin, vec3 target, float distance) {
    vec3 direction = normalize(target - origin);
    mat3 matrix;
    matrix[0] = direction;
    matrix[2] = normalize(vec3(0.0, 0.0, 1.0) - direction.z * direction) / distance;
    matrix[1] = cross(matrix[2], direction);
    return matrix;
}

bool intersectEllipsoid(vec3 origin, vec3 rayDirection, out vec3 intersectionPoint, out vec3 normal, out float thickness) {
    vec3 scaledOrigin = origin / ellipsoidRadius, scaledDirection = rayDirection / ellipsoidRadius;
    float dotProductOriginDirection = dot(scaledOrigin, scaledDirection), originSquared = dot(scaledOrigin, scaledOrigin), directionSquared = dot(scaledDirection, scaledDirection);
    float discriminant = dotProductOriginDirection * dotProductOriginDirection - (originSquared - 1.0) * directionSquared;
    
    if (!(discriminant >= 0.0 && dotProductOriginDirection < 0.0 && originSquared > 1.0)) return false;
    
    float intersectionDistance = (-dotProductOriginDirection - sqrt(discriminant)) / directionSquared;
    intersectionPoint = origin + intersectionDistance * rayDirection;
    normal = normalize(intersectionPoint / (ellipsoidRadius * ellipsoidRadius));
    thickness = 2.0 * sqrt(discriminant) / directionSquared;
    return true;
}

float silhouetteSmoothness, silhouettePower, interiorIntensity, interiorPower;

void drawObject(vec3 cameraPosition, mat3 viewMatrix, vec2 screenPosition) {
    vec3 rayDirection = normalize(viewMatrix * vec3(1.0, screenPosition));
    
    vec3 intersectionPoint, normal;
    float thickness;
    if (!intersectEllipsoid(cameraPosition, rayDirection, intersectionPoint, normal, thickness)) return;
    
    vec3 midPoint = intersectionPoint + 0.5 * thickness * rayDirection;
    vec3 midPointNormal = normalize(midPoint / (ellipsoidRadius * ellipsoidRadius));
    vec3 normalizedIntersection = normalize(intersectionPoint / ellipsoidRadius);
    
    float lightFacingRatio = clamp(dot(normal, lightSourceDirection), 0.0, 1.0);
    float cameraFacingRatio = clamp(-dot(normalizedIntersection, rayDirection), 0.0, 1.0);

    float surfaceNoise = fractalBrownianMotion(intersectionPoint), interiorNoise = fractalBrownianMotion(midPoint + 10.0);
    thickness = clamp(thickness - 6.0 * interiorNoise, 0.0, 1e10);
    
    float silhouetteStrength = pow(silhouetteSmoothness * cameraFacingRatio, silhouettePower);
    float interiorStrength = 1.0 - pow(0.7, interiorPower * thickness);
    
    silhouetteStrength = clamp(silhouetteStrength - surfaceNoise, 0.0, 1.0) * 2.0;
    float alpha = 1.0 - (1.0 - silhouetteStrength) * (1.0 - interiorStrength);
    alpha = clamp(alpha, 0.0, 1.0);
    lightFacingRatio = 0.8 * (lightFacingRatio + fractalBrownianMotion(midPoint - 10.0));
    
    vec4 color = vec4(mix(lightFacingRatio, 1.0, AMBIENT_LUMINOSITY));
    accumulatedColor = mix(accumulatedColor, color, alpha);
}

void main() {
    vec2 uv = fragScaleAndScroll();
    float cameraElevationAngle = 0.2;
    
    silhouetteSmoothness = 1.0; silhouettePower = 3.0; interiorIntensity = 0.9; interiorPower = 3.0;
    vec3 cameraPosition = vec3(-15.0 * cos(iTime) * cos(cameraElevationAngle), 15.0 * sin(iTime) * cos(cameraElevationAngle), 15.0 * sin(cameraElevationAngle));
    mat3 viewMatrix = lookAt(cameraPosition, vec3(0.0), 5.0);
    
    drawObject(cameraPosition, viewMatrix, uv);
    fragColor = accumulatedColor;
}
