# Project 1: Quantum coin flip and random number generator
# Idea: put one qubit in superposition (half 0, half 1), measure it, and get a fair random bit.

import sys                                   # lets us read numbers typed after the script name
from pathlib import Path                     # helps build file paths that work on Windows, Mac and Linux

import matplotlib                            # the plotting library
matplotlib.use("Agg")                        # draw plots straight to PNG files (no pop-up window needed)
import matplotlib.pyplot as plt              # the part of matplotlib we use to save figures

from qiskit import QuantumCircuit, transpile # QuantumCircuit builds circuits; transpile prepares them for a simulator or chip
from qiskit.visualization import plot_histogram  # turns measurement counts into a bar chart
from qiskit_aer import AerSimulator          # a quantum computer simulator that runs on your laptop

HERE = Path(__file__).parent                 # the folder this script lives in, so images are saved next to it
sim = AerSimulator()                         # create one simulator we can reuse for every run


def coin_flip_circuit():
    qc = QuantumCircuit(1, 1)                # 1 qubit (the coin) and 1 classical bit (where we write the result)
    qc.h(0)                                  # Hadamard gate: turns |0> into an equal mix of |0> and |1>
    qc.measure(0, 0)                         # measuring forces the qubit to pick 0 or 1, each with 50% chance
    return qc                                # hand the finished circuit back


def run(qc, shots):
    compiled = transpile(qc, sim)            # translate the circuit into gates the simulator understands
    job = sim.run(compiled, shots=shots)     # run it 'shots' times
    return job.result().get_counts()         # count how many times each answer appeared, e.g. {'0': 498, '1': 502}


def random_number(n_bits):
    qc = QuantumCircuit(n_bits, n_bits)      # one qubit per bit of the number we want
    qc.h(range(n_bits))                      # put every qubit into superposition at once
    qc.measure(range(n_bits), range(n_bits)) # measure all of them
    bits = list(run(qc, shots=1).keys())[0]  # run once and read the single bitstring we got, e.g. '10110010'
    return int(bits, 2), bits                # turn the bitstring into a normal number and return both


def dice_roll():
    while True:                              # keep trying until we land on a valid dice face
        value, _ = random_number(3)          # 3 random bits give a number from 0 to 7
        if value < 6:                        # only 0-5 are fair dice faces (6 and 7 are thrown away)
            return value + 1                 # shift 0-5 up to 1-6


if __name__ == "__main__":
    flips = int(sys.argv[1]) if len(sys.argv) > 1 else 1000   # number of coin flips (default 1000)

    qc = coin_flip_circuit()                                   # build the coin-flip circuit
    print(qc.draw("text"))                                     # show the circuit as text in the terminal
    qc.draw("mpl").savefig(HERE / "circuit.png", dpi=150, bbox_inches="tight", facecolor="white")  # save a picture of the circuit

    counts = run(qc, shots=flips)                              # flip the quantum coin many times
    heads, tails = counts.get("0", 0), counts.get("1", 0)      # call 0 'heads' and 1 'tails'
    print(f"\n{flips} quantum coin flips -> heads (0): {heads}, tails (1): {tails}")
    print(f"Heads ratio: {heads / flips:.3f}  (a fair coin should be close to 0.500)")

    fig = plot_histogram(counts, title=f"Quantum coin: {flips} flips", color="#4C6EF5")  # bar chart of the counts
    fig.savefig(HERE / "histogram.png", dpi=150, bbox_inches="tight", facecolor="white")                     # save it as a PNG

    number, bits = random_number(8)                            # an 8-bit random number (0 to 255)
    print(f"\nRandom 8-bit number: {number}  (bits: {bits})")
    print(f"Quantum dice roll: {dice_roll()}")
    print(f"\nSaved: circuit.png and histogram.png in {HERE.name}/")
