# version 330
uniform  mat4 projectionMatrix;
uniform  mat4 modelViewMatrix;
uniform  mat4 normalMatrix;
uniform float time;
uniform sampler2D textureSampler;


in vec3 normal;
in vec4 position;
in vec2 textureCoords;

out vec4 FragColor;
void main()
{
    vec4 textureColors = texture(textureSampler, textureCoords.xy);
//   SIMPLE GRAY TEXTURE
//    float gray = (textureColors.r + textureColors.g + textureColors.b)/3;

//  luminance
//    float gray = textureColors.r * 0.3 + textureColors.g * 0.59 + textureColors.b * 0.11;

//   ITU-R Luma
    float gray = textureColors.r * 0.2126 + textureColors.g * 0.7152 + textureColors.b * 0.0722;

//   Desaturation
//      float gray = ( max(textureColors.r, max(textureColors.g, textureColors.b)) + min(textureColors.r, min(textureColors.g, textureColors.b))) / 2;

//  Max Decomposition
//      float gray =  max(textureColors.r, max(textureColors.g, textureColors.b));

//  Min Decomposition
//      float gray =  min(textureColors.r, min(textureColors.g, textureColors.b));

//  Single color channel
//      float gray = textureColors.r;
//      float gray = textureColors.g;
//      float gray = textureColors.b;

    FragColor = vec4(gray, gray, gray, 1.0);

}