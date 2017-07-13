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
    vec4 text = texture(textureSampler, textureCoords);
    float red = text.r;
    float green = text.g ;
    float blue = text.b;
    float alpha = text.a;
    float res = red * 0.3f + green * 1 + blue * 0.3;
    vec4 color = vec4(res,res + green,res, alpha );
//    text.rbga;
//  alpha blending
    FragColor = color * color.a + backgroundColor * (1 - color.a);
}