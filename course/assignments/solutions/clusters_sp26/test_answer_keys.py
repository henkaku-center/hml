#!/usr/bin/env python3
"""Runtime test for the SP26 clusters answer keys.

Executes the three solved answer keys end-to-end and reports PASS/FAIL:

  1. clusters_solved.ipynb         (GenJAX canonical)
  2. clusters_python_solved.ipynb  (Python no-GenJAX + optional GenJAX cells)
  3. clusters_solved.Rmd           (R)

The two notebooks are executed cell-by-cell in a single shared namespace
(later cells depend on helpers defined earlier), with a headless matplotlib
backend so plots never block. The R answer key is knitted with
rmarkdown::render().

Usage:
    python3 test_answer_keys.py [--genjax-python PATH] [--rscript PATH]

If --genjax-python is omitted, the script looks for the genjax venv created by
the textbook's test_ch5_code.py at ../../../../textbook/.ch5_test_venv.

Exit code 0 iff every answer key that COULD be tested ran cleanly.
"""

import argparse
import json
import subprocess
import sys
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
GENJAX_NB = HERE / "clusters_solved.ipynb"
PYTHON_NB = HERE / "clusters_python_solved.ipynb"
R_RMD = HERE / "clusters_solved.Rmd"

# The genjax venv built by textbook/test_ch5_code.py.
# HERE = <repo>/course/assignments/solutions/clusters_sp26, so the repo root is
# four levels up and the textbook venv lives at <repo>/textbook/.ch5_test_venv.
# NOTE: do not .resolve() the final path — the venv's bin/python is a symlink to
# the system interpreter that created it, and resolving it would chase the
# symlink OUT of the venv (losing the venv's site-packages, incl. genjax).
# We resolve only the repo-root portion and keep the venv path symlinked.
DEFAULT_VENV_PYTHON = (
    (HERE / ".." / ".." / ".." / "..").resolve()
    / "textbook" / ".ch5_test_venv" / "bin" / "python"
)


# --- Notebook execution ---------------------------------------------------

# Prelude forced into every notebook namespace: headless matplotlib so
# plt.show() never opens a window or blocks.
NB_PRELUDE = (
    "import matplotlib\n"
    "matplotlib.use('Agg')\n"
)


def notebook_code_cells(nb_path):
    """Return the code-cell sources of a notebook, dropping !/% magic lines."""
    nb = json.loads(Path(nb_path).read_text())
    cells = []
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"])
        # Drop jupyter line magics / shell escapes — they aren't valid plain Python.
        src = "\n".join(
            ln for ln in src.split("\n")
            if not ln.strip().startswith("%") and not ln.strip().startswith("!")
        )
        cells.append(src)
    return cells


def make_notebook_runner_script(nb_path):
    """Build a self-contained Python script that runs every code cell of the
    notebook in one shared namespace and prints PASS/FAIL.

    Returned as a string; meant to be executed by the genjax venv's python.
    """
    cells = notebook_code_cells(nb_path)
    payload = json.dumps(cells)
    return f'''
import json, traceback
{NB_PRELUDE}
cells = json.loads({payload!r})
ns = {{"__name__": "__main__"}}
failed = False
for i, src in enumerate(cells):
    try:
        exec(compile(src, "<cell %d>" % i, "exec"), ns)
    except Exception:
        failed = True
        print("  CELL %d FAILED:" % i)
        for line in traceback.format_exc().splitlines():
            print("    " + line)
        break
print("NOTEBOOK_RESULT:" + ("FAIL" if failed else "PASS"))
'''


def run_notebook(nb_path, venv_python):
    """Execute a notebook's code cells via the genjax venv. Returns True on pass."""
    if not nb_path.exists():
        print(f"  SKIP — {nb_path.name} not found")
        return None
    script = make_notebook_runner_script(nb_path)
    result = subprocess.run(
        [str(venv_python), "-c", script],
        capture_output=True, text=True, timeout=600,
    )
    out = result.stdout + result.stderr
    # Echo any cell-failure detail.
    for line in out.splitlines():
        if line.startswith("  CELL") or line.startswith("    "):
            print(line)
    if "NOTEBOOK_RESULT:PASS" in out:
        return True
    if "NOTEBOOK_RESULT:FAIL" in out:
        return False
    # No result marker => the runner itself crashed.
    print("  RUNNER ERROR — raw output:")
    for line in out.splitlines()[-25:]:
        print("    " + line)
    return False


# --- R execution ----------------------------------------------------------

def run_rmd(rmd_path, rscript):
    """Knit the R answer key with rmarkdown::render(). Returns True on pass."""
    if not rmd_path.exists():
        print(f"  SKIP — {rmd_path.name} not found")
        return None
    render_cmd = (
        f'rmarkdown::render("{rmd_path}", quiet = TRUE, '
        f'output_dir = tempdir())'
    )
    result = subprocess.run(
        [rscript, "-e", render_cmd],
        capture_output=True, text=True, timeout=600,
    )
    if result.returncode == 0:
        return True
    print("  R render FAILED:")
    for line in (result.stdout + result.stderr).splitlines()[-30:]:
        print("    " + line)
    return False


# --- Main -----------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--genjax-python", default=str(DEFAULT_VENV_PYTHON),
                        help="Python interpreter with genjax installed.")
    parser.add_argument("--rscript", default="Rscript",
                        help="Rscript executable.")
    args = parser.parse_args()

    venv_python = Path(args.genjax_python)
    results = {}

    print("=" * 64)
    print("SP26 clusters answer-key runtime test")
    print("=" * 64)

    # 1. GenJAX notebook
    print("\n[1] GenJAX answer key — clusters_solved.ipynb")
    if not venv_python.exists():
        print(f"  SKIP — genjax python not found at {venv_python}")
        print("       (run textbook/test_ch5_code.py first to build the venv,")
        print("        or pass --genjax-python)")
        results["genjax"] = None
    else:
        results["genjax"] = run_notebook(GENJAX_NB, venv_python)
        print(f"  RESULT: {_label(results['genjax'])}")

    # 2. Python notebook
    print("\n[2] Python answer key — clusters_python_solved.ipynb")
    if not venv_python.exists():
        print(f"  SKIP — genjax python not found at {venv_python}")
        results["python"] = None
    else:
        results["python"] = run_notebook(PYTHON_NB, venv_python)
        print(f"  RESULT: {_label(results['python'])}")

    # 3. R notebook
    print("\n[3] R answer key — clusters_solved.Rmd")
    rscript_ok = subprocess.run([args.rscript, "--version"],
                                capture_output=True).returncode == 0
    if not rscript_ok:
        print(f"  SKIP — Rscript not runnable ({args.rscript})")
        results["r"] = None
    else:
        results["r"] = run_rmd(R_RMD, args.rscript)
        print(f"  RESULT: {_label(results['r'])}")

    # Summary
    print("\n" + "=" * 64)
    tested = {k: v for k, v in results.items() if v is not None}
    if not tested:
        print("NOTHING TESTED — see SKIP reasons above.")
        sys.exit(1)
    all_pass = all(tested.values())
    for k, v in results.items():
        print(f"  {k:8} {_label(v)}")
    print("=" * 64)
    if all_pass:
        print("ALL TESTED ANSWER KEYS RAN SUCCESSFULLY")
        sys.exit(0)
    print("ONE OR MORE ANSWER KEYS FAILED")
    sys.exit(1)


def _label(v):
    return {True: "PASS", False: "FAIL", None: "SKIPPED"}[v]


if __name__ == "__main__":
    main()
