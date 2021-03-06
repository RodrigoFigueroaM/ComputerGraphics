# version 330
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 normalMatrix;

layout(location = 0) in vec3 pos;
layout(location = 2) in vec3 norm;

out vec3 normal;
out vec4 position;

void main()
{
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos,1.0);
    normal = norm;
    position = vec4(pos,1.0);
}
