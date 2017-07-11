# version 330
uniform  mat4 projectionMatrix;
uniform  mat4 modelViewMatrix;
uniform  mat4 normalMatrix;
uniform sampler2D textureSampler;

in vec3 normal;
in vec4 position;
in vec2 textureCoords;

out vec4 FragColor;
void main()
{
    vec4 text = texture(textureSampler, textureCoords);
    float lum = text.r + text.g + text.b /3;
//    FragColor = vec4(text.r, text.g , text.b/3, 1.0);
    FragColor = vec4(normal, 1.0);
}