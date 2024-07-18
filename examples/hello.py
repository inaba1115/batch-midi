import superdirtpy as sd

import batch_midi as bm

# client, dryrun = sd.SuperDirtClient(), False
client, dryrun = bm.BatchMidiClient(), True
p = {"s": "mydevice", "midichan": 0}
out_dir = "~/Desktop/"


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

    bm.write(client, out_dir, "hello")


if __name__ == "__main__":
    main()
