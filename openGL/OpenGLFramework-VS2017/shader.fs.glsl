#version 330
struct Light {
	vec3 direction;
	vec3 position;

	float constant;
	float l_linear;
	float quadratic;

	float exponent;
	float cutoff;
};

in vec2 texCoord;
in vec3 FragPos;
in vec3 vertex_color;
in vec3 vertex_normal;

out vec4 fragColor;

// [TODO] passing texture from main.cpp
// Hint: sampler2D
uniform sampler2D umtex;

uniform mat4 um4v;
uniform vec3 viewPos;
uniform vec3 materialKa;
uniform vec3 materialKd;
uniform vec3 materialKs;
uniform int light_mode;
uniform vec3 light_ambient;
uniform vec3 light_diffuse;
uniform vec3 light_specular;
uniform float Shininess;
uniform Light dirLight;
uniform Light pointLight;
uniform Light spotLight;

vec3 DirLight(Light dir_light, vec3 normal, vec3 fragPos, vec3 viewDir) {
	vec3 dir_tmp = vec3(um4v * vec4(dir_light.position, 1.0f));
	vec3 dir_lightDir = normalize(-dirLight.direction);
	// Ambient shading
	vec3 dir_ambient = light_ambient * materialKa;
	// Diffuse shading
	float dir_diff = max(dot(normal, dir_lightDir), 0.0);
	vec3 dir_diffuse = dir_diff * materialKd;
	// Specular shading
	vec3 dir_half_vec = normalize(dir_lightDir + viewDir);
	float dir_spec = pow(max(dot(dir_half_vec, normal), 0.0), Shininess);
	vec3 dir_specular = dir_spec * materialKs;
	return dir_ambient + (dir_diffuse + dir_specular)*light_specular*light_diffuse;
}
vec3 PointLight(Light point_light, vec3 normal, vec3 fragPos, vec3 viewDir) {
	vec3 point_tmp = vec3(um4v * vec4(point_light.position, 1.0f));
	vec3 point_lightDir = normalize(point_tmp - fragPos);
	// Ambient shading
	vec3 point_ambient = light_ambient * materialKa;
	// Diffuse shading
	float point_diff = max(dot(normal, point_lightDir), 0.0);
	vec3 point_diffuse = point_diff * materialKd;
	// Specular shading
	vec3 point_half_vec = normalize(viewDir + point_lightDir);
	float point_spec = pow(max(dot(point_half_vec, normal), 0.0), Shininess);
	vec3 point_specular = point_spec * materialKs;
	// Attenuation
	float point_distance = length(point_tmp - fragPos);
	float point_attenuation = min(1.0f / (point_light.constant + point_light.l_linear * point_distance + point_light.quadratic * (point_distance * point_distance)), 1);
	return point_ambient + (point_diffuse + point_specular)*light_specular*light_diffuse*point_attenuation;
}
vec3 SpotLight(Light spot_light, vec3 normal, vec3 fragPos, vec3 viewDir) {
	vec3 spot_tmp = vec3(um4v * vec4(spot_light.position, 1.0f));
	vec3 spot_lightDir = normalize(spot_tmp - fragPos);
	// Spotlight effect
	float costheta = max(dot(normalize(vec3(um4v*vec4(spot_light.direction, 1.0f))), spot_lightDir), 0.0f);
	float SL_effect;
	if (costheta >= cos(spot_light.cutoff)) {
		float vd = dot(spot_lightDir, normalize(spot_light.direction));
		SL_effect = pow(max(vd, 0.0f), spot_light.exponent);
	}
	else {
		SL_effect = 2;
	}
	// Ambient shading
	vec3 ambient = light_ambient * materialKa;
	// Diffuse shading
	float diff = max(dot(normal, spot_lightDir), 0.0);
	vec3 diffuse = diff * materialKd;
	// Specular shading
	vec3 half_vec = normalize(viewDir + spot_lightDir);
	float spec = pow(max(dot(half_vec, normal), 0.0), Shininess);
	vec3 specular = spec * materialKs;
	// Attenuation
	float distance = length(spot_tmp - fragPos);
	float attenuation = min(1.0f / (spot_light.constant + spot_light.l_linear * distance + spot_light.quadratic * (distance * distance)), 1);
	return ambient + (diffuse + specular)*light_specular*light_diffuse*attenuation*SL_effect;
}

void main() {
	fragColor = vec4(texCoord.xy, 0, 1);
	vec3 nor = normalize(vertex_normal);
	vec3 view_pos = vec3(um4v * vec4(viewPos, 1.0f));
	vec3 viewDir = normalize(view_pos - FragPos);
	vec3 result;
	if (light_mode == 0) { //direction light
		result = DirLight(dirLight, nor, FragPos, viewDir);
	}
	else if (light_mode == 1) { //point light
		result = PointLight(pointLight, nor, FragPos, viewDir);
	}
	else if (light_mode == 2) { //spot light
		result = SpotLight(spotLight, nor, FragPos, viewDir);
	}
	// [TODO] sampleing from texture
	// Hint: texture
	fragColor = texture(umtex, texCoord) * vec4(result, 1.0);
}
