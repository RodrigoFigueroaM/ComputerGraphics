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
//   FragColor = ;
    FragColor = texture(textureSampler, textureCoords);
}