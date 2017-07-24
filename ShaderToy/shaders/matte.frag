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

const vec3 lightPos = vec3(0.0, 0.0, 4.0);
const vec3 ligthColor = vec3(1.0, 1.0, 1.0);
const vec3 eyePos = vec3 (0,0,0);

const vec3 diffuseColor = vec3(1.0, 1.0, 1.0); //base color
const float diffueseCoeff = 0.9;
void main()
{
    vec4 tempVertex = modelViewMatrix * position;
    vec3 vrtx = tempVertex.xyz / tempVertex.w;

    vec4 tempNormal = normalMatrix * vec4(normal, 1.0);
    vec3 norml = normalize(tempNormal.xyz);

    vec3 text = texture(textureSampler, textureCoords.xy).rgb;
    vec3 lightDir = normalize(lightPos - vrtx);
    float NdotL = dot(lightDir, norml);
    vec3 eyeDir = normalize(eyePos - vrtx);

    vec3 lambertian = diffueseCoeff * ligthColor * diffuseColor * max(NdotL, 0.0);
    FragColor = vec4( lambertian, 1.0);
}