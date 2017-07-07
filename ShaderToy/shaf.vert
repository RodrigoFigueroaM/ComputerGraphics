uniform highp mat4 projectionMatrix;
uniform highp mat4 modelViewMatrix;
uniform highp mat4 normalMatrix; 

attribute highp vec4 vertexAtr; //.posAttr
attribute vec3 normalAttr; // .normals

varying vec3 normal;
varying vec4 vertex;


attribute lowp vec4 colAttr;
varying lowp vec4 col;

void main() 
{
    gl_Position =  projectionMatrix * modelViewMatrix * vertexAtr;
    normal =  normalAttr;
    vertex = vertexAtr;
}