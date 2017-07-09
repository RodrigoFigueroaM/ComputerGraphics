# version 330
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 normalMatrix;

layout(location = 0) in vec3 pos;
layout(location = 1) in vec3 norm;

out vec3 N;
out vec3 P;
out vec3 V;
out vec3 L;

const vec3 LightPos = vec3(0.0, 2.0, 2.0);

void main()
{
    vec4 tempN = normalMatrix * vec4(norm, 0.0) ;
    N = normalize( vec3(tempN.xyz/ tempN.w) );
    P = pos;
    
    V = -vec3(projectionMatrix * modelViewMatrix * vec4(pos, 1.0));
    L = vec3(projectionMatrix * modelViewMatrix * vec4(LightPos - pos, 1.0));
    gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
    
}
