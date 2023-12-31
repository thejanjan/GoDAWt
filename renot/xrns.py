from collections import OrderedDict
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element


class XrnsFile:
    """
    Provides a data interface for an .xrns project file.
    """

    def __init__(self, filepath: str | None = None):
        # Constants.
        self._root = None
        self._filepath = ''

        # Song properties.
        self.global_song_data: GlobalSongData | None = None
        self.instruments: list[Instrument] = []
        self.tracks: list[Track] = []
        self.patterns: list[Pattern] = []
        self.pattern_sequence: PatternSequence | None = None

        # Load files.
        if filepath:
            self.load(filepath)

    def load(self, filepath: str):
        if self._root:
            self.clear()

        self._filepath = filepath
        with ZipFile(filepath) as z:
            self._root = ET.fromstring(z.read('Song.xml'))

        tag_to_func = {
            'GlobalSongData':  self._process_global_song_data,
            'Instruments':     self._process_instruments,
            'Tracks':          self._process_tracks,
            'PatternPool':     self._process_pattern_pool,
            'PatternSequence': self._process_pattern_sequence,
        }

        for child in self._root:
            func = tag_to_func.get(child.tag)
            if func:
                func(child)

    def clear(self):
        self._root = None
        self._filepath = ''
        self.global_song_data = None
        self.instruments = []
        self.tracks = []
        self.patterns = []
        self.pattern_sequence = None

    def __repr__(self):
        return f'XrnsFile({self._filepath})'

    """
    Processing
    """

    def _process_global_song_data(self, element: Element):
        self.global_song_data = GlobalSongData(element)

    def _process_instruments(self, element: Element):
        self.instruments = [Instrument(e) for e in element]

    def _process_tracks(self, element: Element):
        self.tracks = [Track(e) for e in element]

    def _process_pattern_pool(self, element: Element):
        self.patterns = [Pattern(e) for e in element.find('Patterns')]

    def _process_pattern_sequence(self, element: Element):
        self.pattern_sequence = PatternSequence(element)


class GlobalSongData:

    def __init__(self, element: Element):
        self.bpm: int = int(element.find('BeatsPerMin').text)
        self.lpb: int = int(element.find('LinesPerBeat').text)
        self.tpl: int = int(element.find('TicksPerLine').text)


class Instrument:

    def __init__(self, element: Element):
        self.name = ''
        for thing in element:
            if thing.tag == 'Name':
                self.name = thing.text
                break
        self.transpose: int = int(element.find('GlobalProperties').find('Transpose').text)


class Track:

    def __init__(self, element: Element):
        self.name: str = element.find('Name').text
        self.type: str = element.tag
        self.track_delay: float = float(element.find('TrackDelay').text)


class Pattern:

    class Effect:

        def __init__(self, number: str, value: int):
            self.number: str = number
            self.value: int = value

        @classmethod
        def from_element(cls, element: Element):
            number_element = element.find('number')
            value_element = element.find('value')
            number = number_element.text if number_element else '00'
            value = int(value_element.text, 16) if value_element else 0
            return cls(number, value)

    class Note:

        def __init__(self, element: Element):
            note_element = element.find('Note')
            inst_element = element.find('Instrument')
            vol_element  = element.find('Volume')
            pan_element  = element.find('Panning')
            del_element  = element.find('Delay')
            fxn_element  = element.find('EffectNumber')
            fxv_element  = element.find('EffectValue')

            if note_element is not None:
                self.note: str = note_element.text
            else:
                self.note: str = 'C-5'
            self.note = self.note.replace('-', '')

            self.instrument: int = int(inst_element.text, 16) if inst_element is not None else -1

            try:
                self.volume: int = int(vol_element.text, 16) if vol_element is not None else 127
            except ValueError:
                self.volume = 128

            try:
                self.panning: int = int(pan_element.text, 16) if pan_element is not None else 64
            except ValueError:
                self.panning = 64

            try:
                self.delay: int = int(del_element.text, 16) if del_element is not None else 0
            except ValueError:
                self.delay = 0

            if fxn_element:
                self.effect: Pattern.Effect | None = Pattern.Effect(
                    number=fxn_element.text,
                    value=int(fxv_element.text, 16) if fxv_element else 0
                )
            else:
                self.effect: Pattern.Effect | None = None

    class Line:

        def __init__(self, element: Element):
            notes_element = element.find('NoteColumns')
            effects_element = element.find('EffectColumns')

            self.notes: list[Pattern.Note] = [
                Pattern.Note(e)
                for e in notes_element
            ] if notes_element else []
            self.effects: list[Pattern.Effect] = [
                Pattern.Effect.from_element(e)
                for e in effects_element
            ] if effects_element else []

    class PatternTrack:

        def __init__(self, element: Element):
            self.lines: dict[int, Pattern.Line] = OrderedDict()
            if lines := element.find('Lines'):
                for child in lines:
                    index = int(child.attrib.get('index', 0))
                    self.lines[index] = Pattern.Line(child)

    def __init__(self, element: Element):
        self.lines: int = int(element.find('NumberOfLines').text)
        self.tracks: list[Pattern.PatternTrack] = [
            Pattern.PatternTrack(e) for e in element.find('Tracks')
        ]


class PatternSequence:

    def __init__(self, element: Element):
        self.order: list = [
            int(e.find('Pattern').text)
            for e in element.find('SequenceEntries')
        ]


if __name__ == '__main__':
    xrns = XrnsFile('xrns_examples/pitcher.xrns')
    print(xrns)
