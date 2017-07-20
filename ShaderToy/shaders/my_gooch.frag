# version 330
uniform mat4 projectionMatrix;
uniform mat4 modelViewMatrix;
uniform mat4 normalMatrix;
uniform float time;
uniform sampler2D textureSampler;

in vec4 position;
in vec3 normal;
in vec2 textureCoords;

out vec4 FragColor;

const vec3 lightPos = vec3(0.0, 10.0, 4.0);

const vec3  warmColor = vec3 (0.5, 0.5, 0.0);
const vec3  coolColor = vec3(0.0, 0.0, 0.5);

const vec3 eyePos = vec3 (0,0,0);

const vec3 baseColor = vec3(1.0, 1.0, 1.0);
const vec3 specularColor = vec3(1.0, 1.0, 1.0);

float alpha = 0.3;
float beta = 0.7;

float shininess = 100.0;


void main()
{
    vec4 tempVertex = modelViewMatrix * position;
    vec3 vrtx = tempVertex.xyz / tempVertex.w;

    vec4 tempNormal = normalMatrix * vec4(normal, 1.0);
    vec3 norml = normalize(tempNormal.xyz);

    vec3 text = texture(textureSampler, textureCoords.xy).rgb;
    vec3 coldDiffuse = coolColor + alpha * baseColor;
    vec3 warmDiffuse = warmColor + beta * baseColor;

    vec3 lightDir = normalize(lightPos - vrtx); //L
    float NdotL = dot(lightDir, norml);

    vec3 eyeDir = normalize(eyePos - vrtx);

    //R
    vec3 R = normalize(reflect(-lightDir, norml));
    float RDotV = dot(R,eyeDir);

    //SPECULAR
    vec3 halfVector = normalize(lightDir + eyeDir); //H
    float NdotH = dot(normal, halfVector);

    float  specular = pow( max(RDotV,0.0 ), shininess );
    vec3 spec = specularColor * specular;
//    vec3 kfinal = ((1 + NdotL)/2) * coldDiffuse + (1 - ((1 + NdotL )/2)) * warmDiffuse;
    vec3 kfinal = mix(coldDiffuse, warmDiffuse, NdotL);

    FragColor = vec4( kfinal + spec, 1.0);
}

//precision highp float;
//uniform float time;
//uniform vec2 resolution;
//varying vec3 fPosition;
//varying vec3 fNormal;
//
//uniform mat3 normalMatrix;
//uniform mat4 modelViewMatrix;
//uniform mat4 projectionMatrix;
//
//const vec3 lightPos = vec3(0.0, 10.0, 4.0);
//
//const vec3  warmColor = vec3 (0.4, 0.4, 0.0);
//const vec3  coolColor = vec3(0.0, 0.0, 0.4);
//
//const vec3 eyePos = vec3 (0,0,0);
//
//const vec3 baseColor = vec3(0.0, 0.0, 0.0);
//float alpha = 0.2;
//float beta = 0.6;
//
//float shininess = 160.0;
//
//void main()
//{
//    vec4 tempVertex = modelViewMatrix * vec4(fPosition,1.0);
//    vec3 vrtx = tempVertex.xyz / tempVertex.w;
//
//    vec3 tempNormal = normalMatrix * fNormal;
//    vec3 norml = normalize(tempNormal.xyz);
//
//    vec3 coldDiffuse = coolColor + alpha * baseColor;
//    vec3 warmDiffuse = warmColor + beta * baseColor;
//
//    vec3 lightDir = normalize(lightPos - vrtx); //L
//    float NdotL = dot(lightDir, norml);
//
//    vec3 eyeDir = normalize(eyePos - vrtx);
//
//    //R
//    vec3 R = normalize(reflect(-lightDir, norml));
//    float rDotV = dot(R,eyeDir);
//    //SPECULAR
//    float  specular = pow( max(rDotV,0.0 ), shininess );
//    float a = ((1.0 + NdotL)/2.0);
//    float b = 1.0 - ((1.0 + NdotL )/2.0);
//    vec3 color = a * coldDiffuse + b *warmDiffuse;
//
//  gl_FragColor =  vec4( color + specular, 1.0);
//}
//
