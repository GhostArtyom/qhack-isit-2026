#!/usr/bin/env python3
"""Check #4: Cold QAOA quality — should match/beat greedy and approach brute-force.
   Runs --nruns times with different seeds, reports the best result.

   Usage: uv run python scripts/check_qaoa.py [--cells N] [--channels K] [--maxiter N] [--nruns N]
"""

import argparse, sys, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

sys.path.insert(0, '.')
from src.graphs import generate_interference_graph
from src.baselines import brute_force, greedy_dfs
from src.solve_qaoa import solve_cold


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cells', type=int, default=8)
    p.add_argument('--channels', type=int, default=3)
    p.add_argument('--penalty', type=float, default=6.0)
    p.add_argument('--maxiter', type=int, default=120)
    p.add_argument('--nruns', type=int, default=1)
    p.add_argument('--seed', type=int, default=42)
    args = p.parse_args()

    ig = generate_interference_graph(n_cells=args.cells, n_channels=args.channels, seed=1)
    bf_assign, bf_obj = brute_force(ig)
    gd_assign, gd_obj = greedy_dfs(ig)
    print(f'N={ig.n_cells} K={ig.n_channels}  brute={bf_obj:.4f}  greedy={gd_obj:.4f}')

    best_rc = None
    best_seed = None
    for run_i in range(args.nruns):
        seed = args.seed + run_i
        t0 = time.time()
        rc, enc = solve_cold(ig, encoding='onehot', penalty=args.penalty, reps=1,
                             maxiter=args.maxiter, seed=seed)
        elapsed = time.time() - t0
        status = '✓' if rc.objective <= gd_obj + 1e-9 else '✗'
        print(f'  run {run_i + 1}/{args.nruns} seed={seed}: obj={rc.objective:.4f}'
              f'  gap={rc.objective - bf_obj:+.4f}  iters={rc.n_iterations}'
              f'  time={elapsed:.0f}s  beat_greedy={status}')
        if best_rc is None or rc.objective < best_rc.objective:
            best_rc = rc
            best_seed = seed

    print(f'\nbest (seed={best_seed}): obj={best_rc.objective:.4f}'
          f'  feasible={best_rc.feasible}  gap={best_rc.objective - bf_obj:+.4f}')
    print(f'assignment: {best_rc.assignment}')

    # --- save figure ---
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00']
    node_colors = [colors[best_rc.assignment[n] % len(colors)] for n in ig.graph.nodes]
    fig, ax = plt.subplots(figsize=(5, 4))
    nx.draw(ig.graph, ig.positions, ax=ax, node_color=node_colors, with_labels=True,
            node_size=300, font_size=8, font_color='white')
    ax.set_title(f'QAOA channel assignment (interference={best_rc.objective:.3f})')
    plt.tight_layout()
    plt.savefig('fig_qaoa_assignment.png', dpi=150)
    plt.close()
    print('Saved: fig_qaoa_assignment.png')

    better_than_greedy = best_rc.objective <= gd_obj + 1e-9
    feasible = best_rc.feasible
    ok = better_than_greedy and feasible
    print(f'\n{"PASS" if ok else "FAIL"}: check #4 cold QAOA quality'
          f'  (feasible={feasible} better_than_greedy={better_than_greedy})')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
