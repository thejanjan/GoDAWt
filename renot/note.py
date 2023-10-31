class Note:

    letters = [
        'C', 'C#', 'D', 'D#', 'E', 'F',
        'F#', 'G', 'G#', 'A', 'A#', 'B',
    ]

    def __init__(self, step: int):
        self.step = step

    def transpose(self, amount: int):
        self.step += amount

    @classmethod
    def from_string(cls, note: str) -> 'Note':
        note = note.replace('-', '')
        octave = int(note[-1])
        note = note[:-1]
        letter_index = cls.letters.index(note)
        octave_step = octave * len(cls.letters)
        return cls(step=letter_index + octave_step)

    def to_string(self) -> str:
        letter_index = self.step % len(self.letters)
        letter = self.letters[letter_index]
        octave = self.step // len(self.letters)
        return letter + str(octave)
