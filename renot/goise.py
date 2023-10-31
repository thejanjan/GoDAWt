"""
This module contains a Python version of the Goise resources.
This allows writing of Goise resources as well (but not reads).
"""
from enum import IntEnum, auto
from random import Random

from note import Note

used_ids: set[str] = set()


def get_id_string(length: int = 5, seed: int | None = None) -> str:
    rng = Random(x=seed)
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    while True:
        new_id = ''.join(rng.choice(chars) for _ in range(length))
        if seed:
            break
        if new_id not in used_ids:
            break
    used_ids.add(new_id)
    return new_id


class GoiseSongData:

    script_id = '1_nirk5'

    def __init__(self, song_path: str = 'res://music/song.wav', bpm_map: dict[float, float] = None):
        self.song_path: str = song_path
        self.bpm_map: dict[float, float] = bpm_map or {}
        self.tracks: list[GoiseTrack] = []

    """
    Exports
    """

    def get_tres_string(self) -> str:
        """
        Serializes this entire class into a Godot-friendly format.
        """
        # I don't think it's harmful to setup output like this??
        output = \
        f"""[ext_resource type="Script" path="res://addons/goise/data/track.gd" id="{GoiseTrack.script_id}"]\n""" \
        f"""[ext_resource type="Script" path="res://addons/goise/data/note.gd" id="{GoiseNote.script_id}"]\n""" \
        f"""[ext_resource type="Script" path="res://addons/goise/data/song_data.gd" id="{GoiseSongData.script_id}"]\n""" \
        f"""[ext_resource type="Script" path="res://addons/goise/data/effect.gd" id="{GoiseEffect.script_id}"]\n\n"""
        load_steps = 5  # external resources + ourselves

        # Establish subresources depth-first.
        for track in self.tracks:
            new_steps, output_text = track.get_tres_string()
            load_steps += new_steps
            output += output_text

        # Create last resource reference.
        bpm_str = ',\n'.join(f'{key}: {val}' for key, val in self.bpm_map.items())
        last_ref = \
        f"""[resource]\n""" \
        f"""script = ExtResource("{GoiseSongData.script_id}")\n""" \
        f"""song_path = "{self.song_path}"\n""" \
        """bpm_map = {\n""" \
        f"""{bpm_str}\n""" \
        """}\n""" \
        f"""tracks = Array[ExtResource("{GoiseTrack.script_id}")]([{', '.join([
            f'SubResource("{track.get_unique_id()}")'
            for track in self.tracks
        ])}])\n"""
        output += last_ref

        # Create header.
        uid = get_id_string(length=13, seed=hash(self.song_path))
        header = f'[gd_resource type="Resource" script_class="GoiseSongData" load_steps={load_steps} format=3 uid="uid://{uid}"]\n\n'
        output = header + output

        # We are done.
        return output

    """
    Interface
    """

    def add_track(self, instrument: 'GoiseTrack'):
        self.tracks.append(instrument)


class GoiseTrack:

    script_id = '1_5f3fy'

    def __init__(self, name: str):
        self.name: str = name
        self.notes: list[GoiseNote] = []

        self._id = get_id_string()

    """
    Export
    """

    def get_tres_string(self) -> tuple[int, str]:
        # Create subresource references.
        output = ""
        load_steps = 1

        # Establish subresources depth-first.
        for note in self.notes:
            new_steps, output_text = note.get_tres_string()
            load_steps += new_steps
            output += output_text

        # Sort notes.
        self.notes = sorted(self.notes, key=lambda n: n.beat)

        # Create our own resource reference.
        output += \
        f"""[sub_resource type="Resource" id="{self.get_unique_id()}"]\n""" \
        f"""script = ExtResource("{self.script_id}")\n""" \
        f"""name = "{self.name}"\n""" \
        f"""notes = Array[ExtResource("{GoiseNote.script_id}")]([{', '.join([
            f'SubResource("{note.get_unique_id()}")'
            for note in self.notes
        ])}])\n\n"""

        # Return.
        return load_steps, output

    def get_unique_id(self) -> str:
        return f'Resource_{self._id}'

    """
    Interface
    """

    def add_note(self, note: 'GoiseNote'):
        self.notes.append(note)


class GoiseNote:

    script_id = '1_hp8nu'

    def __init__(self,
                 note: Note,
                 beat: float,
                 end: float):
        self.note: Note = note
        self.beat: float = beat
        self.end: float = end
        self.effects: list[GoiseEffect] = []

        self._id = get_id_string()

    """
    Export
    """

    def get_tres_string(self) -> tuple[int, str]:
        # Create subresource references.
        output = ""
        load_steps = 1

        # Establish subresources depth-first.
        for fx in self.effects:
            new_steps, output_text = fx.get_tres_string()
            load_steps += new_steps
            output += output_text

        # Create our own resource reference.
        output += \
        f"""[sub_resource type="Resource" id="{self.get_unique_id()}"]\n""" \
        f"""script = ExtResource("{self.script_id}")\n""" \
        f"""note = {self.note.step}\n""" \
        f"""beat = {self.beat}\n""" \
        f"""end = {self.end}\n""" \
        f"""effects = Array[ExtResource("{GoiseEffect.script_id}")]([{', '.join([
            f'SubResource("{fx.get_unique_id()}")'
            for fx in self.effects
        ])}])\n\n"""

        # Return.
        return load_steps, output

    def get_unique_id(self) -> str:
        return f'Resource_{self._id}'

    """
    Interface
    """

    def add_effect(self, effect: 'GoiseEffect'):
        self.effects.append(effect)


class GoiseEffect:

    script_id = '2_rtmqs'

    class Type(IntEnum):
        NONE = auto()
        VOLUME = auto()
        PITCH = auto()
        PAN = auto()

    def __init__(self):
        self.type: GoiseEffect.Type = GoiseEffect.Type.NONE
        self.params: list[float] = []

        self._id = get_id_string()

    """
    Export
    """

    def get_tres_string(self) -> tuple[int, str]:
        # Create subresource references.
        output = ""
        load_steps = 1

        # Create our own resource reference.
        output += \
        f"""[sub_resource type="Resource" id="{self.get_unique_id()}"]\n""" \
        f"""script = ExtResource("{self.script_id}")\n""" \
        f"""type = {int(self.type) - 1}\n""" \
        f"""params = Array[float]([{', '.join([
            str(param) for param in self.params
        ])}])\n\n"""

        # Return.
        return load_steps, output

    def get_unique_id(self) -> str:
        return f'Resource_{self._id}'

    """
    Creators
    """

    @classmethod
    def make_volume(cls, time: float, duration: float, delta: float):
        effect = GoiseEffect()
        effect.type = GoiseEffect.Type.VOLUME
        effect.params = [time, duration, delta]
        return effect

    @classmethod
    def make_pitch(cls, time: float, duration: float, delta: float):
        effect = GoiseEffect()
        effect.type = GoiseEffect.Type.PITCH
        effect.params = [time, duration, delta]
        return effect

    @classmethod
    def make_pan(cls, time: float, duration: float, delta: float):
        effect = GoiseEffect()
        effect.type = GoiseEffect.Type.PAN
        effect.params = [time, duration, delta]
        return effect


if __name__ == '__main__':
    song_data = GoiseSongData()

    rng = Random(x=None)

    for a in range(4):

        inst = GoiseTrack(f'inst_{a}')

        for b in range(120):

            note = GoiseNote(f'note_{b}', b + 0.5, -0.5, 0.0)

            for c in range(3):
                funcs = [
                    GoiseEffect.make_volume,
                    GoiseEffect.make_pan,
                    GoiseEffect.make_pitch,
                ]
                func = funcs[c % len(funcs)]
                fx: GoiseEffect = func(rng.random(), rng.random(), rng.random())
                note.add_effect(fx)

            inst.add_note(note)

        song_data.add_track(inst)

    print(song_data.get_tres_string())
