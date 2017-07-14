# version 330
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 normalMatrix;
uniform float time;


layout(location = 0) in vec3 pos;
layout(location = 1) in vec2 textCoords;
layout(location = 2) in vec3 norm;

out vec3 normal;
out vec4 position;
out vec2 textureCoords;

mat4 rotate(float _angle){
    return mat4(cos(_angle),0, -sin(_angle),0,
                0,1,0,0,
                sin(_angle),0,cos(_angle),0,
                0,0,0,1);
}

void main()
{
    gl_Position = projectionMatrix * modelViewMatrix * rotate(time) * vec4(pos,1.0);
    normal = norm;
    position = vec4(pos,1.0);
    textureCoords = pos.xy*0.5f + 0.5;
}
