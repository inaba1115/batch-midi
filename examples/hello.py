import superdirtpy as sd

import batch_midi as bm

# client = sd.SuperDirtClient()
client = bm.BatchMidiClient()
p = {"s": "", "midichan": 0}
out_dir = "~/Desktop/"


def main():
    tctx = sd.TemporalContext(dryrun=True)
    scale = sd.Scale(sd.PitchClass.C, sd.Scales.major)

    for _ in range(8):
        params = p | {
            "n": scale.bind([0, 1, 2, 3]),
            "amp": 0.5,
            "delta": 0.1,
            "sustain": 0.3,
        }
        sd.Pattern(client=client, params=params).play(tctx)

    bm.write(client, out_dir, "hello")


if __name__ == "__main__":
    main()
