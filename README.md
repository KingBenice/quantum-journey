# quantum-journey

Hey, I'm Benjamin Akinade 👋🏾

I do IT support, build websites with Framer, and design for brands here in Lagos. I studied computer science, and quantum physics has been my thing for years (along with astrophysics). So I finally decided to stop just reading about quantum computing and actually start building with it.

This repo is me learning out loud. Small projects, one at a time, each one a bit harder than the last. I'm posting the journey on X too: [@Capt_KingBenice](https://x.com/Capt_KingBenice)

## What's in here so far

1. **[Coin flip](01-quantum-coin-flip/)**: one qubit, 50/50 heads or tails. Where it all starts.
2. **[Entanglement](02-bell-state-entanglement/)**: two qubits that always agree, no matter what.
3. **[Teleportation](03-quantum-teleportation/)**: moving a qubit's state using entanglement plus two normal bits. (No, not Star Trek 😅)
4. **[Bernstein-Vazirani](04-bernstein-vazirani/)**: finding a hidden number in one try instead of many.
5. **[Grover's search](05-grover-search/)**: finding the right answer faster than checking one by one.
6. **[Real IBM hardware](06-run-on-real-hardware/)** (bonus): running a circuit on an actual quantum computer, noise and all.

Each folder has the code, a short write-up in plain English, and the charts it produced.

## Want to run it?

```
python -m venv .venv
.venv\Scripts\activate        (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
cd 01-quantum-coin-flip
python coin_flip.py
```

On Windows and new to Python? [SETUP_GUIDE.md](SETUP_GUIDE.md) walks you through it.

Heads up: everything runs on a simulator on your laptop unless you're in folder 06.

## A couple of results I like

Entanglement: the qubits only ever land on 00 or 11, never mixed.

![Bell state](02-bell-state-entanglement/histogram.png)

Grover: the right answer jumps out after just a couple of rounds.

![Grover rounds](05-grover-search/rounds.png)

## Next up

Deutsch-Jozsa, the quantum Fourier transform, and more runs on real hardware. I'll also write down what I get wrong, because that's half of learning.

If you spot a mistake or have a tip, open an issue or DM me on X. I'd genuinely appreciate it.
