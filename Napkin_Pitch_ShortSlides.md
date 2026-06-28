# Napkin Pitch — 短句幻灯片版 + 中文翻译 + 详细解释

> 用途：这是**真正要放上单页幻灯片**的版本——每段都是短句、关键词驱动，听众扫一眼即懂。下面先给英文短句版（路演主用），再给逐句中文翻译，最后给**详细解释**（讲稿/答辩储备，不上幻灯片）。

---

## 1. 英文短句版（幻灯片正文）

**Quantum-Boosted Channel Allocation for Dense Small-Cell Networks**

**Problem** — Channel allocation in small cells = weighted graph coloring → QUBO. NP-hard. **Recurring**: graph shifts under mobility → same QUBO family re-solved every snapshot.

**Solution** — Hybrid QAOA on the coloring QUBO. **Warm-start from prior snapshot solution** for fast re-optimization. One-hot vs binary encoding study.

**Hack Ingredients** — Qiskit · qiskit-optimization (WarmStartQAOAOptimizer) · qiskit-aer (statevector) · NetworkX.

**Unique Value** — (1) **Warm-start QAOA = cheap incremental re-optimization for dynamic QUBOs.** (2) **Encoding rule for minimum-qubit ansätze** — reusable on any networking QUBO.

**Current Status** — QUBO validated vs brute force. Warm-start nearer optimum (4/5 snapshots at fixed budget). Encoding trade-off benchmarked. → Scaling to mid-size graphs.

**Theme** — Quantum Computing for Communication & Signal Processing.

---

## 2. 中文对照（备稿 / 答辩用）

**面向密集小蜂窝网络的量子增强频谱分配**

**问题** —— 小蜂窝信道分配 = 加权图着色 → QUBO。NP-hard。**反复出现**：移动性下干扰图持续变化 → 同一族 QUBO 逐快照重解。

**方案** —— 在着色 QUBO 上跑混合 QAOA。**从上一快照解暖启动**快速重优化。One-hot vs 二进制编码研究。

**技术要素** —— Qiskit · qiskit-optimization（WarmStartQAOAOptimizer）· qiskit-aer（statevector）· NetworkX。

**独特价值** —— (1) **暖启动 QAOA = 面向动态 QUBO 的低成本增量重优化。** (2) **最小量子比特 ansatz 的编码规则**——可复用于任何网络类 QUBO。

**当前进展** —— QUBO 已对照暴力法验证。固定预算下暖启动优于冷启动（4/5 快照）。编码权衡已基准。→ 扩展到中规模图。

**主题** —— 用量子计算解决通信与信号处理问题。

---

## 3. 详细解释（讲稿/答辩储备，不上幻灯片）

> 以下逐段展开，供你口头讲 3-5 分钟、以及 Q&A 被追问时使用。视角从**量子算法/线路**出发——因为听众里有量子计算同行，你自己也做量子计算。

### Problem —— 为什么这是个值得用量子计算解决的问题

**"信道分配 = 加权图着色 → QUBO"**：把每个小蜂窝当成图的一个节点；两个蜂窝靠得近、会互相干扰，就连一条边，边权=干扰耦合强度（距离越近权越大）；可用的信道就是"颜色"。给每个节点分一个颜色、让相邻同色的边权总和最小——这就是加权图着色。它天然能写成 QUBO（二次无约束二元优化，即一个 `x^T Q x` 的二次型），而 QUBO 正是 QAOA 直接吃的输入。

**"NP-hard"**：图着色是经典 NP-hard。小图能暴力枚举 K^N 种分配，但 N 一上去就爆炸。

**关键钩子——"反复出现"**：这不是一次性优化。用户走动、基站开关、流量变化，干扰图每个快照都变一点，于是**同一族 QUBO 要反复求解**。这个"反复出现 + 相邻实例只差小扰动"的结构，就是暖启动 QAOA 的发力点。没有这个结构，暖启动没那么大用；有这个结构，暖启动才真正划算。**这一句是整个项目的论证核心**——先让听众相信这个结构真实存在，后面的暖启动才有支点。

### Solution —— 暖启动 QAOA 的机制（讲给量子听众）

**冷启动**：每个快照都从零开始重新优化所有变分参数 γ、β。这是 QAOA 最贵的部分——每个优化器迭代都要跑线路、采样、估期望，COBYLA 在外层调很多次参。

**暖启动 QAOA 做了什么**（这是量子算法层的修改，不是经典后处理）：
1. 把上一快照的 bitstring 解**松弛成连续振幅**——0/1 变成 [0,1] 的连续值。
2. 用这些连续振幅**制备一个非均匀初态**：朝旧 bitstring 偏置的相干叠加（ε 控制偏置强度）。
3. 同时把 **mixer 换成 warm-start mixer**（而非全均匀的 X mixer）。
4. 于是变分搜索**从旧解的盆地内起步**，而不是从均匀叠加起步。

**为什么省成本**：相邻快照的 QUBO 只差小扰动，旧解的盆地大概率仍覆盖新最优。从盆地内起步，COBYLA 需要的迭代数大幅减少 / 或在相同迭代预算下得到更接近最优的解。

**实测结论（已验证）**：我们跑出来的诚实结果是——**在固定的、偏紧的优化器预算下（maxiter=25），暖启动在 4/5 个移动快照上比冷启动更接近最优**，平均到最优的 gap 从冷启动的 0.44 降到暖启动的 0.15（降 66%）。这是 Egger et al. 暖启动 QAOA 的近似比优势，应用到扰动 QUBO 序列上。**路演里要这么讲，不要讲"迭代数更少"——那是过度声称；"相同预算下近似比更优"才是站得住的、且对 NISQ 更有意义的声称**（因为每次迭代在硬件上才贵）。

**技术栈**：Qiskit 的 `WarmStartQAOAOptimizer`，连续松弛用 `SlsqpOptimizer`（SciPy，无需 CPLEX/Gurobi），后端 Aer statevector 模拟器。

### 编码研究 —— 线路设计视角（技术深度亮点）

**为什么编码是 ansatz/线路设计决策**：同一个着色问题有两种自然的 QUBO 编码，它们决定了量子比特数和 cost Hamiltonian 的形状，直接影响线路深度。

**One-hot 编码**：
- 变量 `x[v,c]`，每个(节点,颜色)对一个二元变量 → **N·K 个量子比特**。
- 约束"每节点恰好一色"是线性的 `(Σ_c x[v,c] − 1)²`，penalty 项浅。
- 量子比特多，但 cost 项简单、线路浅。

**二进制编码**：
- 用 `⌈log₂K⌉` 个比特表示节点颜色索引 → **N·⌈log₂K⌉ 个量子比特**（K=4 时只要 2 比特/节点 vs one-hot 的 4）。
- "每节点一色"对合法 bitstring 自动满足，但 `⌈log₂K⌉` 比特空间里有 ≥K 的非法索引，要加 penalty。
- 同色判定 `1[ch(u)==ch(v)]` 展开成比特的多线性多项式 → **cost Hamiltonian 更稠密、更深**，可行子空间更小。

**实测结论（已验证）**：在我们的编码研究表里——
- **量子比特**：binary 大幅省比特。例 N10_K4：one-hot 40 → binary 20（省一半）；N8_K5：40 → 24。
- **深度**：小 K 时 one-hot 更浅（N8_K3：78 vs 90），但不是单调——N10_K4 时 binary 反而更浅（114 vs 129）。**这个非单调的权衡正是值得讲的诚实细节**。
- **可行性**：one-hot 在 32+ 量子比特时模拟器已跑不稳，binary 仍 100% 可行——binary 在更大规模上"能跑"本身就是优势。

**价值**：这是一个**可迁移的编码选择规则**，不只对这个问题——任何"把离散选择编码进 QUBO"的网络类问题（路由、调度、分配）都能复用这个 qubit-vs-depth-vs-可行率的权衡框架。

### Unique Value —— 量子视角的价值主张

**贡献不是"QAOA 解了一个着色问题"**（那只是教科书应用）。贡献是**两个量子算法层面的结果**：
1. **暖启动 QAOA 作为动态 QUBO 的低成本增量优化器**——削减 QAOA 最昂贵的开销（变分参数搜索），对应真实的结构特征（相邻快照小扰动），给"相同预算下更优近似比"。
2. **最小量子比特 ansatz 的编码选择规则**——one-hot vs binary 的 qubit/深度/可行率权衡。

**两者都是量子算法层面的结果，恰好落在通信问题上**——这是它契合黑客松主题的方式。

### 必须主动承认的边界（对量子听众硬吹反而掉分）

- **暖启动 QAOA 是 Egger et al. 已有技术**。我们的新颖性**不是发明它**，而是**把它用到网络 dynamic/recurring QUBO regime + 配编码研究**。主动承认这点本身就是技术深度信号。
- **模拟器研究，非真实硬件**，核心 demo 无噪声模型；"QAOA + 噪声"作为未来工作。
- **QAOA 深度受模拟器开销限制**，报告质量饱和时的深度，不硬撑大规模。
- **λ 惩罚靠经验调参**；暖启动价值体现在近似比/迭代，非渐近加速。

### 应用价值（一句话回评委"so what"）

密集部署中，每信道服务更多用户（更小的同道干扰 = 更高空间复用），并有一条可信的量子扩展路径（编码压缩量子比特、暖启动压缩迭代，两者都是面向 NISQ 资源约束的设计）。
