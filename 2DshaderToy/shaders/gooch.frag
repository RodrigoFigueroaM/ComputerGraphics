#version 330

uniform highp mat4 projectionMatrix;
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix;

const vec3 WarmColour = vec3(1.0, 1.0, 1.0);
const vec3 CoolColour = vec3(1.0, 1.0, 1.0);
const vec3 SurfaceColour = vec3(1.0, 0.0, 0.3 );
const float OutlineWidth = 0.0;

in vec3 N;
in vec3 P;
in vec3 V;
in vec3 L;

out vec4 FragColor;
void main()
{
    vec3 l = normalize(L);
    vec3 n = normalize(N);
    vec3 v = normalize(V);
    vec3 h = normalize(l+v);

    float diffuse = dot(l,n);
    float specular = pow(max(dot(n,h), 0.0),32.0);

    vec3 cool = min(CoolColour+SurfaceColour,1.0);
    vec3 warm = min(WarmColour+SurfaceColour,1.0);

    vec3 colour = min(mix(cool,warm,diffuse)+specular,1.0);

    if (dot(n,v)<OutlineWidth) colour=vec3(0,0,0);

    FragColor = vec4(colour,1);
}