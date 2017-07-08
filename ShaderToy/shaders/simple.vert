# version 330
uniform  mat4 projectionMatrix;
uniform  mat4 modelViewMatrix;
//uniform highp mat4 normalMatrix;

layout(location = 0) in vec3 pos;
//layout(location = 1) in vec3 color;
out vec4 col;

void main()
{
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos,1.0);
    col = vec4(pos,1.0);
    
}
