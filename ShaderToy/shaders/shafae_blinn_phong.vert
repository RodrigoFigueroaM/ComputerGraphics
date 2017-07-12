# version 330
uniform highp mat4 projectionMatrix;
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix; 

layout(location = 0) in highp vec4 pos;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 norm;

out vec4 position;
out vec3 normal;

void main() 
{
    gl_Position =  projectionMatrix * modelViewMatrix * pos;
    normal =  norm;
    position = pos;
}