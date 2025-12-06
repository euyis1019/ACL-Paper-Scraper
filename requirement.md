# JC4003 NLP 小组项目 - 知识库

## 📋 项目基本信息

| 项目             | 详情                                                         |
| ---------------- | ------------------------------------------------------------ |
| **课程**         | JC4003: Natural Language Processing                          |
| **任务**         | 设计一个基于LLM的学术论文自动评分与反馈系统（Design Report） |
| **完成方式**     | 单人完成                                                     |
| **报告模板**     | NeurIPS 格式                                                 |
| **参考文献格式** | 不需要特别考虑                                               |
| **页数限制**     | 无硬性限制（建议约 12-14 页正文）                            |
| **截止日期**     | 2025年12月12日 22:00 (UTC+8)                                 |
| **权重**         | 占期末成绩 25%                                               |
| **提交形式**     | 单个 PDF 文档，通过 Blackboard 提交                          |

---

## 📊 报告结构与分值

| 部分                          | 内容                      | 权重 | 篇幅建议      |
| ----------------------------- | ------------------------- | ---- | ------------- |
| **Part A: The Vision**        | 摘要 + 引言与动机         | 15%  | ~250词 + ~1页 |
| **Part B: The Foundation**    | 文献综述                  | 25%  | 2-3页         |
| **Part C: The Blueprint**     | 系统架构与设计（核心）    | 30%  | 4-5页         |
| **Part D: The Validation**    | 创新点 + 评估计划         | 20%  | ~1页 + 2页    |
| **Part E: The Reality Check** | 伦理考量、局限性 + 时间线 | 10%  | ~1页 + 甘特图 |

---

## 📂 数据策略

### 数据来源
- **系统输入数据**: ACL Anthology 论文（PDF格式）
- **不限定特定 Track**，与 NLP/学术论文评审相关即可

### 训练/评估数据
- **PeerRead Dataset**
  - 来源: Allen AI (allenai)
  - GitHub: https://github.com/allenai/PeerRead
  - HuggingFace: https://huggingface.co/datasets/allenai/peer_read
  - 内容:
    - 14.7K 论文草稿 + accept/reject 决定
    - 10.7K 专家评审文本
    - 涵盖会议: ACL, NIPS, ICLR
    - 评分维度: originality, impact, clarity, soundness 等

### 数据使用方案
```
系统输入数据：ACL Anthology 论文 (PDF)
Few-Shot 示例：PeerRead 中的高质量评审示例（评分 + 评审文本）
评估/验证数据：PeerRead Dataset (ACL 子集)
```

---

## 🤖 核心模型选型

| 项目           | 决定                             |
| -------------- | -------------------------------- |
| **模型选择**   | GPT-4、Claude、DeepSeek 最新模型 |
| **使用方式**   | 通过 API 调用                    |
| **交互策略**   | Few-shot prompting（待最终确认） |
| **多模型策略** | 待确定（并行评估/投票/验证）     |

---

## 📐 评分 Rubric 设计

### 设计理念
- **分层结构**: 第一层为完全正交的核心维度，第二层为细粒度子指标
- **正交性原则**: 第一层各维度独立评分，互不影响

### 第一层：正交核心维度（4个）

| 维度                       | 核心关注点   | 与其他维度的区分               |
| -------------------------- | ------------ | ------------------------------ |
| **Technical Quality**      | 方法对不对   | 不管写得好不好、不管是否新颖   |
| **Novelty & Contribution** | 想法新不新   | 不管方法是否完美、不管表达如何 |
| **Clarity & Presentation** | 表达清不清   | 不管内容本身对错、不管是否创新 |
| **Soundness & Validity**   | 结论可不可信 | 不管方法多复杂、不管表达多优美 |

### 第二层：细粒度子指标

#### 1. Technical Quality（技术质量）
- Methodology rigor（方法论严谨性）
- Experimental design（实验设计）
- Reproducibility（可复现性）

#### 2. Novelty & Contribution（创新与贡献）
- Originality of ideas（想法原创性）
- Significance of contribution（贡献重要性）
- Potential impact（潜在影响力）

#### 3. Clarity & Presentation（清晰度与表达）
- Writing quality（写作质量）
- Organization & structure（组织与结构）
- Figures & tables quality（图表质量）

#### 4. Soundness & Validity（可靠性与有效性）
- Correctness of claims（论断正确性）
- Adequacy of evidence（证据充分性）
- Limitation acknowledgment（局限性认知）

---

## 🏗️ 系统架构思路（待细化）
```
输入阶段:
  PDF 论文 → PDF解析 → 结构化文本（Markdown/JSON）

处理阶段:
  结构化文本 → 分段提取（Abstract, Method, Results...）
              → 多模型并行评估（GPT-4 / Claude / DeepSeek）
              → 评分聚合 & 一致性检查

输出阶段:
  → 量化评分（4个正交维度 + 细粒度子指标）
  → 文本反馈（每个维度的优缺点分析）
  → 可视化报告（Dashboard）
```

---

## 📚 参考资源

### 参考论文
- **AutoPeer** (Group 6): LLM-Powered Scoring and Feedback System for Academic Papers
  - 使用 DeepSeek-V3.2-Exp + Few-Shot Prompting
  - 四维度评分: Research Methodology, Innovation, Conclusion, Language

### 关键数据集
- **PeerRead**: https://github.com/allenai/PeerRead
- **ACL Anthology**: https://aclanthology.org/

### 待搜索的文献方向
- Automated Essay Scoring (AES)
- LLM-based paper review
- Peer review automation
- Multi-dimensional text evaluation

---

## ⏳ 待确定事项

- [ ] 多模型策略：并行评估/投票/验证？
- [ ] 交互策略最终确认：Few-shot prompting
- [ ] 系统架构图（Mermaid）
- [ ] 文献综述框架
- [ ] Prompt 设计细节
- [ ] 评估指标与实验设计
- [ ] UI 草图设计
- [ ] 甘特图/时间线

---

*最后更新: 2025年12月6日*