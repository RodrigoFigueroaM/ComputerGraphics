# version 330
uniform  mat4 projectionMatrix;
uniform  mat4 modelViewMatrix;
uniform  mat4 normalMatrix;

layout(location = 0) in vec3 pos;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 norm;

void main()
{
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos,1.0);
}