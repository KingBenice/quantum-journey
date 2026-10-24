# Project 2: Bell state (entanglement)
# Idea: compare two independent random qubits with two entangled qubits.
# Independent qubits give all four answers (00, 01, 10, 11). Entangled qubits only ever agree (00 or 11).

from pathlib import Path                     # file paths that work on any operating system

import matplotlib                            # plotting library
matplotlib.use("Agg")                        # save plots to files instead of opening windows
import matplotlib.pyplot as plt              # used to build a side-by-side figure

from qiskit import QuantumCircuit, transpile # circuit builder and circuit translator
from qiskit.visualization import plot_histogram  # bar chart helper
from qiskit_aer import AerSimulator          # local quantum simulator

HERE = Path(__file__).parent                 # this script's folder
sim = AerSimulator()                         # the simulator we run everything on
SHOTS = 1024                                 # how many times we repeat each experiment


def independent_pair():
    qc = QuantumCircuit(2, 2)                # 2 qubits, 2 classical bits
    qc.h(0)                                  # qubit 0: random 0/1
    qc.h(1)                                  # qubit 1: random 0/1, with no link to qubit 0
    qc.measure([0, 1], [0, 1])               # measure both
    return qc


def bell_pair():
    qc = QuantumCircuit(2, 2)                # 2 qubits, 2 classical bits
    qc.h(0)                                  # put qubit 0 in superposition
    qc.cx(0, 1)                              # CNOT: flip qubit 1 only if qubit 0 is 1. This links (entangles) them
    qc.measure([0, 1], [0, 1])               # measure both; they will always match
    return qc


def run(qc):
    return sim.run(transpile(qc, sim), shots=SHOTS).result().get_counts()  # run and count answers


if __name__ == "__main__":
    bell = bell_pair()                                    # build the entangled circuit
    print(bell.draw("text"))                              # print it in the terminal
    bell.draw("mpl").savefig(HERE / "circuit.png", dpi=150, bbox_inches="tight", facecolor="white")  # save the circuit picture

    indep_counts = run(independent_pair())                # run the 'two separate coins' experiment
    bell_counts = run(bell)                               # run the entangled experiment

    agree = bell_counts.get("00", 0) + bell_counts.get("11", 0)  # how often the entangled qubits matched
    print(f"\nIndependent qubits: {dict(sorted(indep_counts.items()))}")
    print(f"Entangled (Bell) qubits: {dict(sorted(bell_counts.items()))}")
    print(f"Entangled qubits agreed in {agree}/{SHOTS} shots ({100 * agree / SHOTS:.1f}%)")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))     # two charts side by side
    for key in ["00", "01", "10", "11"]:                  # make sure every outcome appears, even with 0 counts
        indep_counts.setdefault(key, 0)
        bell_counts.setdefault(key, 0)
    plot_histogram(indep_counts, ax=axes[0], color="#868E96",
                   title="Two independent qubits")        # left: no entanglement
    axes[0].set_title("Two independent qubits: all 4 answers")  # label each chart clearly
    plot_histogram(bell_counts, ax=axes[1], color="#7048E8",
                   title="Two entangled qubits (Bell state)")  # right: entanglement
    axes[1].set_title("Two entangled qubits: only 00 or 11")
    fig.tight_layout()                                    # tidy the spacing
    fig.savefig(HERE / "histogram.png", dpi=150, bbox_inches="tight", facecolor="white")  # save the comparison chart
    print(f"\nSaved: circuit.png and histogram.png in {HERE.name}/")
