#!/usr/bin/env python3

"""
Usage:
   run_tests.py <command> <argument>...

Run a command line program with input from `sample/in*`, and compare the output
to the corresponding `sample/out*`.

The arguments to this script should be whatever you need to run your solution,
for example:

run_test.py python3 ubo.py

run_test.py ./ubo.py

"""


import difflib
import glob
import subprocess
import sys


def run_single(filename, args):
    with open(filename) as inf:
        proc = subprocess.Popen(args=args, stdin=inf, stdout=subprocess.PIPE)
        out, err = proc.communicate()

    if err:
        print(f"Test on {filename} exited with status {err}", file=sys.stderr)
        return []

    out_lines = out.decode("utf-8").strip().split("\n")
    out_lines = [l.strip() for l in out_lines if l.strip()]

    return out_lines


def main(args):

    tests = list(sorted(glob.glob("sample/in_*")))
    outputs = [t.replace("in", "out") for t in tests]

    for test, output in zip(tests, outputs):
        actual = run_single(test, args[1:])
        with open(output) as f:
            expected = [l.strip() for l in f.readlines() if l.strip()]

        actual.sort()
        expected.sort()

        if expected == actual:
            print(f"{test} -> {output}: OK")
        else:
            print(f"{test} -> {output}: Mismatch")
            for l in difflib.unified_diff(expected, actual, fromfile=output, tofile="actual output"):
                print(l)


if __name__ == "__main__":
    main(sys.argv)
