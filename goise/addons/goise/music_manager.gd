extends Node
class_name GoiseMusicService


var active_song: GoiseSong = null


func set_song(song_data: GoiseSongData) -> GoiseSong:
	if active_song:
		active_song.destroy()
	
	active_song = GoiseSong.new()
	add_child(active_song)
	active_song.set_song_data(song_data)
	return active_song
