#!/usr/bin/env python3
"""Plot the interference graph (visualization only, no check).

   Usage: uv run python scripts/plot_graph.py [--cells N] [--channels K]
"""

import argparse, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

sys.path.insert(0, '.')
from src.graphs import generate_interference_graph


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cells', type=int, default=8)
    p.add_argument('--channels', type=int, default=3)
    p.add_argument('--seed', type=int, default=1)
    args = p.parse_args()

    ig = generate_interference_graph(n_cells=args.cells, n_channels=args.channels, seed=args.seed)
    print(f'N={ig.n_cells} K={ig.n_channels} edges={ig.graph.number_of_edges()}')
    print(f'edge weight range: {min(ig.weights.values()):.3f} .. {max(ig.weights.values()):.3f}')

    fig, ax = plt.subplots(figsize=(5, 4))
    pos = ig.positions
    nx.draw(ig.graph, pos, ax=ax, node_color='tab:blue', with_labels=True,
            node_size=300, font_size=8)
    weights = [3 * ig.graph[u][v]['weight'] for u, v in ig.graph.edges()]
    nx.draw_networkx_edges(ig.graph, pos, ax=ax, width=weights, edge_color='tab:gray')
    ax.set_title('Interference graph (edge width = coupling)')
    plt.tight_layout()
    plt.savefig('fig_interference_graph.png', dpi=150)
    plt.close()
    print('Saved: fig_interference_graph.png')


if __name__ == '__main__':
    main()
