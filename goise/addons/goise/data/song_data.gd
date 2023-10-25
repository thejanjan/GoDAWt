extends Resource
class_name GoiseSongData


@export var song_path: String
@export var window: float
@export var instruments: Array[GoiseInstrument]


func _init(p_song_path: String = "",
			p_window: float = 0.0,
			p_instruments: Array[GoiseInstrument] = []):
	song_path = p_song_path
	window = p_window
	instruments = p_instruments
