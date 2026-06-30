#!/usr/bin/env python3
"""Check #1: QUBO correctness — one-hot & binary argmin must match brute-force optimum.

   Usage: uv run python scripts/check_qubo.py [--cells N] [--channels K]
"""

import argparse, itertools, sys, time
import numpy as np

sys.path.insert(0, '.')
from src.graphs import generate_interference_graph
from src.qubo import build_encoding, interference_objective, _keff
from src.baselines import brute_force, greedy_dfs


def onehot_argmin(ig, penalty):
    N, K = ig.n_cells, ig.n_channels
    best = (None, 1e18)
    for combo in itertools.product(range(K), repeat=N):
        x = np.zeros(N * K)
        for v, c in enumerate(combo):
            x[v * K + c] = 1
        enc = build_encoding(ig, encoding='onehot', penalty=penalty)
        val = enc.qp.objective.evaluate(x)
        if val < best[1]:
            best = (combo, val)
    return interference_objective(ig, dict(enumerate(best[0])))


def binary_argmin(ig, penalty):
    N, K, Ke = ig.n_cells, ig.n_channels, _keff(ig.n_channels)
    best = (None, 1e18)
    for bits in itertools.product(range(2), repeat=N * Ke):
        x = np.array(bits, dtype=float)
        enc = build_encoding(ig, encoding='binary', penalty=penalty)
        val = enc.qp.objective.evaluate(x)
        if val < best[1]:
            best = (bits, val)
    enc = build_encoding(ig, encoding='binary', penalty=penalty)
    return interference_objective(ig, enc.decode(np.array(best[0], dtype=float)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cells', type=int, default=8)
    p.add_argument('--channels', type=int, default=3)
    p.add_argument('--penalty', type=float, default=6.0)
    p.add_argument('--seed', type=int, default=1)
    args = p.parse_args()

    ig = generate_interference_graph(n_cells=args.cells, n_channels=args.channels, seed=args.seed)
    print(f'Graph: N={ig.n_cells} K={ig.n_channels} edges={ig.graph.number_of_edges()}')

    bf_assign, bf_obj = brute_force(ig)
    gd_assign, gd_obj = greedy_dfs(ig)
    print(f'brute-force optimum = {bf_obj:.4f}')
    print(f'greedy             = {gd_obj:.4f}  (gap {gd_obj - bf_obj:+.4f})')

    t0 = time.time()
    oh = onehot_argmin(ig, args.penalty)
    t1 = time.time()
    bn = binary_argmin(ig, args.penalty)
    t2 = time.time()

    print(f'\none-hot argmin = {oh:.4f}  matches brute: {abs(oh - bf_obj) < 1e-9}  ({t1 - t0:.1f}s)')
    print(f'binary  argmin = {bn:.4f}  matches brute: {abs(bn - bf_obj) < 1e-9}  ({t2 - t1:.1f}s)')
    print(f'\nqubits: one-hot={ig.n_cells * ig.n_channels}  binary={ig.n_cells * _keff(ig.n_channels)}')

    ok = abs(oh - bf_obj) < 1e-9 and abs(bn - bf_obj) < 1e-9
    print(f'\n{"PASS" if ok else "FAIL"}: check #1 QUBO correctness')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
