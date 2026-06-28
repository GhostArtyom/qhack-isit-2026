# Napkin Pitch Speech

Hello everyone, my group name is The Entangler. Our project name is Quantum-Boosted Channel Allocation for Dense Small-Cell Networks.

You know, 5G technology is based on small-cell base stations. The problem is that: dozens of these cells squeezing into a few channels. If two cells are too close, they cannot share a channel without interference, so someone has to decide who gets which channel to keep out channel jam. That's weighted graph coloring — a NP-hard problem. But it's not a one-shot problem. People move, traffic shifts, the interference graph changes every snapshot, and you have to re-solve the same puzzle over and over again. Same structure, just a bit different at each time.

So we try to use QAOA to solve it. Normal QAOA starts fresh every snapshot: each optimizer step costs circuit runs, sampling, expectation estimation. It's too expensive. Our idea is to take the last snapshot's solution, and use it to set the next QAOA's starting point — the initial state and mixer — so each search begins near where it left off, not from scratch. The graph only changed a little bit, so the old solution is probably still close to the optimal solution.

That's the main thread, but there's a second one: how to encode the problem into qubits. For graph coloring, it has two natural choices. One-hot encoding gives every cell-channel pair its own qubit — N times K qubits, simple penalties, shallow circuit. Binary encoding packs the channel index into log₂K bits per cell — way fewer qubits, but the cost Hamiltonian gets denser and the circuit gets deeper. It's a real qubit-versus-depth trade-off, and we benchmark both on the same graphs.

For tech stack, we use WarmStartQAOAOptimizer of qiskit-optimization and statevector simulator of qiskit-aer for simulating variational quantum circuits, and use NetworkX for interference graphs.

So the unique value of our project is: first, warm-start QAOA as a cheap incremental re-optimizer for dynamic QUBOs, and second, an encoding rule for minimum-qubit ansatz.

The current status is QUBO validated against brute force on small graphs. Warm-start is closer to optimal than cold-start at a fixed optimizer budget. Also, encoding trade-off is benchmarked. The next stage we will analyze mid-size graphs.

That all, thank you!
