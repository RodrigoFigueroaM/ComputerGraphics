#version 120\n

uniform highp mat4 projectionMatrix;
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix;


varying vec3 normal;
varying vec4 vertex;


const float edge = 0.5;
const float phong = 0.98;


const vec3 diffuseColor = vec3(1.0, 0.25, 1.0);
const vec3 PhongColor = vec3(0.75, 0.75, 1.0);

const vec3 eyePos = vec3 (0,0,0);

void main()
{
    vec4 tempVertex = modelViewMatrix * vertex;
    vec3 vrtx = tempVertex.xyz / tempVertex.w;

    vec4 tempNormal = normalMatrix * vec4(normal,0.0);
    vec3 nrml =  normalize(tempNormal.xyz);


    vec3 color = diffuseColor;
    float f = dot(vec3(0,0,1),nrml);
    if (abs(f) < edge)
        color = vec3(0);
    if (f > phong)
        color = PhongColor;

    gl_FragColor = vec4(color, 1);

}