# version 330
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 normalMatrix;

layout(location = 0) in vec3 pos;
layout(location = 1) in vec3 textCoords;
layout(location = 2) in vec3 norm;

const vec3 lightPosition = vec3(0.0, 2.0, 2.0);

out vec3 normal;
out vec4 position;
out vec2 textureCoords;


out float NdotL;
out vec3 ReflectVec;
out vec3 ViewVec;

void main()
{
    vec3 ecPos      = vec3 (0.0,0.0,0.0);
    vec3 tnorm      = normalize(normalMatrix * vec4(norm, 1.0)).xyz;
    vec3 lightVec   = normalize(lightPosition - ecPos);
    ReflectVec      = normalize(reflect(-lightVec, tnorm));
    ViewVec         = normalize(-ecPos);
    NdotL           = (dot(lightVec, tnorm) + 1.0) * 0.5;
    gl_Position     = projectionMatrix * modelViewMatrix * vec4(pos,1.0);
    
}
