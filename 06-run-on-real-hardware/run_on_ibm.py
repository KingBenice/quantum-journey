# Bonus: run the Bell state (Project 2) on a real IBM quantum computer.
# Before using this: create a free IBM Quantum Platform account, make an Open Plan instance,
# and save your API key once (see SETUP_GUIDE.md). Each run uses a small part of your free monthly time.
#
# Test it first without an account:  python run_on_ibm.py --fake
# (--fake uses a built-in copy of an old IBM chip's noise, running on your laptop.)

import sys                                   # read the --fake flag
from pathlib import Path                     # file paths

import matplotlib
matplotlib.use("Agg")                        # save plots to files

from qiskit import QuantumCircuit            # circuit builder
from qiskit.transpiler import generate_preset_pass_manager  # rewrites the circuit for a real chip's layout
from qiskit.visualization import plot_histogram
from qiskit_ibm_runtime.executor_sampler import Sampler     # the 'run circuits and give me counts' tool (qiskit-ibm-runtime 0.50+)

HERE = Path(__file__).parent

qc = QuantumCircuit(2)                       # 2 qubits
qc.h(0)                                      # superposition
qc.cx(0, 1)                                  # entangle
qc.measure_all()                             # measure everything

if "--fake" in sys.argv:                     # practice mode: no account needed
    from qiskit_ibm_runtime.fake_provider import FakeManilaV2
    backend = FakeManilaV2()                 # a simulated copy of a retired 5-qubit IBM chip, noise included
else:
    from qiskit_ibm_runtime import QiskitRuntimeService
    service = QiskitRuntimeService()         # loads the API key you saved with save_account()
    backend = service.least_busy(operational=True, simulator=False)  # pick the real chip with the shortest queue

print(f"Running on: {backend.name}")
pm = generate_preset_pass_manager(backend=backend, optimization_level=1)  # fit the circuit to this chip
isa_circuit = pm.run(qc)                     # the chip-ready version of our circuit

sampler = Sampler(mode=backend)              # connect the sampler to the chosen backend
job = sampler.run([isa_circuit], shots=1024) # send the job (a real chip may queue for a while)
if "--fake" not in sys.argv:                 # only real jobs show up on the IBM website
    print(f"Job ID: {job.job_id()}  (you can watch it on the IBM Quantum Platform 'Workloads' page)")

result = job.result()[0]                     # wait for the result of our one circuit
counts = result.data.meas.get_counts()       # 'meas' is the name measure_all() gives the classical bits
print("Counts:", dict(sorted(counts.items())))
agree = counts.get("00", 0) + counts.get("11", 0)
print(f"Qubits agreed in {100 * agree / sum(counts.values()):.1f}% of shots "
      "(a perfect, noise-free machine would give 100%; real chips have a little noise)")

name = "hardware_histogram.png" if "--fake" not in sys.argv else "fake_backend_histogram.png"
plot_histogram(counts, title=f"Bell state on {backend.name}", color="#C2255C").savefig(
    HERE / name, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Saved: {name}")
