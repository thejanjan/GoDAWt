"""
This module is the main file for running renot.
"""
import json
import sys
import os
import argparse
import logging
from pathlib import Path

from note import Note
from goise import GoiseSongData, GoiseTrack, GoiseNote
from xrns import XrnsFile, Pattern

__date__ = '2023-10-24'
__updated__ = '2023-10-24'
__author__ = 'micahanichols27@gmail.com'


def main(argv=None):
    def p(text: str, with_name: bool = True):
        if with_name:
            name = os.path.basename(sys.argv[0])
            sys.stderr.write(name + f": {text}\n")
        else:
            name = os.path.basename(sys.argv[0])
            indent = len(name) * " "
            sys.stderr.write(indent + f"  {text}\n")

    # try parsing arguments
    try:
        parser = argparse.ArgumentParser(
            epilog='Convert Renoise project files into a Goise resource (a Godot plugin)',
            description='MIT License 2023 - Micah Nichols'
        )
        parser.add_argument('-c', '--config', dest='config', default='config.json', type=str, help='path to a config json file')

        args = parser.parse_args(argv or sys.argv[1:])

    except Exception as e:
        p(repr(e))
        p("for help use --help", with_name=False)
        return 2

    # try to load json
    try:
        with open(args.config) as f:
            config: dict = json.load(f)
    except Exception as e:
        p(repr(e))
        p("config load error", with_name=False)
        return 2

    # iterate over each song
    for song_key, data in config['songs'].items():
        try:
            # load our project file
            xrns_filepath = config['global']['xrns_in'] + data['filename'] + '.xrns'
            p(f'{song_key} - loading {xrns_filepath}')
            xrns = XrnsFile(xrns_filepath)

            # useful constants
            pattern_order: list[int] = xrns.pattern_sequence.order

            # determine the bpm map
            bpm_map = {0: xrns.global_song_data.bpm}

            # start creating our output file
            song_data = GoiseSongData(
                song_path=config['global']['music_path'] + data['filename'] + config['global']['song_fileformat'],
                bpm_map=bpm_map,
            )

            # iterate over each instrument name
            for inst_name, inst_data in data['insts'].items():
                # find the index of this instrument
                for i, xrns_instrument in enumerate(xrns.instruments):
                    if xrns_instrument.name == inst_name:
                        instrument_index = i
                        break
                else:
                    p(f'{song_key} - could not find {inst_name} in {data["name"]}')
                    continue

                # get instrument globals
                transpose = xrns_instrument.transpose

                # create our instrument type
                p(f'{song_key} - building instrument {inst_name}')
                instrument = GoiseTrack(name=inst_data.get('name', inst_name))
                song_data.add_track(instrument)

                # iterate over each track at a time, looking for this instrument data
                current_note: GoiseNote | None = None
                for track_index in range(len(xrns.tracks)):
                    global_line_index = 0

                    for pattern_index in pattern_order:
                        # ok cool! we are looking at this pattern now
                        pattern: Pattern = xrns.patterns[pattern_index]
                        track: Pattern.PatternTrack = pattern.tracks[track_index]

                        for local_line_index, line in track.lines.items():
                            line_index = global_line_index + local_line_index

                            for note in line.notes:
                                delay_time = note.delay / 256
                                if note.note == 'OFF' and current_note:
                                    # we cancel the current note
                                    current_note.end = line_index + delay_time
                                    current_note = None
                                elif note.instrument == instrument_index:
                                    # we start using this instrument
                                    noteobj = Note.from_string(note.note)
                                    noteobj.transpose(transpose)
                                    current_note = GoiseNote(
                                        note=noteobj,
                                        beat=line_index + delay_time,
                                        end=0.0,
                                    )
                                    instrument.add_note(current_note)

                            if current_note:
                                for effect in line.effects:
                                    pass

                        # increase time by lines iterated over
                        global_line_index += pattern.lines

            # write to output
            with open(config['global']['data_out'] + song_key + '.tres', 'w') as f:
                f.write(song_data.get_tres_string())
        except Exception as e:
            name = os.path.basename(sys.argv[0])
            sys.stderr.write(name + ": " + repr(e) + "\n")
            continue

    # completion
    return 0


if __name__ == "__main__":
    sys.exit(main())
