extends Resource
class_name GoiseSongData


@export var song_path: String
@export var bpm_map: Dictionary
@export var tracks: Array[GoiseTrack]


func _init(p_song_path: String = "",
			p_bpm_map: Dictionary = {},
			p_tracks: Array[GoiseTrack] = []):
	song_path = p_song_path
	bpm_map = p_bpm_map
	tracks = p_tracks
