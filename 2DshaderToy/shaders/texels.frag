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
    vec2 pixel = gl_FragCoord.xy;
    vec4 N = texture(textureSampler, vec2(pixel.x, pixel.y+10.0));
    vec2 S = texture(textureSampler, vec2(pixel.x, pixel.y-1.0)).xy;
    vec2 W = texture(textureSampler, vec2(pixel.x-1.0, pixel.y)).xy;
    vec2 E = texture(textureSampler, vec2(pixel.x+1.0, pixel.y)).xy;
//
    FragColor = text + N;


////    alpha blending
//      FragColor = text * text.a + backgroundColor * (1 - text.a);
}