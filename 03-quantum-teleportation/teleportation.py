# Project 3: Quantum teleportation
# Idea: Alice sends the state of one qubit to Bob using one shared entangled pair plus two normal bits.
# To check it worked, Bob "undoes" the state he should have received. If teleportation worked, he always reads 0.

import math                                  # for pi
from pathlib import Path                     # file paths

import matplotlib                            # plotting
matplotlib.use("Agg")                        # save to files, no windows
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile  # circuit building blocks
from qiskit.visualization import plot_histogram   # bar charts
from qiskit_aer import AerSimulator               # local simulator

HERE = Path(__file__).parent                 # this script's folder
sim = AerSimulator()                         # the simulator
SHOTS = 1024                                 # number of repeats

THETA = 1.1                                  # angle that picks the 'mystery' state Alice sends (any value works)
PHI = 0.7                                    # a second angle, so the state is not a simple 0 or 1


def teleport_circuit(theta=THETA, phi=PHI):
    msg = QuantumRegister(1, "msg")          # Alice's qubit holding the state she wants to send
    alice = QuantumRegister(1, "alice")      # Alice's half of the entangled pair
    bob = QuantumRegister(1, "bob")          # Bob's half of the entangled pair
    c_alice = ClassicalRegister(2, "alice_bits")  # the two normal bits Alice sends to Bob
    c_bob = ClassicalRegister(1, "bob_check")     # where we record Bob's final check
    qc = QuantumCircuit(msg, alice, bob, c_alice, c_bob)

    qc.ry(theta, msg)                        # step 0: create the mystery state on Alice's message qubit
    qc.rz(phi, msg)                          # (two rotations give a state with a phase, not just a mix)
    qc.barrier()                             # a visual divider in the drawing

    qc.h(alice)                              # step 1: make an entangled (Bell) pair...
    qc.cx(alice, bob)                        # ...shared between Alice and Bob
    qc.barrier()

    qc.cx(msg, alice)                        # step 2: Alice links her message qubit to her half of the pair
    qc.h(msg)                                # and rotates it so the next measurement reads out the right info
    qc.barrier()

    qc.measure(msg, c_alice[0])              # step 3: Alice measures both her qubits...
    qc.measure(alice, c_alice[1])            # ...and gets two normal bits, which she 'phones' to Bob

    with qc.if_test((c_alice[1], 1)):        # step 4: if Alice's second bit is 1...
        qc.x(bob)                            # ...Bob flips his qubit (X gate)
    with qc.if_test((c_alice[0], 1)):        # if Alice's first bit is 1...
        qc.z(bob)                            # ...Bob applies a phase flip (Z gate)
    qc.barrier()                             # now Bob's qubit holds Alice's original state

    qc.rz(-phi, bob)                         # check: undo the two rotations in reverse order
    qc.ry(-theta, bob)                       # if Bob really has the state, this returns him to exactly 0
    qc.measure(bob, c_bob[0])                # measure Bob's qubit
    return qc


def bob_results(counts):
    tally = {"0": 0, "1": 0}                 # how often Bob's check came out 0 or 1
    for key, n in counts.items():            # keys look like 'b aa' (Bob's bit, a space, Alice's two bits)
        tally[key.split(" ")[0]] += n        # take only Bob's bit
    return tally


if __name__ == "__main__":
    qc = teleport_circuit()                                      # build the full protocol
    print(qc.draw("text", fold=-1))                               # print it (wide terminal helps)
    qc.draw("mpl", fold=-1).savefig(HERE / "circuit.png", dpi=150, bbox_inches="tight", facecolor="white")  # save the picture

    counts = sim.run(transpile(qc, sim), shots=SHOTS).result().get_counts()  # run it
    alice_only = {}                                               # Alice's two bits on their own
    for key, n in counts.items():
        a = key.split(" ")[1]
        alice_only[a] = alice_only.get(a, 0) + n
    bob = bob_results(counts)

    print(f"\nAlice's two measured bits (random): {dict(sorted(alice_only.items()))}")
    print(f"Bob's check after undoing the state: {bob}")
    print(f"Teleportation success rate: {100 * bob['0'] / SHOTS:.1f}%")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))            # two charts side by side
    plot_histogram(alice_only, ax=axes[0], color="#868E96",
                   title="Alice's 2 bits: random every time")
    axes[0].set_title("Alice's 2 bits: random every time")  # label each chart clearly
    plot_histogram(bob, ax=axes[1], color="#2B8A3E",
                   title="Bob's check: always 0 = state arrived")
    axes[1].set_title("Bob's check: always 0 = state arrived")
    fig.tight_layout()
    fig.savefig(HERE / "histogram.png", dpi=150, bbox_inches="tight", facecolor="white")
    print(f"\nSaved: circuit.png and histogram.png in {HERE.name}/")
