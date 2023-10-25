@tool
extends EditorPlugin


func _enter_tree():
	# Initialization of the plugin goes here.
	add_custom_type("SongData", "Resource", preload("data/song_data.gd"), preload("data/song_data.png"))


func _exit_tree():
	# Clean-up of the plugin goes here.
	remove_custom_type("SongData")
