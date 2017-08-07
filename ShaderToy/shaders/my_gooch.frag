#version 330
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

const vec3  warmColor = vec3 (0.4, 0.4, 0.0);
const vec3  coolColor = vec3(0.0, 0.0, 0.4);

const vec3 eyePos = vec3 (0,0,0);

const vec3 baseColor = vec3(1.0, 1.0, 1.0);
const vec3 specularColor = vec3(1.0, 1.0, 1.0);

float alpha = 0.4;
float beta = 0.5;

float shininess = 100.0;


void main()
{
    vec4 tempVertex = modelViewMatrix * position;
    vec3 vrtx = tempVertex.xyz / tempVertex.w;

    vec4 tempNormal = normalMatrix * vec4(normal, 1.0);
    vec3 norml = normalize(tempNormal.xyz);

    vec3 text = texture(textureSampler, textureCoords.xy).rgb;
    vec3 coolDiffuse = coolColor + alpha * baseColor;
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
    float diffuse = (1 + NdotL)/2;
   vec3 kfinal = diffuse * warmDiffuse + (1 - diffuse) * coolDiffuse;
    //vec3 kfinal = mix(coolDiffuse, warmDiffuse, NdotL);

    FragColor = vec4( kfinal + spec, 1.0);
}