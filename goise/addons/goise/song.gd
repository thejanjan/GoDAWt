extends Node
class_name GoiseSong

# Nodes
var audio_stream_player: AudioStreamPlayer = null

# Attributes
var song_data: GoiseSongData = null
var listeners: Dictionary = {}

# State
var last_t: float = 0.0
var note_state: Dictionary = {}

enum NoteState { WAIT, CUED, HIT, RELEASED } 


func _ready():
	audio_stream_player = AudioStreamPlayer.new()
	add_child(audio_stream_player)


func destroy():
	queue_free()


func _process(delta):
	var t: float = audio_stream_player.get_playback_position()
	var line: float = song_data.get_line(t)
	last_t = t
	if last_t > t:
		note_state = {}
	
	for track in song_data.tracks:
		if track.name not in listeners:
			continue
		
		for note_listener in listeners[track.name]:
			if note_listener not in note_state:
				note_state[note_listener] = {}
			
			for note in track.notes:
				if note in note_state[note_listener]:
					if note_state[note_listener][note] == NoteState.RELEASED:
						continue
				else:
					note_state[note_listener][note] = NoteState.WAIT
				
				var zero_beat = note.beat + note_listener.cue
				var one_beat = note.beat
				var end_beat = 1.0
				if note.end != 0.0:
					end_beat = inverse_lerp(zero_beat, one_beat, note.end)
				var beat_delta = inverse_lerp(zero_beat, one_beat, line)
				
				if beat_delta < 0:
					# The note is not ready to be processed.
					continue
				elif beat_delta < 1.0:
					# The note is ready to process.
					if note_state[note_listener][note] == NoteState.WAIT:
						note_state[note_listener][note] = NoteState.CUED
						note_listener.start_note(note)
					if note_state[note_listener][note] == NoteState.CUED:
						note_listener.process_note(note, beat_delta, end_beat)
				elif beat_delta < end_beat:
					# The note has been hit.
					if note_state[note_listener][note] == NoteState.CUED:
						note_state[note_listener][note] = NoteState.HIT
						note_listener.hit_note(note)
					if note_state[note_listener][note] == NoteState.HIT:
						note_listener.process_note(note, beat_delta, end_beat)
				else:
					# The note is ended.
					if note_state[note_listener][note] == NoteState.CUED:
						note_state[note_listener][note] = NoteState.RELEASED
						note_listener.hit_note(note)
						note_listener.process_note(note, end_beat, end_beat)
						note_listener.release_note(note)
					elif note_state[note_listener][note] == NoteState.HIT:
						note_state[note_listener][note] = NoteState.RELEASED
						note_listener.process_note(note, end_beat, end_beat)
						note_listener.release_note(note)


"""
Internal Interface
"""

func start():
	audio_stream_player.stream = load(song_data.song_path)
	audio_stream_player.play()


func set_song_data(song_data: GoiseSongData):
	self.song_data = song_data

"""
External Interface
"""


func attach_listener(listener: GoiseNoteListener):
	var inst_name = listener.inst_name
	if inst_name not in listeners:
		listeners[inst_name] = []
	listeners[inst_name].append(listener)


func detach_listener(listener: GoiseNoteListener):
	var inst_name = listener.inst_name
	if inst_name not in listeners:
		return
	listeners[inst_name].erase(listener)
	if not listeners[inst_name]:
		listeners.erase(inst_name)
