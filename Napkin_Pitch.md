# Napkin Pitch: Quantum-Boosted Channel Allocation for Dense Small-Cell Networks

**The Problem:** Channel allocation in dense small-cell networks is a weighted graph-coloring problem → a QUBO. It's NP-hard, and—critically—it's *recurring*: under user/cell mobility the interference graph changes, so the same QUBO family must be re-solved snapshot after snapshot. Greedy heuristics leave interference on the table; exact solvers don't scale; neither re-converges fast.

**Your Solution:** Hybrid QAOA on the coloring QUBO (Qiskit QAOA + classical COBYLA), on an Aer statevector simulator. For the dynamic regime, **warm-start QAOA**: relax the prior snapshot's bitstring to continuous amplitudes and use it to initialize both the ansatz state and the mixer, so re-optimization starts inside the basin of the previous solution and reaches near-optimal quality at a far smaller QAOA iteration budget than a cold restart (each iteration is the expensive part on NISQ hardware). We also study **one-hot vs binary encodings** as a qubit/depth ansatz-design decision.

**Hack Ingredients:** Qiskit · qiskit-optimization (GraphColoring QUBO builder, WarmStartQAOAOptimizer) · qiskit-aer (statevector simulator) · NetworkX (interference graphs) · NumPy/SciPy (classical baselines) · Python on a laptop.

**Unique Value Proposition:** Two quantum-algorithm-level contributions that land on a communication problem. (1) **Warm-start QAOA = cheap incremental re-optimization for dynamic QUBOs**—attacking QAOA's real cost (variational parameter search) on a real structural feature (adjacent snapshots differ by a small perturbation): for the same optimizer budget it returns a markedly better approximation than a cold restart. (2) An **encoding selection rule for minimum-qubit ansätze**: one-hot (N·K qubits, shallow penalty) vs binary (N·⌈log₂K⌉ qubits, denser/deeper cost Hamiltonian)—a qubit-vs-depth-vs-feasibility trade-off reusable on any networking QUBO. Value: more served users per channel in dense deployments, with a credible quantum path to scale.

**Current Status:** QUBO formulation validated against brute force on small interference graphs; QAOA-vs-greedy and warm-start-vs-cold-start baselines coded and running on the simulator (warm-start shows fewer optimizer iterations); one-hot vs binary encoding trade-off benchmarked. Scaling the demo to mid-size graphs and packaging a live re-allocation visualization for the final.

**Hackathon Theme:** Solving Problems in Communication and Signal Processing using Quantum Computing.

---

## 中文对照（备稿 / 答辩用）

**问题：** 密集小蜂窝网络的信道分配是加权图着色问题 → QUBO。NP-hard，且关键在于它是*反复出现*的：在用户/基站移动性下干扰图不断变化，同一族 QUBO 要逐快照反复求解。贪心启发式留下干扰余量；精确求解器不可扩展；两者都重收敛不够快。

**方案：** 在着色 QUBO 上跑混合 QAOA（Qiskit QAOA + 经典 COBYLA），后端为 Aer statevector 模拟器。针对动态场景做**暖启动 QAOA**：把上一快照的 bitstring 松弛为连续振幅，同时初始化 ansatz 态与 mixer，使重优化从上一解的盆地内起步，在远更小的 QAOA 迭代预算下达到近最优质量（每次迭代才是 NISQ 上最贵的部分）。同时研究 **one-hot vs 二进制编码**作为量子比特/深度的 ansatz 设计决策。

**技术要素：** Qiskit · qiskit-optimization（GraphColoring QUBO 构造器、WarmStartQAOAOptimizer）· qiskit-aer（statevector 模拟器）· NetworkX（干扰图）· NumPy/SciPy（经典基线）· 笔记本上的 Python。

**独特价值：** 两个量子算法层面的贡献，恰好落在通信问题上。(1) **暖启动 QAOA = 面向动态 QUBO 的低成本增量重优化**——对准 QAOA 最昂贵的开销（变分参数搜索），对应真实的结构特征（相邻快照只差小扰动）：在相同优化器预算下，它返回的近似比冷启动显著更优。(2) **最小量子比特 ansatz 的编码选择规则**：one-hot（N·K 量子比特、penalty 浅）vs 二进制（N·⌈log₂K⌉ 量子比特、cost Hamiltonian 更稠密更深）——量子比特 vs 深度 vs 可行率的权衡，可复用于任何网络类 QUBO。价值：密集部署中每信道服务更多用户，并有可信的量子扩展路径。

**当前进展：** QUBO 建模已对照暴力法在小型干扰图上验证；QAOA-vs-贪心、暖启动-vs-冷启动基线已编码并在模拟器上跑通（在固定迭代预算下暖启动近似比冷启动更优）；one-hot vs 二进制编码权衡已完成基准。正在扩展到中规模图并为决赛打包实时重分配可视化。

**黑客松主题：** 用量子计算解决通信与信号处理中的问题。

---

## 英文路演讲稿（~4 分钟 / ~560 词，量子计算视角）

> 面向 ISIT 量子计算同行听众；从量子算法/线路设计视角展开，通信问题只用一句动机带过。语速 ~140 wpm。

**[Problem]** Quick motivation, then I'll get to the quantum part. Dense small-cell networks have to assign channels to minimize interference — that's weighted graph coloring, and it's a QUBO. The non-trivial feature is that it's **recurring**: the graph changes under mobility, so you re-solve the same QUBO family over and over. That structure is what we exploit.

**[Solution]** We run hybrid QAOA on the coloring QUBO. The standard cold start re-optimizes every parameter from scratch each snapshot. Our move is **warm-start QAOA**: we take the previous snapshot's bitstring, relax it to continuous amplitudes, and use it to initialize both the ansatz state and the mixer, so the variational search starts inside the basin of the prior solution. The honest result — and the NISQ-relevant one — is about *iteration budget*: at a fixed, tight optimizer budget where a cold restart is still far from optimum, warm-start lands much closer, because it doesn't pay the restart cost. Each QAOA iteration is the expensive part on hardware, so a better approximation per iteration is the win that matters. We're using Qiskit's WarmStartQAOAOptimizer on an Aer statevector backend.

**[Encoding]** The second thread is **encoding as a circuit-design decision**. Graph coloring admits two natural QUBO encodings: one-hot — a binary variable per (node, color) pair, N-times-K qubits, trivial constraints, shallow penalty term — versus binary — log-2-of-K variables per node, far fewer qubits, but the "one color per node" constraint becomes a denser, higher-weight penalty, so the cost Hamiltonian gets deeper and the feasible subspace is smaller. That's a genuine ansatz-resource trade-off: qubit count against Hamiltonian depth against feasible-solution rate. We benchmark both on the same graphs and report where each wins. This is the kind of design reasoning that's reusable on any networking QUBO, not just this one.

**[Hack Ingredients]** Stack: Qiskit, qiskit-optimization — which hands us the warm-start optimizer; we build the coloring QUBO ourselves, since the optimization package ships graph apps like Max-Cut and Vertex-Cover but not coloring — qiskit-aer for statevector, NetworkX for the interference graphs.

**[Value]** So the contribution isn't "QAOA solves a coloring problem." It's two things: **warm-start QAOA as a cheap incremental optimizer for dynamic QUBOs** — better approximation per optimizer iteration, which is the cost that matters on hardware — and an **encoding selection rule for minimum-qubit ansätze**. Both are quantum-algorithm-level results that happen to land on a communication problem.

**[Current Status]** Status: QUBO validated against brute force on small graphs; at a fixed optimizer budget, warm-start lands nearer optimum than cold-start on the majority of mobility snapshots; encoding trade-off benchmarked. Next: mid-size graphs and a live re-allocation demo for the final. Limits, honestly: simulator-only, no noise model yet, QAOA depth bounded by simulator cost.

**[Close]** A real, runnable quantum-classic hybrid pipeline attacking a recurring QUBO from the algorithm side. Quantum computing for communication and signal processing — thank you.
