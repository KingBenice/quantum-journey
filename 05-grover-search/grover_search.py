# Project 5: Grover's search on 3 qubits
# Idea: 3 qubits hold 8 possible items (000 to 111). One is 'marked'. Classically you check items one by one
# (up to 8 tries). Grover's algorithm boosts the marked item's probability so one measurement usually finds it.

import math                                  # for pi, sqrt and floor
import sys                                   # read the marked item from the command line
from pathlib import Path                     # file paths

import matplotlib                            # plotting
matplotlib.use("Agg")                        # save to files
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile # circuit builder + translator
from qiskit.quantum_info import Statevector  # exact probabilities, used for the 'rounds' chart
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

HERE = Path(__file__).parent                 # this script's folder
sim = AerSimulator()                         # the simulator
SHOTS = 1024                                 # repeats


def oracle(qc, marked):
    n = len(marked)                          # number of qubits
    for i, bit in enumerate(reversed(marked)):   # Qiskit's qubit 0 is the rightmost character
        if bit == "0":
            qc.x(i)                          # flip the 0s so the marked item looks like '111'
    qc.h(n - 1)                              # this H + multi-controlled X + H combo...
    qc.mcx(list(range(n - 1)), n - 1)        # ...flips the sign (phase) of '111' only
    qc.h(n - 1)
    for i, bit in enumerate(reversed(marked)):
        if bit == "0":
            qc.x(i)                          # undo the flips: now only the marked item has a minus sign


def diffuser(qc, n):
    qc.h(range(n))                           # the 'diffuser' reflects every amplitude around the average...
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))                           # ...which grows the marked item (negative) and shrinks the rest


def grover_circuit(marked, rounds, measure=True):
    n = len(marked)
    qc = QuantumCircuit(n, n) if measure else QuantumCircuit(n)
    qc.h(range(n))                           # start with all 8 items equally likely
    for _ in range(rounds):                  # each round = oracle (mark) + diffuser (amplify)
        qc.barrier()
        oracle(qc, marked)
        qc.barrier()
        diffuser(qc, n)
    if measure:
        qc.measure(range(n), range(n))       # read the answer
    return qc


if __name__ == "__main__":
    marked = sys.argv[1] if len(sys.argv) > 1 else "101"     # the item we are searching for
    n = len(marked)
    best_rounds = math.floor(math.pi / 4 * math.sqrt(2 ** n))  # the ideal number of rounds: about (pi/4)*sqrt(N)
    print(f"Searching {2 ** n} items for '{marked}' using {best_rounds} Grover rounds")

    qc = grover_circuit(marked, best_rounds)                   # build the circuit
    print(qc.draw("text", fold=-1))
    qc.draw("mpl", fold=-1).savefig(HERE / "circuit.png", dpi=150, bbox_inches="tight", facecolor="white")

    counts = sim.run(transpile(qc, sim), shots=SHOTS).result().get_counts()   # run it
    hit = counts.get(marked, 0)
    print(f"\nFound '{marked}' in {hit}/{SHOTS} shots ({100 * hit / SHOTS:.1f}%). "
          f"Random guessing would give {100 / 2 ** n:.1f}%.")
    fig = plot_histogram(counts, title=f"Grover search for '{marked}' ({best_rounds} rounds)", color="#1971C2")
    fig.savefig(HERE / "histogram.png", dpi=150, bbox_inches="tight", facecolor="white")

    # Bonus chart: what happens with 0 to 6 rounds? Too many rounds 'overshoot' and the chance drops again.
    probs = []
    for r in range(7):
        sv = Statevector(grover_circuit(marked, r, measure=False))  # exact state, no sampling noise
        probs.append(float(sv.probabilities_dict().get(marked, 0.0)))      # chance of measuring the marked item
    print("Chance of the marked item after 0..6 rounds:", [round(p, 3) for p in probs])
    fig2, ax = plt.subplots(figsize=(7, 4))
    ax.plot(range(7), probs, marker="o", color="#1971C2")
    ax.axvline(best_rounds, linestyle="--", color="gray")
    ax.set_xlabel("Grover rounds")
    ax.set_ylabel(f"Probability of '{marked}'")
    ax.set_title("Too many rounds overshoots: the chance rises and falls")
    ax.set_ylim(0, 1.05)
    ax.grid(alpha=0.3)
    fig2.savefig(HERE / "rounds.png", dpi=150, bbox_inches="tight", facecolor="white")
    print(f"\nSaved: circuit.png, histogram.png and rounds.png in {HERE.name}/")
