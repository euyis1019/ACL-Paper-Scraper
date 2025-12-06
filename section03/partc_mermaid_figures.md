# HorizonBench Part C: Mermaid Diagrams

> 将每个代码块分别转换为 PNG，文件名见标题

---

## Figure 2: system_overview.png

```mermaid
flowchart TB
    subgraph Input["Input"]
        PDF["Academic Paper PDF"]
    end

    subgraph Phase1["Phase 1: Paper Understanding"]
        direction TB
        P1A["MinerU Parser"]
        P1B["LLM Extraction"]
        P1C["Paper Schema"]
        P1A --> P1B --> P1C
    end

    subgraph Phase2["Phase 2: Deep Research Agent"]
        direction TB
        P2A["Research Planning"]
        P2B["Iterative Search"]
        P2C["OpenReview Query"]
        P2D["Benchmark Synthesis"]
        P2A --> P2B
        P2A --> P2C
        P2B & P2C --> P2D
    end

    subgraph Phase3["Phase 3: Multi-Dimensional Evaluation"]
        direction TB
        P3A["Layer 1: 4 Dimensions"]
        P3B["Layer 2: 12 Metrics"]
        P3C["Grade-Based Rating"]
        P3A --> P3B --> P3C
    end

    subgraph Phase4["Phase 4: Multi-Model Consensus"]
        direction TB
        subgraph Reviewers["Independent Reviewers"]
            R1["GPT-4"]
            R2["Claude 3.5"]
            R3["DeepSeek-V3"]
        end
        P4A["Parallel Review"]
        P4B["Meta Review: Gemini"]
        P4C["Final Decision"]
        R1 & R2 & R3 --> P4A
        P4A --> P4B --> P4C
    end

    subgraph Output["Output"]
        O1["Overall Rating"]
        O2["Dimension Scores"]
        O3["Benchmark Context"]
        O4["Actionable Feedback"]
    end

    PDF --> Phase1
    Phase1 --> Phase2
    Phase2 --> Phase3
    Phase3 --> Phase4
    Phase4 --> Output

    style Phase1 fill:#e3f2fd
    style Phase2 fill:#fff3e0
    style Phase3 fill:#e8f5e9
    style Phase4 fill:#fce4ec
```

---

## Figure 3: paper_understanding.png

```mermaid
flowchart LR
    subgraph Input["Input"]
        PDF["PDF Document"]
    end

    subgraph Parsing["Structural Parsing"]
        MinerU["MinerU Engine"]
        subgraph Preserved["Preserved Elements"]
            Dual["Dual-Column Layout"]
            Math["Mathematical Formulas"]
            Table["Tables & Figures"]
        end
        MinerU --> Preserved
    end

    subgraph Extraction["Semantic Extraction"]
        MD["Structured Markdown"]
        LLM["LLM Extractor"]
        subgraph Fields["Extracted Fields"]
            Meta["Metadata"]
            Content["Content Understanding"]
            Class["Classification"]
            Relation["Relation Network"]
        end
        MD --> LLM --> Fields
    end

    subgraph Validation["Validation"]
        Check{"Fields Complete?"}
        Retry["LLM Retry"]
        Schema["Paper Schema"]
        Check -->|No| Retry
        Retry --> Check
        Check -->|Yes| Schema
    end

    PDF --> MinerU
    Preserved --> MD
    Fields --> Check

    style Parsing fill:#e3f2fd
    style Extraction fill:#fff3e0
    style Validation fill:#e8f5e9
```

---

## Figure 4: deep_research.png

```mermaid
flowchart TB
    subgraph Input["Input from Phase 1"]
        Schema["Paper Schema"]
        Keywords["Keywords & Domain"]
        Relations["Relation Network"]
    end

    subgraph Planning["Step 1: Research Planning"]
        Analyze["LLM Analyzes Research Problem"]
        GenPlan["Generate Search Strategy"]
        subgraph Queries["Search Dimensions"]
            Q1["Core Method"]
            Q2["Application Domain"]
            Q3["Baseline Models"]
            Q4["Datasets"]
        end
        Analyze --> GenPlan --> Queries
    end

    subgraph Search["Step 2: Iterative Search Loop"]
        GenQuery["Generate Query"]
        subgraph APIs["Search APIs"]
            SS["Semantic Scholar"]
            AX["arXiv"]
            OR["OpenReview"]
        end
        Results["Search Results"]
        subgraph Filter["LLM Relevance Filter"]
            High["High: Get Full Text"]
            Medium["Medium: Keep Abstract"]
            Low["Low: Discard"]
        end
        subgraph Control["Loop Control"]
            Count{"Collected >= N?"}
            Sufficient{"Coverage Sufficient?"}
            Gap["Identify Knowledge Gap"]
        end
        GenQuery --> APIs --> Results --> Filter
        High & Medium --> Count
        Count -->|No| GenQuery
        Count -->|Yes| Sufficient
        Sufficient -->|Gap Found| Gap --> GenQuery
    end

    subgraph Synthesis["Step 3: Benchmark Synthesis"]
        Aggregate["Aggregate Literature"]
        subgraph Report["Dynamic Benchmark"]
            SOTA["Current SOTA"]
            Trends["Research Trends"]
            Gaps["Open Problems"]
            Position["Paper Positioning"]
        end
        Aggregate --> Report
    end

    subgraph Output["Output"]
        Benchmark["Contextualized Benchmark"]
        FewShot["Few-Shot Examples"]
    end

    Schema & Keywords & Relations --> Analyze
    Sufficient -->|Sufficient| Aggregate
    Report --> Benchmark
    OR --> FewShot

    style Planning fill:#e3f2fd
    style Search fill:#fff8e1
    style Synthesis fill:#e8f5e9
```

---

## Figure 5: multi_model.png

```mermaid
flowchart TB
    subgraph Input["Input"]
        Paper["Paper Schema"]
        Benchmark["Dynamic Benchmark"]
        FewShot["Few-Shot Examples"]
    end

    subgraph Independent["Independent Reviews - Parallel"]
        subgraph R1["Reviewer 1: GPT-4"]
            R1Rate["4 Dimension Grades"]
            R1Text["Review Comments"]
        end
        subgraph R2["Reviewer 2: Claude 3.5"]
            R2Rate["4 Dimension Grades"]
            R2Text["Review Comments"]
        end
        subgraph R3["Reviewer 3: DeepSeek-V3"]
            R3Rate["4 Dimension Grades"]
            R3Text["Review Comments"]
        end
    end

    subgraph MetaReview["Meta Review: Gemini 1.5 Pro - Area Chair"]
        Collect["Collect All Reviews"]
        subgraph Analysis["Synthesis Analysis"]
            Consensus["Identify Consensus"]
            Divergence["Analyze Divergence"]
            PaperCheck["Verify Against Paper"]
        end
        subgraph Decision["Final Decision"]
            FinalRating["Overall Rating"]
            Justification["Decision Rationale"]
            Confidence["Confidence Score"]
            Suggestions["Improvement Suggestions"]
        end
        Collect --> Analysis --> Decision
    end

    subgraph Output["Final Output"]
        Report["Complete Evaluation Report"]
    end

    Paper & Benchmark & FewShot --> R1 & R2 & R3
    R1 & R2 & R3 --> Collect
    Decision --> Report

    style Independent fill:#e3f2fd
    style MetaReview fill:#fff3e0
```

---

## Figure 6: evaluation_dims.png

```mermaid
flowchart TB
    subgraph Input["Input"]
        Paper["Target Paper"]
        Benchmark["Dynamic Benchmark"]
        FewShot["Few-Shot Examples"]
    end

    subgraph Layer1["Layer 1: Orthogonal Dimensions"]
        subgraph D1["Technical Quality"]
            D1Q["Is methodology correct?"]
        end
        subgraph D2["Novelty & Contribution"]
            D2Q["Contribution over SOTA?"]
        end
        subgraph D3["Clarity & Presentation"]
            D3Q["Is writing clear?"]
        end
        subgraph D4["Soundness & Validity"]
            D4Q["Are conclusions supported?"]
        end
    end

    subgraph Layer2["Layer 2: Fine-Grained Metrics"]
        subgraph D1Sub["Technical Quality"]
            D1S1["Methodology Rigor"]
            D1S2["Experimental Design"]
            D1S3["Reproducibility"]
        end
        subgraph D2Sub["Novelty"]
            D2S1["Originality"]
            D2S2["Significance"]
            D2S3["Impact"]
        end
        subgraph D3Sub["Clarity"]
            D3S1["Writing Quality"]
            D3S2["Organization"]
            D3S3["Figures & Tables"]
        end
        subgraph D4Sub["Soundness"]
            D4S1["Correctness"]
            D4S2["Evidence"]
            D4S3["Limitations"]
        end
    end

    subgraph Rating["Grade-Based Rating Scale"]
        Scale["Strong Accept | Accept | Weak Accept | Borderline | Weak Reject | Reject | Strong Reject"]
    end

    subgraph Output["Output"]
        DimRatings["4 Dimension Grades"]
        SubRatings["12 Metric Assessments"]
        TextFeedback["Textual Justifications"]
    end

    Input --> Layer1
    D1 --> D1Sub
    D2 --> D2Sub
    D3 --> D3Sub
    D4 --> D4Sub
    Layer2 --> Rating --> Output

    style Layer1 fill:#e3f2fd
    style Layer2 fill:#fff8e1
    style Rating fill:#e8f5e9
```

---

## Figure 7: output_report.png

```mermaid
flowchart TB
    subgraph Report["HorizonBench Evaluation Report"]
        subgraph Header["Section 1: Header"]
            Title["Paper Title & Metadata"]
            Overall["Overall Rating: Accept"]
            Conf["Confidence: High"]
        end
        
        subgraph DimScores["Section 2: Dimension Scores"]
            DS1["Technical Quality: Accept"]
            DS2["Novelty: Strong Accept"]
            DS3["Clarity: Accept"]
            DS4["Soundness: Weak Accept"]
        end
        
        subgraph BenchmarkCtx["Section 3: Benchmark Context"]
            BC1["Related Papers: 15"]
            BC2["Current SOTA: Method X"]
            BC3["Positioning: Exceeds in Y"]
        end
        
        subgraph ReviewerSum["Section 4: Reviewer Summary"]
            RS1["GPT-4: Accept"]
            RS2["Claude: Accept"]
            RS3["DeepSeek: Weak Accept"]
        end
        
        subgraph MetaSec["Section 5: Meta Review"]
            MR1["Consensus Points"]
            MR2["Divergence Resolution"]
            MR3["Decision Rationale"]
        end
        
        subgraph Feedback["Section 6: Feedback"]
            Strengths["Strengths"]
            Weaknesses["Weaknesses"]
            Suggestions["Improvement Suggestions"]
        end
    end

    Header --> DimScores --> BenchmarkCtx --> ReviewerSum --> MetaSec --> Feedback

    style Header fill:#e8f5e9
    style DimScores fill:#e3f2fd
    style BenchmarkCtx fill:#fff3e0
    style MetaSec fill:#fce4ec
    style Feedback fill:#f3e5f5
```

---

## 图片命名对照表

| Figure | Mermaid 代码块 | 输出文件名 |
|--------|---------------|-----------|
| Figure 2 | system_overview | `system_overview.png` |
| Figure 3 | paper_understanding | `paper_understanding.png` |
| Figure 4 | deep_research | `deep_research.png` |
| Figure 5 | multi_model | `multi_model.png` |
| Figure 6 | evaluation_dims | `evaluation_dims.png` |
| Figure 7 | output_report | `output_report.png` |

**放置路径**: `figures/` 目录下
