#version 330

uniform highp mat4 projectionMatrix;
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix;

in vec3 normal;
in vec4 position;

out vec4 FragColor;

const float edge = 0.55;
const float phong = .98;
const vec3 diffuseColor = vec3(0.4, 0.23, 0.8);
const vec3 PhongColor = vec3(0.75, 0.75, 1.0);
const vec3 eyePos = vec3 (0,0,0);

void main()
{
    vec4 tempVertex = modelViewMatrix * position;
    vec3 vrtx = tempVertex.xyz / tempVertex.w;

    vec4 tempNormal = normalMatrix * vec4(normal,0.0);
    vec3 nrml =  normalize(tempNormal.xyz);


    vec3 color = diffuseColor;
    float f = dot(vec3(0,0,1),nrml);
    if (abs(f) < edge)
        color = vec3(0);
    if (f > phong)
        color = PhongColor;

    FragColor = vec4(color, 1);

}