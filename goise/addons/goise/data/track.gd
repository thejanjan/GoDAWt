extends Resource
class_name GoiseTrack


@export var name: String
@export var notes: Array[GoiseNote]


func _init(p_name: String = 'Track',
			p_notes: Array[GoiseNote] = []):
	name = p_name
	notes = p_notes
