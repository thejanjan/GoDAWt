extends Resource
class_name GoiseEffect


enum Type {
	NONE,
	VOLUME,
	PITCH,
	PAN,
}


@export var type: Type
@export var params: Array[float]


func _init(p_type: Type = Type.NONE,
			p_params: Array[float] = []):
	type = p_type
	params = p_params
