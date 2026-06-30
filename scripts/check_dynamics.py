#!/usr/bin/env python3
"""Check #2 (HEADLINE): Warm-start dynamics — N=8, tight maxiter budget.
   Cold vs warm QAOA across a mobility sequence at fixed maxiter.

   Usage: uv run python scripts/check_dynamics.py [--cells N] [--channels K] [--maxiter N] [--snapshots N]
"""

import argparse, sys, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, '.')
from src.graphs import small_graph
from src.dynamics import run_dynamics


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cells', type=int, default=8)
    p.add_argument('--channels', type=int, default=3)
    p.add_argument('--penalty', type=float, default=6.0)
    p.add_argument('--maxiter', type=int, default=25)
    p.add_argument('--snapshots', type=int, default=5)
    p.add_argument('--seed', type=int, default=42)
    args = p.parse_args()

    ig = small_graph(seed=1)
    print(f'Base graph: N={ig.n_cells} K={ig.n_channels} edges={ig.graph.number_of_edges()}')
    print(f'maxiter={args.maxiter}  snapshots={args.snapshots}\n')

    t0 = time.time()
    rep = run_dynamics(base=ig, n_snapshots=args.snapshots, encoding='onehot',
                       penalty=args.penalty, reps=1, maxiter=args.maxiter,
                       seed=args.seed, perturb_seed=1)
    elapsed = time.time() - t0

    # --- print table ---
    rows = rep.iter_table()
    header = f"{'snap':>4} {'brute':>8} {'cold':>8} {'warm':>8} {'c_gap':>7} {'w_gap':>7} {'warm<':>6}"
    print(header)
    print('-' * len(header))
    for r in rows:
        wb = 'YES' if r['warm_gap'] < r['cold_gap'] - 1e-9 else ''
        print(f"{r['snapshot']:>4} {r['brute']:>8.3f} {r['cold_obj']:>8.3f} "
              f"{r['warm_obj']:>8.3f} {r['cold_gap']:>7.3f} {r['warm_gap']:>7.3f} {wb:>6}")

    print(f'\nMean gap:  cold={rep.mean_cold_gap:.4f}  warm={rep.mean_warm_gap:.4f}')
    print(f'Gap reduction: {rep.mean_cold_gap - rep.mean_warm_gap:+.4f}')
    print(f'Warm better on {rep.warm_better_count}/{len(rep.snapshots)} snapshots')
    print(f'Time: {elapsed:.0f}s')

    # --- save figure ---
    snaps = [r['snapshot'] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(snaps, [r['brute'] for r in rows], 'k--o', label='brute-force optimum')
    ax.plot(snaps, [r['cold_obj'] for r in rows], 'rs-', label='cold-start QAOA')
    ax.plot(snaps, [r['warm_obj'] for r in rows], 'g^-', label='warm-start QAOA')
    ax.set_xlabel('mobility snapshot')
    ax.set_ylabel('co-channel interference')
    ax.set_title(f'Warm-start vs cold-start QAOA @ maxiter={args.maxiter}\n'
                 f'(mean gap: warm {rep.mean_warm_gap:.3f} vs cold {rep.mean_cold_gap:.3f})')
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('fig_mobility_dynamics.png', dpi=150)
    plt.close()
    print('Saved: fig_mobility_dynamics.png')

    ok = rep.mean_warm_gap <= rep.mean_cold_gap + 1e-9
    print(f'\n{"PASS" if ok else "NOTE"}: warm gap <= cold gap  (mean_warm={rep.mean_warm_gap:.4f} mean_cold={rep.mean_cold_gap:.4f})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
