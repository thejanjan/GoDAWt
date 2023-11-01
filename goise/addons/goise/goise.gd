@tool
extends EditorPlugin

const AUTOLOAD_NAME = "GoiseMusicManager"


func _enter_tree():
	add_custom_type("SongData", "Resource", preload("data/song_data.gd"), preload("data/song_data.png"))
	add_autoload_singleton(AUTOLOAD_NAME, "res://addons/goise/music_manager.tscn")


func _exit_tree():
	remove_custom_type("SongData")
	remove_autoload_singleton(AUTOLOAD_NAME)
