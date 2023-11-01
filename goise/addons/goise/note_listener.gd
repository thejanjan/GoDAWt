extends Node
class_name GoiseNoteListener


var inst_name: String
var cue: float


func _init(p_inst_name: String = 'snare', p_cue: float = -1):
	inst_name = p_inst_name
	cue = p_cue

func start_note(note: GoiseNote):
	pass

func hit_note(note: GoiseNote):
	pass
	
func release_note(note: GoiseNote):
	pass

func process_note(note: GoiseNote, t: float, end: float):
	pass
