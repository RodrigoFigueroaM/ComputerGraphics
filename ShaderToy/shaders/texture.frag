# version 330
uniform  mat4 projectionMatrix;
uniform  mat4 modelViewMatrix;
uniform  mat4 normalMatrix;
uniform  float time;
uniform sampler2D textureSampler;


in vec3 normal;
in vec4 position;
in vec2 textureCoords;

out vec4 FragColor;

vec4 backgroundColor = vec4(0.2, 0.2, 0.2, 1.0);
void main()
{
    vec4 text = texture(textureSampler, textureCoords.xy);
//    alpha blending
    FragColor = text * text.a + backgroundColor * (1-text.a);
}