#version 330
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix; 

const vec4 lightPos = vec4(0.0,0.0,10.0,1.0);
const vec4 lightColor = vec4(0.4,0.0,0.4,1.0);

const vec4 lightPos1 = vec4(0.0,1.0,10.0,1.0);
const vec4 lightColor1 = vec4(0.4,0.0,0.4,1.0);

const vec4 ambientColor = vec4(0.2,0.2,0.2, 1.0);
const vec4 diffuseColor = vec4(0.5,0.5,0.5, 1.0);
const vec4 specColor = vec4(1.0,1.0,1.0,1.0);
const float shininess = 100.0;

const vec4 color = vec4(0.3, 0.0, 0.3, 1.0);

in vec4 position;
in vec3 normal;

out vec4 FragColor;

vec4 ComputeLight (const in vec3 direction, const in vec4 lightcolor, const in vec3 normal, const in vec3 halfvec, const in vec4 mydiffuse, const in vec4 myspecular, const in float myshininess)
{
    float nDotL = dot(normal, direction);
  vec4 lambert = mydiffuse * lightcolor * max (nDotL, 0.0);

  float nDotH = dot(normal, halfvec);
  vec4 phong = myspecular * lightcolor * pow (max(nDotH, 0.0), myshininess);

  vec4 retval = lambert + phong;
  return retval;
}



void main() 
{
    const vec3 eyepos = vec3 (0,0,0);
    vec4 _mypos = modelViewMatrix * position;
    vec3 mypos = _mypos.xyz / _mypos.w;
    vec3 eyedir = normalize(eyepos - mypos);

    vec4 _normal = normalMatrix * vec4(normal,0.0);
    vec3 thisNormal = normalize(_normal.xyz);

    vec3 position0 = lightPos.xyz / lightPos.w;
    vec3 direction0 = normalize(position0 - mypos);
    vec3 half0 = normalize(direction0 + eyedir);
    vec4 color0 = ComputeLight(direction0, lightColor, thisNormal, half0, diffuseColor, specColor, shininess); 
    

    // Light 1, point 
    vec3 position1 = lightPos1.xyz / lightPos1.w;
    vec3 direction1 = normalize(position1 - mypos);
    vec3 half1 = normalize(direction1 + eyedir); 
    vec4 color1 = ComputeLight(direction1, lightColor1, thisNormal, half1, diffuseColor, specColor, shininess) ;



    FragColor = ambientColor + color0 + color1 ;
}
