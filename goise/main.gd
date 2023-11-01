extends Node

var song_data = preload("res://music/data/steam_factory.tres")

# Called when the node enters the scene tree for the first time.
func _ready():
	var song: GoiseSong = GoiseMusicManager.set_song(song_data)
	var snare_listener = GoiseNoteListener.new("bass")
	song.attach_listener(snare_listener)
	song.start()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
