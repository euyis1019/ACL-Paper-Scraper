import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置学术风格
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# 定义任务数据
tasks = [
    # (任务名称, 开始周, 持续周数, 类别)
    ("Requirements & Tech Stack", 1, 1, "Planning"),
    ("Task Assignment", 1, 1, "Planning"),
    
    ("ACL Data Collection", 2, 1, "Phase 1"),
    ("PDF Parsing Pipeline (MinerU)", 2, 1.5, "Phase 1"),
    ("Paper Schema Design", 2, 1, "Phase 1"),
    
    ("Deep Research Agent", 3, 1.5, "Phase 2"),
    ("Semantic Scholar API", 3, 1, "Phase 2"),
    ("OpenReview Integration", 3, 1, "Phase 2"),
    
    ("Evaluation Rubric Design", 4, 1, "Phase 3"),
    ("Few-Shot Examples Collection", 4, 1, "Phase 3"),
    ("Prompt Engineering", 4, 1.5, "Phase 3"),
    
    ("Multi-Model Integration", 5, 1, "Phase 4"),
    ("Meta Review Mechanism", 5, 1, "Phase 4"),
    ("UI Prototype", 5, 1.5, "Phase 4"),
    
    ("End-to-End Testing", 6, 1, "Validation"),
    ("Human-AI Consistency Eval", 6, 1, "Validation"),
    ("Documentation & Report", 6, 1, "Validation"),
]

# 创建DataFrame
df = pd.DataFrame(tasks, columns=['Task', 'Start', 'Duration', 'Category'])

# 定义颜色方案（学术风格配色）
colors = {
    'Planning': '#2E86AB',      # 深蓝
    'Phase 1': '#A23B72',       # 玫红
    'Phase 2': '#F18F01',       # 橙色
    'Phase 3': '#C73E1D',       # 砖红
    'Phase 4': '#3B1F2B',       # 深紫
    'Validation': '#44AF69',    # 绿色
}

# 创建图表
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制甘特条
y_positions = range(len(df))
for idx, row in df.iterrows():
    ax.barh(
        y=idx,
        width=row['Duration'],
        left=row['Start'],
        height=0.6,
        color=colors[row['Category']],
        edgecolor='white',
        linewidth=0.5,
        alpha=0.85
    )

# 设置Y轴
ax.set_yticks(y_positions)
ax.set_yticklabels(df['Task'])
ax.invert_yaxis()  # 最上面的任务在顶部

# 设置X轴
ax.set_xlim(0.5, 7.5)
ax.set_xticks(range(1, 8))
ax.set_xticklabels([f'Week {i}' for i in range(1, 8)])
ax.set_xlabel('Project Timeline', fontweight='bold')

# 添加垂直网格线（周分隔）
for week in range(1, 8):
    ax.axvline(x=week, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)

# 添加阶段分隔线
phase_boundaries = [2, 5, 8, 11, 14]  # 任务索引
for boundary in phase_boundaries:
    if boundary < len(df):
        ax.axhline(y=boundary - 0.5, color='gray', linestyle='-', linewidth=0.8, alpha=0.3)

# 添加图例
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=colors[cat], label=cat, alpha=0.85) 
                   for cat in ['Planning', 'Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Validation']]
ax.legend(handles=legend_elements, loc='lower right', frameon=True, 
          fancybox=True, shadow=False, ncol=2, fontsize=9)

# 添加标题
ax.set_title('HorizonBench: Project Development Timeline', 
             fontsize=14, fontweight='bold', pad=15)

# 添加阶段标注（右侧）
phase_labels = [
    (0.5, "Planning"),
    (3, "Paper\nUnderstanding"),
    (6, "Deep Research\nAgent"),
    (9, "Multi-Dim\nEvaluation"),
    (12, "Multi-Model\nConsensus"),
    (15, "Validation"),
]

# 微调布局
plt.tight_layout()

# 保存图片
plt.savefig('horizonbench_gantt.pdf', format='pdf', bbox_inches='tight')
plt.savefig('horizonbench_gantt.png', format='png', bbox_inches='tight', dpi=300)
plt.show()

print("图表已保存为 horizonbench_gantt.pdf 和 horizonbench_gantt.png")