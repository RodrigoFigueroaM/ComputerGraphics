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

const float T = 0.6;
vec4 backgroundColor = vec4(0.2, 0.2, 0.2, 1.0);
vec4 black = vec4(0.0, 0.0, 0.0, 1.0);
vec4 white = vec4(1.0, 1.0, 1.0, 1.0);
void main()
{
//    float T = sin(time* 2);
    vec4 text = texture(textureSampler, textureCoords);
    float gray = text.r * 0.3 + text.g * 0.59 + text.b * 0.11;
    vec4 grayVector = vec4(gray, gray, gray, 1.0);
    if( gray < T)
        FragColor = black;
    else
        FragColor = white;
}