# Algorithmic-Discrimination-Proof-Ladder
A simulation system based on counterfactual causal inference to verify the burden of proof allocation in algorithmic discrimination litigation.
# Algorithmic-Discrimination-Proof-Ladder
# 算法歧视诉讼举证责任分配模拟系统

This repository contains the simulation system for the undergraduate thesis: **"The Dilemma and Resolution of Burden of Proof Allocation in Algorithmic Discrimination Litigation: A Perspective Based on Counterfactual Causal Inference."**

本项目是毕业论文《算法歧视诉讼中举证责任分配的困境与出路——基于“反事实因果推断”视角》的配套模拟实验工具。

---
> **This project formalizes legal burden-shifting rules into a rigorous causal inference model.** > **本项目将法律上的举证责任分配规则形式化为严谨的因果推断模型。**

## 📖 Project Overview | 项目概览

Algorithmic discrimination presents a "Black Box" challenge in judicial proceedings, making it nearly impossible for plaintiffs to meet the traditional burden of proof. This project implements a **"Three-Tiered Burden of Proof Rule"** to bridge the gap between legal requirements and technical feasibility through counterfactual analysis.

算法歧视在司法程序中面临“黑箱”挑战，导致原告难以履行证明义务。本项目通过反事实分析，构建了一套衔接法律需求与技术可行性的“三阶梯举证责任规则”。

---

## ⚖️ The Three-Tiered Rule | 三阶梯证明规则实证

This system simulates the shifting of the burden of proof in judicial proceedings across two typical algorithmic scenarios:
本系统通过两个典型司法场景模拟举证责任的流转过程：

### Case 1: Hiring Algorithm Discrimination (Based on UCI Adult Dataset)
### 场景一：招聘算法歧视 (基于 UCI 真实数据)

* **Phase 1: Prima Facie Case (第一阶梯：初步举证)**
    Calculates the Disparate Impact (DI) ratio. Empirical results show $DI=0.35$ (Female approval rate is only 35% of males), triggering the shifting of the burden of proof.
    计算 DI 系数。实证显示 $DI=0.35$（女性获准率仅为男性 35%），达到“初步证明”标准，触发举证责任转移。

* **Phase 2: Technical Rebuttal & Causal Isolation (第二阶梯：技术反证与因果剥离)**
    Utilizes counterfactual intervention to strip away neutral features such as education, age, and working hours.
    利用反事实干预，剥离教育、年龄、工时等中性特征的影响。

* **Empirical Conclusion (实证结论)**: 
    Detected a **8.53%** net gender-based causal bias.
    精准检测出 **8.53%** 的纯性别因果偏见。

* **Judicial Verdict (判定结论)**: 
    The bias rate exceeds the 5% legal threshold; therefore, the platform failed its rebuttal, and algorithmic discrimination is legally established.
    偏见率超过 5% 的法定门槛，判定平台反证失败，构成法律意义上的歧视。



---

### Case 2: Dynamic Pricing / "Big Data Price Gouging" (Based on Regression Analysis)
### 场景二：大数据杀熟 (基于回归分析)

* **Proof Logic (证明逻辑)**: 
    Fix the "Urgency of Demand" and only modify the "User Identity" (New vs. Old) for price back-testing.
    固定“需求紧急度”，仅改变“用户身份”进行价格回测，实现“同等需求、不同身份”的对照。

* **Experimental Comparison (实验对比)**:
    * **Price Gouging Exists (存在加价时)**: 100% of orders showed identity-based premiums; Plaintiff wins.
        检测到 100% 的订单存在纯身份溢价，判定原告胜诉。
    * **Normal Volatility (正常波动时)**: The price gap is below the 5% legal threshold; the system automatically filters out frivolous litigation.
        差价低于 5% 法律门槛，系统自动拦截滥诉，判定驳回起诉。
---

## 🛠️ Technical Features | 技术特性

- **Cross-Scenario Validation (多场景验证)**: Supports both Hiring Discrimination (Classification) and "Big Data Price Skimming" (Regression).
- **Causal Robustness (因果稳健性)**: Implements batch counterfactual testing to provide statistical confidence levels for legal evidence.
- **Model-Agnostic (模型无关性)**: The proof logic can be applied to various "Black Box" algorithms.

---
## 🚀 快速开始 (Quick Start)
### Prerequisites | 环境要求
- Python 3.8+
- Scikit-learn, Pandas, NumPy

只需几行代码，即可对您的数据集进行初步的公平性体检：

```python
from adpl import FairLadder
from adpl.datasets import load_adult_data

# 1. 加载示例数据（或导入您自己的 DataFrame）
data, target, sensitive_attr = load_adult_data()

# 2. 初始化“证明阶梯”，设定检测等级为：统计公平 (L1)
ladder = FairLadder(level="Statistical")

# 3. 执行偏见检测
report = ladder.check_bias(data, target, sensitive_feature=sensitive_attr)

# 4. 打印可视化报告
report.print_summary()
```
---
## 📊 Experimental Results | 实验结果验证

The following table summarizes the performance of the **Three-Tiered Proof Rule** using real-world census data and parameterized pricing models.
下表展示了“三阶梯证明规则”在真实人口普查数据及参数化定价模型下的实证表现。

| Case Scenario (实证场景) | Phase 1: DI Ratio (第一阶梯统计) | Phase 2: Causal Rate (第二阶梯因果率) | Final Verdict (最终裁判) |
| :--- | :--- | :--- | :--- |
| **Hiring (UCI Adult Data)** | **0.3597** (显著差异) | **8.53%** | **Guilty (构成性别歧视)** |
| **Pricing (Bias=15.0)** | 1.1772 (触发阈值) | **100.00%** | **Guilty (构成杀熟歧视)** |
| **Pricing (Bias=1.0)** | 1.0341 (正常波动) | N/A (第一阶梯拦截) | **Dismissed (驳回起诉)** |

### 📈 Result Analysis | 结果分析

- **Evidence Transformation (从统计到因果)**: 
  - In the **UCI Adult** case, while the statistical gap was huge (DI=0.36), the counterfactual test isolated the **8.53%** net causal effect of gender. This proves the system's ability to strip away neutral factors like education and hours-per-week.
  - 在 **UCI Adult** 实证中，尽管统计差异巨大（DI仅为0.36），但反事实检验精准剥离出 **8.53%** 的纯性别因果贡献。这证明了系统能够排除教育、工时等中性因素，锁定核心因果歧视。

- **Precision vs. Frivolity (精准性与防滥诉)**:
  - The system successfully blocked the "Pricing (Bias=1.0)" case at Phase 1 because the 3.4% price gap was within the legal tolerance (5%). This protects algorithmic innovation from frivolous litigation.
  - 系统成功在第一阶梯拦截了“偏见=1.0”的定价案例，因为其价差处于法律容忍范围（5%），有效防止了针对正常商业波动的滥诉，保护了算法定价的合理创新空间。

- **Causal Determination (因果判定能力)**:
  - In the personalized pricing scenario (Bias=15.0), the **100% group bias rate** reveals that the platform's excuse of "urgency" was a mere pretext for identity-based price gouging.
  - 在大数据杀熟场景中，**100% 的群体偏见率** 穿透了平台以“需求紧急度”为幌子的抗辩，证明在相同需求背景下，价格上涨纯粹基于老用户身份。

- **Robustness (稳健性)**:
  - The system maintains high accuracy even with random noise, ensuring the reliability of the "Technical Verification Report" for judicial use.
  - 系统在存在随机噪声的情况下依然保持高度准确，确保了生成《技术验证报告》的司法可靠性。
 ---

## 🗺️ 证明阶梯：公平性理论地图 (Theory Map)

ADPL 框架将公平性标准抽象为四个递进的层级。开发者可以根据业务的风险等级（Risk Level）和数据复杂度选择合适的证明深度。

| 阶梯层级 (Level) | 核心指标 (Key Metrics) | 适用场景 | 局限性 | 决策建议 |
| :--- | :--- | :--- | :--- | :--- |
| **L1: 统计公平** | $DP$ (Demographic Parity) | 宏观合规性初筛、法律强监管 | 忽略个体差异，可能导致“反向歧视” | 当社会价值导向（如多元化配额）大于个体准确率时使用 |
| **L2: 条件公平** | $EO$ (Equal Opportunity) | 信贷审批、绩效考核、医疗筛查 | 依赖标签准确性，无法检测隐含偏见 | 适用于追求“同等能力、同等机会”的专业选拔场景 |
| **L3: 个体公平** | $L-Lipschitz$ Continuity | 法律判决、高度个性化服务 | 相似度度量（Similarity Metric）定义较为主观 | 适用于需要确保“相似的人得到相似处理”的精细化决策 |
| **L4: 反事实公平** | $Causal\ Effect\ (\tau)$ | 高风险 AI 决策、医疗诊断、因果追溯 | 计算开销大，需构建复杂的因果图 (DAG) | **最高安全等级**。用于必须证明“若敏感属性改变，决策仍不变”的场景 |



### ⚖️ 公平性与准确率的权衡 (Trade-off)

在实际应用中，攀登“公平阶梯”往往伴随着模型性能的微调。ADPL 旨在帮助开发者找到 **Pareto 最优解**。



> **提示：** 随着阶梯等级的提高（从 L1 到 L4），算法对偏见的消除越彻底，但对数据质量和先验知识（如因果关系）的要求也随之增加。

---
### Installation & Execution | 安装与运行
```bash
# Clone the repository | 克隆仓库
git clone [https://github.com/](https://github.com/)[Your-Username]/Algorithmic-Discrimination-Proof-Ladder.git

# Install dependencies | 安装依赖
pip install -r requirements.txt

# Run the simulation | 运行模拟
python src/main_simulation.py





