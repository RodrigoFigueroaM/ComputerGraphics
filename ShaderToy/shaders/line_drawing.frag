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
const vec3 eyePos = vec3 (0,0,0);
vec4 color = vec4(1.0, 1.0, 1.0, 1.0);
void main()
{
    if(dot(eyePos, normal) < 0 )
        color = vec4(0.0, 0.0, 0.0, 1.0);

    vec4 text = texture(textureSampler, textureCoords.xy);
    FragColor = text * text.a + vec4(0.0, 0.0, 0.0, 1.0) * (1 - text.a) + vec4(color);
}