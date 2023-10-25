extends Resource
class_name GoiseNote


@export var note: String
@export var time: float
@export var cue: float
@export var release: float
@export var effects: Array[GoiseEffect]


func _init(p_note: String = 'C3',
			p_time: float = 0.0,
			p_cue: float = -0.67,
			p_release: float = 0.0,
			p_effects: Array[GoiseEffect] = []):
	note = p_note
	time = p_time
	cue = p_cue
	release = p_release
	effects = p_effects
