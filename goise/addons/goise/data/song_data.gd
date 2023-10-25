extends Resource
class_name GoiseSongData


@export var song_path: String
@export var instruments: Array[GoiseInstrument]


func _init(p_song_path: String = "",
			p_instruments: Array[GoiseInstrument] = []):
	song_path = p_song_path
	instruments = p_instruments
