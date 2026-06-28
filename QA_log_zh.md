# 项目 QA 整理

> 本文件整理了在确定与推进本项目（面向密集小蜂窝网络的量子增强频谱分配）过程中，团队与我之间的关键问答。这些问题直接塑造了最终方案。按主题归类。

---

## Q1：团队背景 / 平台 / 方向如何定？

**Q：你们团队整体技术背景怎样？这决定了"容易实现"的边界。**
**A：本科+研究生混合。** → 方案需偏向可快速上手的模拟器 demo，但可承担中等复杂度的混合方案。

**Q：计划用哪种量子计算平台/硬件？**
**A：Qiskit + 模拟器。** → Hack Ingredients 固定为 Qiskit + qiskit-aer statevector；不依赖真实硬件排队，2 天内能出 demo。

**Q：在符合主题的方向里倾向哪一个？**
**A：QAOA 网络资源分配。** → 出自项目想法列表"面向网络资源分配的量子优化"。QUBO 建模清晰、Qiskit 有现成构建块、混合团队 2 天可落地，同时能展技术深度。

---

## Q2：三个具体问题里选哪个？创新点怎么定？

**Q：三个具体问题（A 频谱分配+暖启动 / B 关联+负载均衡 / C 链路调度）选哪个？**
**A：A 频谱分配+暖启动。** → 核心简单（图着色 QUBO）、有创新点（暖启动）、价值故事清晰（6G 频谱效率）。B 的 QUBO 不够干净、调参难；C 创新性低、6G 故事弱。

**Q：创新点怎么定（暖启动 / 编码权衡 / 两者都要）？**
**A：两者都要。** → 暖启动做主动算法贡献（拿创新分），编码权衡做配套资源感知实现（拿技术深度分）。两者耦合：暖启动定义算法，编码定义其资源感知实现。

---

## Q3：Demo 规模与路演语言？

**Q：Demo 干扰图规模定多大？**
**A：小规模 + 一个中规模点。** → 小规模（6-10 基站）现场能跑通；中规模点（15-25 基站）撑可扩展性故事。兼顾现场可行性可扩展性论证。

**Q：路演用什么语言？**
**A：英文为主 + 中文对照。** → ISIT 国际会场，英文覆盖更广；中文对照备稿/答辩用。

---

## Q4：为什么创新点锚在暖启动？（论证核心）

**核心回答（量子视角的硬理由）：**

1. **打在 QAOA 真正的痛点上**：QAOA 最贵的是变分参数优化（每 step 跑线路、采样、估期望），冷启动每快照付全价。暖启动直接削减这个最贵的部分。

2. **量子原生，非经典后处理**：暖启动改的是初态制备（非均匀叠加，朝旧 bitstring 偏置）和 mixer（warm-start mixer）——是 ansatz/线路层的修改，正经的量子算法设计。对量子听众，"改 ansatz 比改后处理"高一个段位。

3. **对应真实结构特征**："相邻快照只差小扰动"是 recurring QUBO 的真实性质，暖启动是"实例间相关"的天然算法回应——不是硬造新颖性。对"这真有用吗"的追问：当 `||Q_t − Q_{t-1}||` 小时，旧解盆地大概率覆盖新最优，省的迭代可量化。

4. **给得出可画、可守的结论**：度量是 objective-vs-iteration 曲线 / 重收敛迭代数 / 固定预算下近似比。2 天黑客松里，能在图上画出、能当面复现的结论，比宏大但证不了的声明强。

5. **编码权衡为何是配角**：编码研究撑技术深度但故事性弱；暖启动是主动算法贡献，编码是配套。主创新放主动贡献、配套放编码是更强的组合。

6. **必须主动承认的边界**：warm-start QAOA 是 Egger et al. 已有技术。新颖性**不是发明它**，而是**把它用到网络 dynamic/recurring QUBO regime + 配编码研究**。主动承认本身就是技术深度信号。

---

## Q5：幻灯片格式与受众视角？

**Q（反馈）：幻灯片其实是一页的，字数不要太多；听众里有不少搞量子计算的，我自己也做量子计算，希望整个项目更从量子计算视角出发。**
**A：** → 重写为极简单页短句版（每段 1-2 句）；视角从量子算法/线路出发，通信问题只一句动机带过；不再科普 QAOA 基本原理，直接讲暖启动机制与编码线路设计。产出 `Napkin_Pitch_ShortSlides_zh.md`（英文短句 + 中文翻译 + 详细解释）。

---

## Q6：实测后对 pitch 声称的修正（诚实性）

**情况**：初版 pitch 写"暖启动以远少于冷启动的迭代数收敛"。实测发现：单快照下冷/暖迭代数接近（150 vs 155），暖启动的真正优势是**在固定紧预算下近似比更优**（4/5 快照更近最优，mean gap 0.15 vs 0.44）。

**修正**：把声称改为"在固定 QAOA 迭代预算下达到近最优质量，远优于冷重启"——这是 Egger et al. 的近似比结果，站得住且对 NISQ 更有意义（每次迭代在硬件上才贵）。同步更新了 `Napkin_Pitch.md` 的方案/价值/进展/讲稿与中文对照。

**为什么不能讲"迭代数更少"**：那是过度声称，实测不支持。对量子听众讲一个证不了的声称会掉可信度。"相同预算下更优近似比"才是真且强的声称。

---

## Q7：技术栈集成中遇到的真实坑

**问题**：Qiskit 2.4.2 + qiskit-algorithms 0.4.0 + qiskit-aer 0.17.2 组合下，QAOA + 暖启动要跑通需三个非显然配置：

1. **必须用 V2 sampler**：`qiskit_algorithms.QAOA` 要求 `BaseSamplerV2`，用 `qiskit_aer.primitives.SamplerV2`（不是 V1，也不是 BackendEstimatorV2）。
2. **必须传 transpiler 给 QAOA**：Aer 的 SamplerV2 不自动 transpile，否则报 `AerError: unknown instruction: QAOA`。需 `QAOA(transpiler=generate_preset_pass_manager(...))`。且为避免目标宽度限制，用 basis_gates 而非 backend target。
3. **暖启动 pre_solver 必须是连续求解器**：`MinimumEigenOptimizer` 不能解连续松弛（报 "Continuous variables are not supported"），用 `SlsqpOptimizer`。
4. **`GraphColoring` 在 qiskit-optimization 0.7 中不存在**（有 Maxcut/VertexCover/Tsp 等但无着色）→ 手写 `QuadraticProgram` 构建着色 QUBO，这也正是暴露 one-hot/binary 编码切换的机会。
5. **`MinimumEigenOptimizer` 的结果打包在该版本组合下会 IndexError**（优化本身没问题，只是脆弱的样本索引层）→ 直接调 `QAOA.compute_minimum_eigenvalue` 并自己解码 `best_measurement`，绕开脆弱层。

这些都已写进记忆 `qiskit-stack-integration-gotchas.md`，避免重新踩坑。

---

## Q8：要"uv 安装"且"python3.12"

**Q：用 uv 安装；python3.12。**
**A：** → `uv venv --python 3.12`，`uv pip install qiskit qiskit-optimization qiskit-aer networkx numpy scipy matplotlib ipykernel`，另装 `qiskit-algorithms`（独立包）。环境已就绪，所有模块在 `.venv` 下验证通过。

---

## Q9：Egger et al. 暖启动 QAOA 的引用与链接

**情况**：评委/听众里有量子计算同行，warm-start QAOA 是已有技术，必须在路演和答辩里主动承认并正确引用。

**核心论文**：

**[1] D.J. Egger, J. Mareček, S. Woerner, "Warm-starting quantum optimization," _Quantum_, vol. 5, p. 479, June 2021.**
- DOI: <https://doi.org/10.22331/q-2021-06-17-479>
- arXiv: <https://arxiv.org/abs/2009.10095>

**论文关键内容（与我们直接相关的）**：
- 把经典连续松弛的最优解映射为一个非均匀初态（参数 ε 控制到松弛解的距离）
- 同时构造对应的 warm-start mixer（替换标准 X mixer）
- 数值实验：暖启动 QAOA 在固定 p 层下**近似比优于冷启动**，低 p 时优势尤其显著
- 这正是我们 dynamics 里测到的现象：固定 maxiter=25 下暖启动近似比更优（mean gap 0.04 vs 0.20）

**路演/答辩里正确的引用方式**：
> "Warm-start QAOA was introduced by Egger, Mareček, and Woerner (Quantum, 2021). Our contribution is NOT inventing the technique — it's applying it to the *dynamic/recurring QUBO regime in networking* and pairing it with an encoding study that makes the ansatz resource-aware."

**不能做的事**：把暖启动 QAOA 当成自己的发明来吹。对知道这个技术的量子听众硬吹会掉信任分。主动承认本身是技术深度信号。

---

## Q10：信道分配为什么是加权图着色？快照是什么？"攻"这个词？

### 为什么是加权图着色

用具体例子说明：**5 个小蜂窝（A,B,C,D,E），3 个可用信道（红、绿、蓝）**。

```
      cell_B──w=0.9──cell_C
        |   \        /
      w=0.7  w=0.3 / w=0.5
        |      \  /
      cell_A──cell_D──cell_E
              w=0.8  w=0.4
```

- **节点** = 小蜂窝
- **边** = 两个蜂窝靠得足够近，用同一个信道会互相干扰
- **边权 w** = 干扰耦合强度（靠得越近 w 越大，用同信道时惩罚越重）
- **颜色** = 可用信道（3 信道 = 3 颜色）
- **优化目标**：不是传统 k-着色（"相邻不许同色"），而是**加权着色优化**——允许同色，但同色就把对应的 w 计入总干扰，我们去最小化这个总干扰

**为什么天然是 QUBO？** 对每条边 (u,v) 有干扰权 w_uv。如果 u 和 v 都被分到色 c，x[u,c]·x[v,c] = 1，惩罚 w_uv 被激活。整个目标 `Σ w_uv · Σ_c x[u,c]·x[v,c]` 全是二次二元项——直接就是 QUBO，不需要转换。

### "快照"是什么

**快照 (snapshot) = 干扰图在某个时刻的"一帧照片"**。
- 时刻 t=0：用户/基站在各自位置 → 特定干扰图 G_0 → 求解 QUBO_0
- 时刻 t=1：用户走动、基站开关 → 干扰图变成 G_1（基本结构相同，但边/权有局部扰动）→ 求解 QUBO_1
- 时刻 t=2：G_2 ……

连续两帧 QUBO 只差一个小扰动——这就是"反复出现 + 相邻实例相关"的结构，是暖启动的发力点。

### 关于"攻"这个词

你指出"攻"太军事化，已替换。更新后的表述：
- 中文："削减"、"落在"、"对准"
- 英文："attacking" → 在工程语境里是中性常见的（"attack the problem/cost"），但如果也不喜欢可用 "address / cut / reduce the cost"

---

## Q11：One-hot 编码 vs 二进制编码 —— 具体例子

用 **N=3 基站、K=3 信道（红/绿/蓝）** 为例。

### One-hot 编码

每个 (节点, 信道) 对一个二元变量 x[v,c] ∈ {0,1}。
**量子比特数** = N × K = 3 × 3 = **9**。

**解 "A=红, B=绿, C=红"** 的 bitstring：
```
x[A,红]=1  x[A,绿]=0  x[A,蓝]=0   ← 恰好一个 1（"每节点恰好一色"）
x[B,红]=0  x[B,绿]=1  x[B,蓝]=0
x[C,红]=1  x[C,绿]=0  x[C,蓝]=0
```
约束惩罚：`λ · Σ_v (Σ_c x[v,c] − 1)²`，展开为 `λ(Σ x² − 2Σ x + 1)`，标准二次 penalty。**特点：qubit 多、约束浅、线路浅。**

### 二进制编码

信道索引用 ⌈log₂K⌉ = ⌈log₂3⌉ = **2 比特/节点** 表示。
**量子比特数** = N × ⌈log₂K⌉ = 3 × 2 = **6**（省 3 个）。

**编码方案**：bit[v,0]·2⁰ + bit[v,1]·2¹
```
00(0)→红    01(1)→绿    10(2)→蓝    11(3)→非法！
```

**同一解** 编码为：
```
bit[A,0]=0  bit[A,1]=0   → 00 → 0=红 ✓
bit[B,0]=1  bit[B,1]=0   → 01 → 1=绿 ✓
bit[C,0]=0  bit[C,1]=0   → 00 → 0=红 ✓
```
非法值惩罚：`1[ch(v) ≥ 3]` = `bit[v,0]·bit[v,1]`（对 K=3 恰好是单个乘积项）。同色判定 `1[ch(u)==ch(v)]` 展开成比特乘积的多线性展开（如 `(1−b0−c0+2b0c0)(1−b1−c1+2b1c1)`）→ **cost Hamiltonian 更稠密/更深。**

### 对比表

| | One-hot | 二进制 |
|---|---|---|
| N=3, K=3 | 9 qubits | 6 qubits |
| N=10, K=4 | 40 qubits | 20 qubits |
| N=8, K=5 | 40 qubits | 24 qubits |
| 约束 | `(Σ_c x−1)²`，浅 | `1[ch≥K]`，比特乘积 |
| Cost | `w·x·y`，简单二次 | `1[ch==ch]`，多线性展开 |
| 线路深度 | 浅 | 深（更多 CX） |

---

## Q12：Qiskit QAOA 能不能用 GPU？你用了没有？

**没有用 GPU。** 当前项目用的是 Aer **CPU** statevector 模拟器，没启用 GPU 加速。

**能不能用？能。**

Aer 原生支持 GPU，装 `qiskit-aer-gpu` 后指定 device：

```bash
uv add qiskit-aer-gpu
```

```python
from qiskit_aer import AerSimulator
sim = AerSimulator(method='statevector', device='GPU')
# 大规模电路可用 method='tensor_network', device='GPU'
```

**当前项目为什么不加 GPU？**

当前 demo 的最大电路是 28 qubits（中规模图、二进制编码）。28 qubits statevector = 2²⁸ 复数 ≈ **4 GB RAM**，完全在主机 RAM 内，CPU 模拟器跑得动。加 GPU 不会显著加速反而引入 CUDA 依赖——对黑客松来说是过度工程化。

**评委如果问"为什么没用 GPU"**，标准回答：

> "Our largest demo circuit is 28 qubits — the statevector fits in standard laptop RAM. For bigger circuits we'd transition to GPU, which Aer supports natively. We include that as the 'credible quantum path to scale' in our value proposition."

这恰好是**可行性**评分项希望你展示的：知道工具的上限，选择适度的方案，给出合理的扩展路径。需要加 GPU 的时候（~35+ qubits），Aer 直接 `device='GPU'` 就能切过去。
