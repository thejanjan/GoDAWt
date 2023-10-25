extends Resource
class_name GoiseInstrument


@export var name: String
@export var notes: Array[GoiseNote]


func _init(p_name: String = 'Instrument',
			p_notes: Array[GoiseNote] = []):
	name = p_name
	notes = p_notes
