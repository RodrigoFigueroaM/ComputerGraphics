# version 330
const vec3  SurfaceColor =  vec3 (0.75, 0.75, 0.75);
const vec3  WarmColor =  vec3 (0.6, 0.6, 0.0);
const vec3  CoolColor =  vec3 (0.0, 0.0, 0.6);
const float DiffuseWarm =  0.45;
const float DiffuseCool = 0.45;

in float NdotL;
in vec3  ReflectVec;
in vec3  ViewVec;

out vec4 FragColor;

void main (void)
{
    vec3 kcool    = min(CoolColor + DiffuseCool * SurfaceColor, 1.0);
    vec3 kwarm    = min(WarmColor + DiffuseWarm * SurfaceColor, 1.0);
    vec3 kfinal   = mix(kcool, kwarm, NdotL);

    vec3 nreflect = normalize(ReflectVec);
    vec3 nview    = normalize(ViewVec);

    float spec    = max(dot(nreflect, nview), 0.0);
    spec          = pow(spec, 100.0);

    FragColor = vec4 (min(kfinal + spec, 1.0), 1.0);
}
