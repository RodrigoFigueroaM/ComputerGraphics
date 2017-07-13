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
    vec4 text = texture(textureSampler, textureCoords);
//  step 1: Internal relief where p5 is the current pixel
//    |__p1__|__p2__|__p3__|
//    |__p4__|__p5__|__p6__|
//    |__p7__|__p8__|__p9__|
    vec2 pixel = textureCoords.xy;
    vec4 p1 = texture(textureSampler, vec2(pixel.x - 1.0, pixel.y + 1.0));
    vec4 p2 = texture(textureSampler, vec2(pixel.x, pixel.y + 1.0));
    vec4 p3 = texture(textureSampler, vec2(pixel.x + 1.0, pixel.y + 1.0));
    vec4 p4 = texture(textureSampler, vec2(pixel.x - 1.0, pixel.y));
    vec4 p5 = texture(textureSampler, vec2(pixel.x, pixel.y));
    vec4 p6 = texture(textureSampler, vec2(pixel.x + 1.0, pixel.y));
    vec4 p7 = texture(textureSampler, vec2(pixel.x - 1.0, pixel.y - 1.0));
    vec4 p8 = texture(textureSampler, vec2(pixel.x, pixel.y - 1.0));
    vec4 p9 = texture(textureSampler, vec2(pixel.x + 1.0, pixel.y - 1.0));

    vec4 maximum = max(max( max( max(max( max( max( max(p1, p2),p3), p4),p5), p6), p7), p8), p9);
    vec4 minimum = min(min( min( min(min( min( min( min(p1, p2),p3), p4),p5), p6), p7), p8), p9);

//  Step 2: Classification
    FragColor = maximum - minimum ;
//        FragColor =  text + text + text + text;
}