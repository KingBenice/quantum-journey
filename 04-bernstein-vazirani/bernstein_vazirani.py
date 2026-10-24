# Project 4: Bernstein-Vazirani algorithm (a first quantum speedup)
# Puzzle: a black box hides a secret bitstring s. Ask it about any bitstring x and it answers (s . x) mod 2,
# a single 0 or 1. A classical computer needs one question per bit (n questions).
# A quantum computer finds the whole secret with ONE question, by asking about all x at once.

import sys                                   # read the secret from the command line if given
from pathlib import Path                     # file paths

import matplotlib                            # plotting
matplotlib.use("Agg")                        # save to files, no windows

from qiskit import QuantumCircuit, transpile # circuit builder + translator
from qiskit.visualization import plot_histogram   # bar chart
from qiskit_aer import AerSimulator               # local simulator

HERE = Path(__file__).parent                 # this script's folder
sim = AerSimulator()                         # the simulator
SHOTS = 1024                                 # repeats (one would be enough; more shows it never fails)


def classical_solver(secret):
    n = len(secret)                          # number of bits in the secret
    found, questions = "", 0                 # what we learn, and how many times we ask the box
    for i in range(n):                       # ask about one bit position at a time
        x = ["0"] * n                        # a question with a single 1 in position i...
        x[i] = "1"
        answer = sum(int(a) * int(b) for a, b in zip(secret, x)) % 2  # ...the box answers (s . x) mod 2
        found += str(answer)                 # that answer IS bit i of the secret
        questions += 1                       # count the question
    return found, questions


def oracle(qc, secret):
    n = len(secret)                          # number of input qubits
    for i, bit in enumerate(reversed(secret)):  # Qiskit numbers qubits from the right, so read the secret backwards
        if bit == "1":                       # wherever the secret has a 1...
            qc.cx(i, n)                      # ...link that input qubit to the helper qubit (this computes s . x)


def bv_circuit(secret):
    n = len(secret)                          # input size
    qc = QuantumCircuit(n + 1, n)            # n input qubits + 1 helper qubit; n classical bits for the answer
    qc.x(n)                                  # set the helper qubit to 1...
    qc.h(range(n + 1))                       # ...then Hadamard everything: inputs become 'all x at once', helper becomes |->
    qc.barrier()                             # divider in the drawing
    oracle(qc, secret)                       # ask the black box ONE time (on every x in superposition)
    qc.barrier()
    qc.h(range(n))                           # Hadamard the inputs again: the waves interfere and leave exactly s
    qc.measure(range(n), range(n))           # read the inputs: the result is the secret
    return qc


if __name__ == "__main__":
    secret = sys.argv[1] if len(sys.argv) > 1 else "101101"  # the hidden string (change it to test!)
    assert set(secret) <= {"0", "1"}, "secret must be made of 0s and 1s"

    found_c, q_c = classical_solver(secret)                   # solve the classical way
    print(f"Secret hidden in the box: {secret}")
    print(f"Classical method: found {found_c} using {q_c} questions")

    qc = bv_circuit(secret)                                    # build the quantum circuit
    print(qc.draw("text"))
    qc.draw("mpl").savefig(HERE / "circuit.png", dpi=150, bbox_inches="tight", facecolor="white")  # save the circuit picture

    counts = sim.run(transpile(qc, sim), shots=SHOTS).result().get_counts()     # run it
    best = max(counts, key=counts.get)                          # the most common answer
    print(f"Quantum method: found {best} using 1 question (in {counts[best]}/{SHOTS} shots)")
    print("Match!" if best == secret else "Mismatch, check the oracle")

    fig = plot_histogram(counts, title=f"Bernstein-Vazirani: secret {secret} found in one query",
                         color="#E8590C")
    fig.savefig(HERE / "histogram.png", dpi=150, bbox_inches="tight", facecolor="white")
    print(f"\nSaved: circuit.png and histogram.png in {HERE.name}/")
