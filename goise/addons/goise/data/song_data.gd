extends Resource
class_name GoiseSongData


@export var song_path: String
@export var bpm_map: Dictionary
@export var lpb_map: Dictionary
@export var tracks: Array[GoiseTrack]


func _init(p_song_path: String = "",
			p_bpm_map: Dictionary = {},
			p_lbp_map: Dictionary = {},
			p_tracks: Array[GoiseTrack] = []):
	song_path = p_song_path
	bpm_map = p_bpm_map
	lpb_map = p_lbp_map
	tracks = p_tracks


func get_line(t: float) -> float:
	# TODO - handle bpm adjusts
	var bpm = bpm_map[0]
	var bps = bpm / 60.0
	var lpb = lpb_map[0]
	return bps * t * lpb
