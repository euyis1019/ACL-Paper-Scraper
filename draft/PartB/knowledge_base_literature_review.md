# HorizonBench 项目知识库 - 文献综述更新

> 最后更新: 2025年12月6日

---

## 七、文献综述总结 (Part B: The Foundation)

### 7.1 章节结构

| 小节 | 主题 | 关键内容 |
|------|------|----------|
| 3.1 | AES: From Feature Engineering to Deep Learning | PEG → e-rater → BiLSTM/CNN → BERT/Transformer |
| 3.2 | LLM-Based Automated Scholarly Paper Review | ReviewMT, OpenReviewer, SEA, AGENTREVIEW |
| 3.3 | Multi-Agent Systems and Consensus | MARG, Agent collaboration, Meta-review |
| 3.4 | Benchmark Datasets and Evaluation | PeerRead, OpenReview, RAGBench, ARES |
| 3.5 | Research Gaps and HorizonBench Positioning | 5 个核心空白 + 我们的解决方案 |

---

### 7.2 核心引用文献

#### 7.2.1 自动作文评分 (AES)

| 引用 | 贡献 | 与我们的关系 |
|------|------|--------------|
| Page (1966) - PEG | 首个AES系统，表面特征 | 说明早期方法局限性 |
| Burstein et al. (1998) - e-rater | ETS系统，语法+词汇特征 | 手工特征的瓶颈 |
| Taghipour & Ng (2016) - BiLSTM | 深度学习首次应用于AES | 语义理解的进步 |
| Dong et al. (2017) - CNN+Attention | 局部语言模式捕获 | 注意力机制的引入 |
| Wang et al. (2022) - Multi-scale BERT | BERT用于AES的SOTA | Transformer时代 |
| Misgna et al. (2024) - Survey | 深度学习AES综述 | 指出反馈生成被忽视 |

#### 7.2.2 LLM 论文评审

| 引用 | 贡献 | 与我们的关系 |
|------|------|--------------|
| Tan et al. (2025) - ASPR Survey | LLM学术评审全面综述 | 领域全景图 |
| Zhou et al. (2024) - LLM Reliability | RR-MCQ基准，评估LLM可靠性 | >60%准确率，完全正确仅20% |
| OpenReviewer (2024) | 79K评审数据微调Llama | 专业化训练克服过度正面倾向 |
| SEA (2024) | 跨会议标准化评审 | 自我纠正策略 |
| AGENTREVIEW (2024) | LLM模拟同行评审动态 | 多因素可控实验 |

#### 7.2.3 多智能体系统

| 引用 | 贡献 | 与我们的关系 |
|------|------|--------------|
| D'Arcy et al. (2024) - MARG | 多Agent评审生成 | 通用评论60%→29%，好评论1.7→3.7 |
| Guo et al. (2024) - MAS Survey | LLM多Agent综述 | Agent profiling, 共识机制 |
| Duan et al. (2024) | 第三方LLM共识优化 | 不确定性估计减少幻觉 |

#### 7.2.4 基准数据集

| 引用 | 数据集 | 规模 | 用途 |
|------|--------|------|------|
| Kang et al. (2018) | PeerRead | 14.7K papers + 10.7K reviews | 奠基性数据集 |
| Ghosal et al. (2022) | Peer Review Analyze | 1,199 reviews, 17K sentences | 多层标注 |
| ORB (2023) | OpenReview-Based | 36K submissions, 89K reviews | 包含拒稿数据 |
| RAGBench (2024) | RAG评估 | 100K examples | RAG质量评估 |
| ARES (2024) | RAG评估框架 | - | 轻量化评估 |

---

### 7.3 五大研究空白与 HorizonBench 解决方案

| # | 研究空白 | 现有问题 | HorizonBench 解决方案 |
|---|----------|----------|----------------------|
| 1 | **Static vs. Dynamic Baselines** | 固定通用标准，不考虑领域差异 | Deep Research Agent 动态构建领域基准 |
| 2 | **Numerical Score Instability** | LLM数字输出不稳定，重复运行结果不同 | 等级制评分 (Strong Accept → Strong Reject) |
| 3 | **Single-Model Bias** | 单模型偏见和幻觉 | 异构多模型共识 (GPT/Claude/DeepSeek + Gemini Meta) |
| 4 | **Disconnect from Real Review** | 单次生成，无deliberation | 完整模拟 Reviewer → AC → Meta Review 流程 |
| 5 | **Limited Rejection Data** | 仅训练于接受论文，不知边界 | 整合 OpenReview 拒稿数据作为 Few-Shot |

---

### 7.4 关键论点与支撑证据

#### 论点1: LLM作为评审者尚不可靠

> **证据**: Zhou et al. (2024) 发现 LLM 在单选题上准确率 >60%，但完全正确仅约 20%。模型在长文档处理、零样本评分和批判性反馈方面仍然薄弱。

#### 论点2: 多Agent优于单Agent

> **证据**: MARG (D'Arcy et al., 2024) 通过多Agent将通用评论比例从60%降至29%，好评论数量翻倍 (1.7 → 3.7)。

#### 论点3: 专业化训练克服过度正面倾向

> **证据**: OpenReviewer 证明在 peer review 数据上的专业化训练可以克服 LLM 生成过度正面评估的倾向。

#### 论点4: 拒稿数据对理解边界至关重要

> **证据**: ORB数据集强调"负面和详细的反例对于研究论文内容、评审和最终决定之间的依赖关系非常有价值"。

---

### 7.5 与参考 Assessment (AutoPeer) 的差异化

| 维度 | AutoPeer 方法 | HorizonBench 创新 |
|------|--------------|-------------------|
| **基准构建** | 固定评分标准 | 动态检索领域前沿基准 |
| **评分方式** | 100分制数值 | 等级制 (7级) |
| **模型策略** | 单模型 (DeepSeek-V3.2-Exp) | 异构多模型共识 |
| **评审流程** | 单次评估 | 模拟完整 Reviewer → AC 流程 |
| **Few-Shot来源** | 未明确 | OpenReview 真实评审 (含拒稿) |
| **处理创新性** | 无特殊处理 | 检索稀少 = 高创新性 |

---

### 7.6 文献综述写作要点

#### 写作结构
1. **开篇**: 定位自动化论文评审的交叉学科性质
2. **历史脉络**: AES从特征工程到深度学习的演进
3. **当前前沿**: LLM-based ASPR的最新进展
4. **技术支撑**: 多Agent共识机制
5. **数据基础**: 基准数据集的发展
6. **研究空白**: 明确5个gap并阐述我们的定位

#### 引用策略
- **经典文献**: Page (1966), e-rater, BiLSTM, BERT
- **最新进展**: 2024年Survey和系统论文
- **直接相关**: MARG, AGENTREVIEW, OpenReviewer
- **数据集**: PeerRead, OpenReview, RAGBench

---

### 7.7 待补充内容

- [ ] 完整 BibTeX 条目核实
- [ ] 图表：AES技术演进时间线 (可选)
- [ ] 表格：方法对比表
- [ ] 与 NeurIPS 格式对齐

---

*文档更新结束*
