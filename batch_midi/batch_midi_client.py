from dataclasses import dataclass
from datetime import datetime

import mido  # type: ignore
import superdirtpy as sd

from .util import gen_filename, second2tick


@dataclass
class MidiEvent:
    typ: str
    note: int
    velo: int
    tick: int


class BatchMidiClient(sd.SuperDirtClient):
    def __init__(self) -> None:
        self._event_buffer: list[tuple[dict, datetime]] = []

    def send(self, event: dict, timestamp: datetime, dryrun: bool = False) -> None:
        self._event_buffer.append((event, timestamp))

    def write(self, out_dir: str, prefix: str = "") -> None:
        outfile = mido.MidiFile()
        track = mido.MidiTrack()
        track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(120)))
        outfile.tracks.append(track)

        midi_events: list[MidiEvent] = []
        for event, timestamp in self._event_buffer:
            octave = event["octave"] if "octave" in event else 5
            note = event["n"] + 12 * octave
            velo = round(127 * event["amp"])
            ts = timestamp.timestamp()
            sustain = event["sustain"] if "sustain" in event else event["delta"]

            midi_events.append(MidiEvent("note_on", note, velo, second2tick(ts)))
            midi_events.append(MidiEvent("note_off", note, velo, second2tick(ts + sustain)))

        on_notes: set = set()
        now = -1
        for e in sorted(midi_events, key=lambda e: e.tick):
            if now < 0:
                now = e.tick

            if e.typ == "note_on":
                if e.note in on_notes:
                    track.append(mido.Message(type="note_off", note=e.note, velocity=0, time=e.tick - now))
                    track.append(mido.Message(type="note_on", note=e.note, velocity=e.velo, time=0))
                else:
                    track.append(mido.Message(type="note_on", note=e.note, velocity=e.velo, time=e.tick - now))
                    on_notes.add(e.note)
            elif e.typ == "note_off":
                if e.note in on_notes:
                    track.append(mido.Message(type="note_off", note=e.note, velocity=e.velo, time=e.tick - now))
                    on_notes.remove(e.note)
                else:
                    pass

            now = e.tick

        outfile.save(gen_filename(out_dir, prefix))
