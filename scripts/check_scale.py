#!/usr/bin/env python3
"""Check #5: Scalability — midsize graph (14 cells, 4 channels) via binary encoding.
   Brute force is intractable here; QAOA must beat greedy.

   Usage: uv run python scripts/check_scale.py [--cells N] [--channels K]
"""

import argparse, sys, time
import numpy as np

sys.path.insert(0, '.')
from src.graphs import midsize_graph, generate_interference_graph
from src.qubo import _keff
from src.baselines import greedy_dfs
from src.solve_qaoa import solve_cold


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cells', type=int, default=10)
    p.add_argument('--channels', type=int, default=3)
    p.add_argument('--penalty', type=float, default=10.0)
    p.add_argument('--maxiter', type=int, default=40)
    p.add_argument('--seed', type=int, default=42)
    args = p.parse_args()

    mid = generate_interference_graph(n_cells=args.cells, n_channels=args.channels, seed=0)
    n_onehot = mid.n_cells * mid.n_channels
    n_binary = mid.n_cells * _keff(mid.n_channels)
    n_brute = mid.n_channels ** mid.n_cells
    print(f'mid-size: N={mid.n_cells} K={mid.n_channels} edges={mid.graph.number_of_edges()}')
    print(f'qubits: one-hot={n_onehot} binary={n_binary}  (brute={n_brute} assignments)')

    gd_assign, gd_obj = greedy_dfs(mid)
    print(f'greedy = {gd_obj:.4f}')

    t0 = time.time()
    rc, enc = solve_cold(mid, encoding='binary', penalty=args.penalty, reps=1,
                         maxiter=args.maxiter, seed=args.seed)
    elapsed = time.time() - t0

    print(f'QAOA (binary) = {rc.objective:.4f}  feasible={rc.feasible}'
          f'  iters={rc.n_iterations}  time={elapsed:.0f}s')
    print(f'QAOA vs greedy: {rc.objective - gd_obj:+.4f}')

    better = rc.objective <= gd_obj + 1e-9
    ok = rc.feasible and better
    print(f'\n{"PASS" if ok else "FAIL"}: check #5 scalability'
          f'  (feasible={rc.feasible} better_than_greedy={better})')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
