# version 330
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 normalMatrix;

layout(location = 0) in vec3 pos;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 norm;

out vec3 normal;
out vec4 position;
out vec2 textureCoords;

void main()
{
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos,1.0);
    normal = norm;
    position = vec4(pos,1.0);
    textureCoords = pos.xy*0.5f + 0.5;
}
