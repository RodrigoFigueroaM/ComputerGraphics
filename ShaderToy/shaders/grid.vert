# version 330
uniform  mat4 projectionMatrix;
uniform  mat4 modelViewMatrix;
uniform  mat4 normalMatrix;
uniform  mat4 modelTransformationMatrix;

layout(location = 0) in vec3 pos;
layout(location = 1) in vec3 textCoords;
layout(location = 2) in vec3 norm;

void main()
{
    gl_Position = projectionMatrix * modelViewMatrix * modelTransformationMatrix * vec4(pos,1.0);
}
