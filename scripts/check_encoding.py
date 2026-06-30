#!/usr/bin/env python3
"""Check #3: Encoding trade-off — one-hot vs binary across (N, K) combos.

   Usage: uv run python scripts/check_encoding.py
"""

import sys, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, '.')
from src.encoding_study import study, print_table


def main():
    combos = [(8, 3), (10, 3), (12, 3)]
    all_rows = []
    for n, k in combos:
        t0 = time.time()
        rows = study(n_cells=n, n_channels=k, reps=1, n_runs=3)
        elapsed = time.time() - t0
        all_rows += rows
        print(f'\nN={n} K={k} ({elapsed:.0f}s)')

    print()
    print_table(all_rows)

    # --- save figure ---
    df = pd.DataFrame([{
        'graph': r.graph_id, 'enc': r.encoding, 'qubits': r.n_qubits,
        'depth': r.depth, 'gates': r.n_gates,
        'K': r.n_channels, 'N': r.n_cells,
    } for r in all_rows])

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    for enc, marker, color in [('onehot', 'o', 'C0'), ('binary', '^', 'C1')]:
        sub = df[df.enc == enc]
        a1.plot(sub.K, sub.qubits, marker + '-', color=color, label=enc)
        a2.plot(sub.K, sub.depth, marker + '-', color=color, label=enc)
    a1.set_xlabel('K (channels)'); a1.set_ylabel('qubits')
    a1.set_title('Qubits: one-hot N·K vs binary N·⌈log₂K⌉')
    a1.legend(); a1.grid(alpha=0.3)
    a2.set_xlabel('K (channels)'); a2.set_ylabel('decomposed ansatz depth')
    a2.set_title('Depth: binary denser cost Hamiltonian')
    a2.legend(); a2.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_encoding_tradeoff.png', dpi=150)
    plt.close()
    print('\nSaved: fig_encoding_tradeoff.png')

    # quick sanity: binary should have fewer qubits than one-hot for same (N,K)
    ok = True
    for r in all_rows:
        partner = [x for x in all_rows if x.graph_id == r.graph_id and x.encoding != r.encoding]
        if partner:
            other = partner[0]
            if r.encoding == 'binary':
                ok = ok and (r.n_qubits <= other.n_qubits)
    print(f'\n{"PASS" if ok else "FAIL"}: check #3 binary ≤ onehot qubits')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
