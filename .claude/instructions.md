# HorizonBench 项目指令

## 核心工作流程

### LaTeX 编译规则
**重要：每一次对 main.tex 进行修改之后，都必须进行编译**

编译命令序列：
```bash
# 完整编译流程
pdflatex main.tex
bibtex main
pdflatex main.tex  
pdflatex main.tex
```

或者使用 latexmk（如果可用）：
```bash
latexmk -pdf main.tex
```

### 验证步骤
1. 检查编译是否成功（无错误）
2. 确认 main.pdf 已更新
3. 检查参考文献是否正确显示
4. 验证图表编号和引用是否正确

### 项目结构
- `main.tex` - 主文档
- `appendix.tex` - 附录
- `main.bib` - 参考文献
- `Fig/` - 图片目录
- `draft/` - 草稿和辅助文件

### 编译注意事项
- 确保所有图片文件存在且路径正确
- 修改参考文献后需要完整的编译流程
- 检查 .log 文件中的警告信息
- 保持 .aux、.bbl 等辅助文件同步

---

## Draft内容提取与合并规则

### 处理Part*草稿内容的标准流程

当处理形如`draft/PartA/`、`draft/PartB/`、`draft/PartC/`等任何Part*目录的内容时，必须遵循以下规则：

#### 1. 内容提取原则
- **系统性扫描**: 完整扫描draft目录下的所有.tex文件、.bib文件和图片资源
- **内容分类**: 按照论文结构（Introduction, Literature Review, Method等）分类提取内容
- **引用完整性**: 确保所有\cite{}引用都有对应的bib条目

#### 2. 图片资源管理
- **命名规范化**: 将draft中的图片重命名为统一格式（如`partA_fig1.pdf` → `system_overview.pdf`，`partB_fig1.pdf` → `literature_evolution.pdf`）
- **路径统一**: 所有图片移动到主目录的`Fig/`文件夹
- **引用更新**: 更新所有\includegraphics{}路径为新的统一路径
- **格式检查**: 确保图片格式符合LaTeX要求（首选.pdf，.png作为备选）
- **Part标识**: 在图片命名中体现来源Part，便于追踪和管理

#### 3. 参考文献合并
- **去重检查**: 检查main.bib中是否已存在相同的引用条目
- **格式统一**: 确保bib条目格式符合项目标准
- **分类标记**: 使用注释标记引用来源（如% === PartA Introduction ===、% === PartB Literature Review ===、% === PartC Method ===）
- **依赖验证**: 确保所有tex文件中的\cite{}在合并后的bib文件中都能找到

#### 4. 内容整合流程
```bash
# 标准操作序列：
1. 备份现有main.tex和main.bib
2. 扫描指定Part*目录，创建整合计划
3. 识别Part对应的论文章节（PartA→Introduction, PartB→Literature Review, PartC→Method等）
4. 复制并重命名图片资源到Fig/目录
5. 合并bib文件，处理重复条目并添加Part标识注释
6. 将tex内容按章节插入main.tex对应位置
7. 更新所有图片和引用路径
8. 完整编译验证
9. 检查所有引用是否正确显示
```

#### 5. 质量检查清单
- [ ] 所有图片文件已正确移动并重命名
- [ ] 所有\includegraphics路径已更新
- [ ] 所有\cite引用在main.bib中存在对应条目
- [ ] 无重复的bib条目
- [ ] 编译无错误和警告
- [ ] 图表编号连续且正确
- [ ] 参考文献列表完整显示

#### 6. 错误处理
- **缺失图片**: 立即报告并要求用户提供
- **重复引用**: 采用更完整的bib条目，删除冗余
- **路径错误**: 系统性检查和修正所有相对路径
- **编译失败**: 逐步回退，定位问题源头

### 重要提醒
- 每次内容合并后必须进行完整编译
- 保持draft原文件不变，所有修改在main文件中进行
- 合并过程中如发现冲突，优先咨询用户决策
- 记录所有文件变更，便于问题排查

### Part*目录常见映射关系
| Part目录 | 对应章节 | 典型内容 |
|----------|----------|----------|
| `PartA` | Introduction, Abstract | 引言、摘要、动机 |
| `PartB` | Literature Review, Related Work | 文献综述、相关工作 |
| `PartC` | Method, Methodology | 系统设计、方法论 |
| `PartD` | Evaluation, Experiments | 实验设计、评估计划 |
| `PartE` | Conclusion, Future Work | 结论、伦理考量、时间线 |

**注意**: 具体映射关系以项目实际结构和用户指示为准