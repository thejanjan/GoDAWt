extends Resource
class_name GoiseNote


@export var note: int
@export var beat: float
@export var end: float
@export var effects: Array[GoiseEffect]


func _init(p_note: int = 0,
			p_beat: float = 0.0,
			p_end: float = 0.0,
			p_effects: Array[GoiseEffect] = []):
	note = p_note
	beat = p_beat
	end = p_end
	effects = p_effects
