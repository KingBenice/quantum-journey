# Beginner setup guide (Windows)

About 20 minutes. You only do Part 1 once.

## Part 1: Install Python and Qiskit
1. Go to python.org/downloads/windows and download the **Windows installer (64-bit)** for **Python 3.13** (all the packages here have Windows builds for it).
2. Run the installer and tick **"Add python.exe to PATH"** on the first screen, then click Install Now.
3. Open **Command Prompt** and check it worked: `python --version`
4. Get the code. Either download this repo as a ZIP from GitHub (green "Code" button, then "Download ZIP") and unzip it, or `git clone` it. Then go into the folder:
   `cd Downloads\quantum-journey`
5. Make a virtual environment (a private box for this project's packages) and switch it on:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```
   You will see `(.venv)` at the start of the line. In PowerShell use `.venv\Scripts\Activate.ps1` instead.
6. Install everything: `pip install -r requirements.txt`

## Part 2: Run the projects
```
cd 01-quantum-coin-flip
python coin_flip.py
cd ..\02-bell-state-entanglement
python bell_state.py
```
Do the same for folders 03, 04 and 05. Each script prints its results and saves PNG images next to itself. Next time, just `cd` into the repo and run `.venv\Scripts\activate` again first.

**If something goes wrong:** "python is not recognized" means PATH was not ticked, so re-run the installer and choose Modify. "No module named qiskit" means the `(.venv)` is not active.

## Part 3 (optional): Real IBM quantum hardware, free
Checked on IBM's live pages on 24 Oct 2026:
- IBM Quantum Platform's **Open Plan** is free: up to **10 minutes of QPU time per 28-day rolling window** on real 100+ qubit processors.
- IBM is also running a limited-time promotion (announced 16 Mar 2026): Open Plan users on a non-trial account who use 20 minutes within 12 months can opt in to 180 minutes over the next 12 months.
- Only Open Plan instances are free. Other plans cost money, so always check that your instance says **Open Plan**.

Steps:
1. Go to **quantum.cloud.ibm.com** and sign up or log in with an **IBMid or a Google account**.
2. In the region switcher at the top, choose **us-east**. Open Plan instances can only be created there.
3. On the **Instances** page, create an instance with the **Open Plan**, then copy its **CRN**.
4. On the dashboard, create an **API key** and keep it private. Never post it on GitHub or X.
5. Save them once on your laptop (inside the `(.venv)`):
   ```
   python -c "from qiskit_ibm_runtime import QiskitRuntimeService; QiskitRuntimeService.save_account(token='YOUR_API_KEY', instance='YOUR_CRN', set_as_default=True)"
   ```
6. Test without using any time: `python 06-run-on-real-hardware\run_on_ibm.py --fake`. Then run it for real without `--fake`. Jobs can wait in a queue, and you can watch them on the **Workloads** page.

Sources: quantum.cloud.ibm.com/docs/en/guides/plans-overview, .../guides/cloud-setup, .../guides/instances, and ibm.com/quantum/blog/open-plan-updates. Plans change, so re-check those pages before you rely on the numbers.
