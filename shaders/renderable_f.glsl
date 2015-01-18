#version 130

uniform sampler2D charset;
uniform sampler2D palette;
uniform sampler2D grain;
// width of the generated palette texture, ie palette.MAX_COLORS
uniform float palTextureWidth;
uniform float grainStrength;
uniform float bgColorAlpha;

in vec2 texCoords;
in float theFgColorIndex;
in float theBgColorIndex;

const float grainSize = 0.0025;

out vec4 outColor;

void main()
{
	outColor = texture2D(charset, texCoords);
	// look up fg/bg colors from palette texture
	vec2 colorUV = vec2(0.0, 0.0);
	// offset U coord slightly so we're not sampling from pixel boundary
	colorUV.x = (theFgColorIndex + 0.01) / palTextureWidth;
	vec4 fgColor = texture2D(palette, colorUV);
	// multiple charset pixel value by FG color
	// tinting >1 color charsets isn't officially supported but hey
	outColor.rgb *= fgColor.rgb;
	// any totally transparent pixels get the BG color
	colorUV.x = (theBgColorIndex + 0.01) / palTextureWidth;
	vec4 bgColor = texture(palette, colorUV);
	bgColor.a *= bgColorAlpha;
	// thanks Mark Wonnacott for tip on how to do this w/o a branch
	outColor = mix(bgColor, fgColor, outColor.a);
	// apply "grain" for eg UI elements
	vec4 grainColor = texture2D(grain, gl_FragCoord.xy * grainSize);
	outColor.rgb += (0.5 - grainColor.rgb) * grainStrength;
}
