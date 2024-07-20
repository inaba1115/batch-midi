import superdirtpy as sd

import batch_midi as bm

# client = sd.SuperDirtClient()
client = bm.BatchMidiClient()
dryrun = isinstance(client, bm.BatchMidiClient)
p = {"s": "superpiano"}


def main():
    tctx = sd.TemporalContext(dryrun=dryrun)
    scale = sd.Scale(sd.PitchClass.C, sd.Scales.major)

    for _ in range(8):
        params = p | {
            "n": scale.bind([0, 1, 2, 3]),
            "amp": 0.5,
            "delta": 0.1,
            "sustain": 0.3,
        }
        sd.Pattern(client=client, params=params).play(tctx)


if __name__ == "__main__":
    main()
    bm.write(client, "~/Desktop/", "hello")
