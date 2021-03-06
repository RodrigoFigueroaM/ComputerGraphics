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

vec3 lightPos = vec3(0.0, 2.0, 2.0);
const vec3 lightColor = vec3(0.0, 0.0, 1.0);

const vec3 ambientColor = vec3(0.2, 0.2, 0.2);
const vec3 diffuseColor = vec3(0.5, 0.5, 0.5);
const vec3 specularColor = vec3(1.0, 1.0, 1.0);

const vec3 emitColor = vec3(0.0, 0.0, 1.0);
const float shininess = 160.0;
const vec3 eyePos = vec3 (0,0,0);

const vec4 color = vec4(0.443, 0.0, 0.323, 1.0);

vec3 redLightPos = vec3(0.0, 0.0, 2.0);
const vec3 redLightColor = vec3(1.0, 0.0, 0.0);


mat4 rotate(float _angle){
    return mat4(cos(_angle),0, -sin(_angle),0,
                0,1,0,0,
                sin(_angle),0,cos(_angle),0,
                0,0,0,1);
}

vec3 computeLigth(const in vec3 normal, const in vec3 direction, const in vec3 diffuseColor,
                  const in vec3 lightColor, const in vec3 halfVector, const in vec3 specularColor,
                  const in float shininess)
{
    //DIFFUSE
    float NdotL = dot(normal, direction );
    vec3 lambert = NdotL * diffuseColor * lightColor * max(NdotL ,0.0);
    //SPECULAR
    float NdotH = dot(normal, halfVector);
    vec3  blinnPhong = lightColor * specularColor * pow( max(NdotH,0.0 ), shininess );
    return blinnPhong + lambert;
}

void main()
{
    lightPos = (rotate(time * 10) * vec4(lightPos, 1.0)).xyz;
    vec4 tempVertex = modelViewMatrix * position;
    vec3 vrtx = tempVertex.xyz / tempVertex.w;
    vec4 tempNormal = normalMatrix * vec4(normal,0.0);
    vec3 nrml =  normalize(tempNormal.xyz);
    vec3 eyeDir = normalize(eyePos - vrtx); // V
    vec3 lightDir = normalize(lightPos - vrtx); //L
    vec3 halfVector = normalize(lightDir + eyeDir); //H

    vec3 color = computeLigth(nrml, lightDir, diffuseColor, lightColor, halfVector, specularColor, shininess);

    vec3 redLightDir = normalize(redLightPos - vrtx);
    vec3 redLightHalfVec = normalize(redLightDir + eyeDir);

    vec3 redLightColor = computeLigth(nrml, redLightDir, diffuseColor, redLightColor, halfVector, specularColor, shininess);



//   FragColor = vec4(lambert + blinnPhong + ambientColor  , 1.0);
//FragColor =     vec4(lambert , 1.0);
vec4 text = texture(textureSampler, textureCoords.xy);
//    alpha blending
    FragColor = text * text.a + vec4(0.0, 0.0, 0.0, 1.0) * (1 - text.a) + vec4(color + redLightColor + ambientColor, 1.0);
}