# MCS 研究生课程统一仓库 · 2026–27 学年第一学期

按当前教学计划与 Fall 2026 课件整理。整个学期共用根目录一个 Git 仓库；课程目录不创建 `.git`，不使用 Git submodule。本次仅整理已有资料，未完成任何作业。

## Agent 工作入口

全局规则见 [AGENTS.md](AGENTS.md)，六个角色的职责、Prompt、独立验证及交接流程见 [agents/README.md](agents/README.md)。进入具体作业目录后，可直接要求“作为 Planner 处理当前作业，读取仓库根 agents/planner.md”。

`Chores/` 与任何层级的 `_private/` 均为本地隐私目录，已加入 Git 忽略；除非任务明确要求，Agent 不主动访问。课程/作业可按需补充自己的 AGENTS.md，不放宽全局真实性、原件保护和隐私规则。

## 课程索引

| 目录 | 课程 | 当前资料覆盖 |
| --- | --- | --- |
| [CSC5010_Artificial_Intelligence/](CSC5010_Artificial_Intelligence/README.md) | 人工智能 | 人工智能基础、状态空间搜索、BFS/DFS、Dijkstra、启发式搜索与博弈。 |
| [CSC5036_Network_Programming/](CSC5036_Network_Programming/README.md) | 网络编程 | 计算机网络、传输层、TCP 流量与拥塞控制、Socket 编程及 EC2 网络测量。 |
| [CSC5041_Introduction_to_Database_Systems/](CSC5041_Introduction_to_Database_Systems/README.md) | 数据库系统导论 | ER 建模、关系模型、关系代数、SQL 和数据库设计。 |
| [CSC5051_Natural_Language_Processing/](CSC5051_Natural_Language_Processing/README.md) | 自然语言处理 | 语言学基础、词表示、Word2Vec 与自然语言处理。 |
| [DDA5001_Machine_Learning/](DDA5001_Machine_Learning/README.md) | 机器学习 | 监督与无监督学习、感知机、最小二乘、最大似然、训练与测试。 |

## 目录规范

保留现有课程编号与目录名，教师原始文件名原则上不改。按需建立：

| 目录 | 用途 |
| --- | --- |
| `syllabus/` | 大纲、评分规则、课程说明、教学安排 |
| `slides/` | 教师 PPT、讲义；包含课程说明的完整课件仍放此处，不拆分原文件 |
| `assignments/hwXX/` | 已明确发布的作业 |
| `projects/projectXX/` | 已明确发布的项目或大作业 |
| `notes/` | 自己的笔记 |
| `resources/` | 参考资料、Tutorial、数据说明等 |
| `exams/` | 考试与复习资料 |
| `templates/latex/` | 共享 LaTeX 模板，可纳入 Git |
| `00_unsorted/` | 归属无法确定的新增文件；本次没有需放入的文件，暂不创建 |
| `Chores/` | 行政通知、选课、个人证明、申请、会议等校内事务；本地保留，禁止提交 |

作业内 `requirements/` 保存教师要求与原始配套压缩包；按需建立 `src/`、`report/`、`results/`、`submission/`。手写作业可增加 `handwritten/` 和 `notes/`。项目采用类似结构，并按需增加 `data/`。不为未发布作业或项目预建目录，不用占位文件制造空目录。

**`submission/` 表示最终实际提交版本**，不是草稿或编译缓存；保留提交的确切文件。教师原件原则上保留且不直接修改，编辑时复制到自己的工作目录。Git 不保存空目录。

## Git 与本地资料

- 只在根目录初始化 Git；本次不提交、不设置远程、不上传 GitHub。
- `.gitignore` 明确忽略 `/Chores/`，以及系统文件、环境、缓存、Office 临时文件、LaTeX 中间文件、构建目录、凭据与模型权重。
- `.gitignore` 对已被跟踪的文件不生效；以后添加资料时确认 `git status`，不要强制添加 Chores。
- 不全局忽略 PDF、PPTX、Word、ZIP、`.npy`、`.mat` 或 `submission/`，避免遗漏教师原件、小型配套数据与最终提交件。
- 大数据放入相应作业/项目的 `data/raw/` 或 `data/downloads/`（已忽略），README 记录来源、版本与获取方法；模型检查点放 `checkpoints/`。这些目录本次均未创建。
- 部分 CSC5010 讲义明确写有不得向他人传播的限制；仓库应保持私有，公开发布前需处理这些材料的传播权限。

## 本次整理记录

- 识别 5 门课程、5 个已有作业文件夹；无具体项目要求，不创建项目目录。
- 数据库 Questions.pdf 为 Tutorial 1，归入 resources/tutorials；NLP Tutorial 1.zip 同类归档。
- 网络作业原文 CSC4303 与现有 CSC5036 目录不一致，沿用原目录归属并标记待核实；AI hw02 仅沿用旧 Homework2 编号，原文未确认官方编号。
- CUHK-beamer.zip 为 Beamer 幻灯片模板，原样移至 templates/latex，可提交 Git。
- 机器学习同章带 `(1)` 的课件保留全部版本。评分图片扩展名为 .jpg，实际为 HEIF，预览解码失败，依据文件名归类，未改内容。
- Chores 已包含校内行政与选课材料，本次原地保留；系统 .DS_Store 原地保留并忽略。
- 原有文件共 74 个，合计约 123.82 MiB；最大单文件 Week 1A - IntroductionNEW.pptx 约 22.27 MiB，EC2 PPT 约 12.91 MiB。未发现独立的大型数据集、模型权重或缓存目录。
- code_source.zip 约 4.05 MiB，内含 .npy/.mat 数据和代码；解包总计约 4.12 MiB，可保留原包。ZIP 中的 __MACOSX 和 .DS_Store 没有删除；Git 忽略规则不会过滤压缩包内部条目。

<details>
<summary>完整文件移动清单（原文件名均保留）</summary>

| 原路径 | 新路径 |
| --- | --- |
| `CSC5010_Artificial_Intelligence/AI-Introduction2026-09-01.pdf` | `CSC5010_Artificial_Intelligence/slides/AI-Introduction2026-09-01.pdf` |
| `CSC5010_Artificial_Intelligence/AI_Search_Ding6.pdf` | `CSC5010_Artificial_Intelligence/slides/AI_Search_Ding6.pdf` |
| `CSC5010_Artificial_Intelligence/BFS-DFS-Dijkstra-2026-4-7.pdf` | `CSC5010_Artificial_Intelligence/slides/BFS-DFS-Dijkstra-2026-4-7.pdf` |
| `CSC5010_Artificial_Intelligence/GamesCDing2026-9-3.pdf` | `CSC5010_Artificial_Intelligence/slides/GamesCDing2026-9-3.pdf` |
| `CSC5010_Artificial_Intelligence/Homework1/AI-2026-homeWork-Set-1.pdf` | `CSC5010_Artificial_Intelligence/assignments/hw01/requirements/AI-2026-homeWork-Set-1.pdf` |
| `CSC5010_Artificial_Intelligence/Homework2/BFS-DFS-Dijkstra-Astar-homework.pdf` | `CSC5010_Artificial_Intelligence/assignments/hw02/requirements/BFS-DFS-Dijkstra-Astar-homework.pdf` |
| `CSC5010_Artificial_Intelligence/Informed_Search_Ding2026-6-15.pdf` | `CSC5010_Artificial_Intelligence/slides/Informed_Search_Ding2026-6-15.pdf` |
| `CSC5036_Network_Programming/01-intro.pdf` | `CSC5036_Network_Programming/slides/01-intro.pdf` |
| `CSC5036_Network_Programming/02-network.pdf` | `CSC5036_Network_Programming/slides/02-network.pdf` |
| `CSC5036_Network_Programming/03-transport.pdf` | `CSC5036_Network_Programming/slides/03-transport.pdf` |
| `CSC5036_Network_Programming/04-flow_control.pdf` | `CSC5036_Network_Programming/slides/04-flow_control.pdf` |
| `CSC5036_Network_Programming/05-congestion.pdf` | `CSC5036_Network_Programming/slides/05-congestion.pdf` |
| `CSC5036_Network_Programming/06-socket.pdf` | `CSC5036_Network_Programming/slides/06-socket.pdf` |
| `CSC5036_Network_Programming/Homework1/Assignment1.md` | `CSC5036_Network_Programming/assignments/hw01/requirements/Assignment1.md` |
| `CSC5036_Network_Programming/Homework1/ec2(1).pptx` | `CSC5036_Network_Programming/assignments/hw01/requirements/ec2(1).pptx` |
| `CSC5036_Network_Programming/Homework1/ec2_measurement.pdf` | `CSC5036_Network_Programming/assignments/hw01/requirements/ec2_measurement.pdf` |
| `CSC5041_Introduction_to_Database_Systems/CSC5041_Teaching_Plan.pdf` | `CSC5041_Introduction_to_Database_Systems/syllabus/CSC5041_Teaching_Plan.pdf` |
| `CSC5041_Introduction_to_Database_Systems/Lecture2A.pptx` | `CSC5041_Introduction_to_Database_Systems/slides/Lecture2A.pptx` |
| `CSC5041_Introduction_to_Database_Systems/Questions.pdf` | `CSC5041_Introduction_to_Database_Systems/resources/tutorials/Questions.pdf` |
| `CSC5041_Introduction_to_Database_Systems/Relational_Algebra.pptx` | `CSC5041_Introduction_to_Database_Systems/slides/Relational_Algebra.pptx` |
| `CSC5041_Introduction_to_Database_Systems/SQLpart1.pptx` | `CSC5041_Introduction_to_Database_Systems/slides/SQLpart1.pptx` |
| `CSC5041_Introduction_to_Database_Systems/Week 1A - IntroductionNEW.pptx` | `CSC5041_Introduction_to_Database_Systems/slides/Week 1A - IntroductionNEW.pptx` |
| `CSC5041_Introduction_to_Database_Systems/Week 1B - Conceptual DB Design.pptx` | `CSC5041_Introduction_to_Database_Systems/slides/Week 1B - Conceptual DB Design.pptx` |
| `CSC5051_Natural_Language_Processing/Homework1/Assignment_1.pdf` | `CSC5051_Natural_Language_Processing/assignments/hw01/requirements/Assignment_1.pdf` |
| `CSC5051_Natural_Language_Processing/Lecture 1：Introduction.pdf` | `CSC5051_Natural_Language_Processing/slides/Lecture 1：Introduction.pdf` |
| `CSC5051_Natural_Language_Processing/Lecture 2：Linguistics Basics and Word Representation.pdf` | `CSC5051_Natural_Language_Processing/slides/Lecture 2：Linguistics Basics and Word Representation.pdf` |
| `CSC5051_Natural_Language_Processing/Tutorial 1.zip` | `CSC5051_Natural_Language_Processing/resources/tutorials/Tutorial 1.zip` |
| `CUHK-beamer.zip` | `templates/latex/CUHK-beamer.zip` |
| `DDA5001_Machine_Learning/Composition_of_Score.jpg` | `DDA5001_Machine_Learning/syllabus/Composition_of_Score.jpg` |
| `DDA5001_Machine_Learning/Homework1/DDA5001_HW1.pdf` | `DDA5001_Machine_Learning/assignments/hw01/requirements/DDA5001_HW1.pdf` |
| `DDA5001_Machine_Learning/Homework1/code_source.zip` | `DDA5001_Machine_Learning/assignments/hw01/requirements/code_source.zip` |
| `DDA5001_Machine_Learning/Syllabus.pdf` | `DDA5001_Machine_Learning/syllabus/Syllabus.pdf` |
| `DDA5001_Machine_Learning/slides1_JY(1).pdf` | `DDA5001_Machine_Learning/slides/slides1_JY(1).pdf` |
| `DDA5001_Machine_Learning/slides2_JY(1).pdf` | `DDA5001_Machine_Learning/slides/slides2_JY(1).pdf` |
| `DDA5001_Machine_Learning/slides2_JY.pdf` | `DDA5001_Machine_Learning/slides/slides2_JY.pdf` |
| `DDA5001_Machine_Learning/slides3_JY(1).pdf` | `DDA5001_Machine_Learning/slides/slides3_JY(1).pdf` |
| `DDA5001_Machine_Learning/slides3_JY.pdf` | `DDA5001_Machine_Learning/slides/slides3_JY.pdf` |
| `DDA5001_Machine_Learning/slides4_JY.pdf` | `DDA5001_Machine_Learning/slides/slides4_JY.pdf` |
| `DDA5001_Machine_Learning/slides5_JY.pdf` | `DDA5001_Machine_Learning/slides/slides5_JY.pdf` |
| `DDA5001_Machine_Learning/slides6_JY.pdf` | `DDA5001_Machine_Learning/slides/slides6_JY.pdf` |
| `DDA5001_Machine_Learning/tutorial1_slides.pdf` | `DDA5001_Machine_Learning/slides/tutorial1_slides.pdf` |

</details>

核验：所有原始文件均仍存在；全部 67 个非 `.DS_Store` 文件 SHA-256 与整理前一致。系统元数据 `.DS_Store` 在整理过程中出现外部变化，不作为课程内容一致性的依据。

## 最终目录树

以下省略 Git 内部文件、系统元数据和 Chores 内的私人文件清单。

```text
.
├── CSC5010_Artificial_Intelligence/
│   ├── assignments/
│   │   ├── hw01/
│   │   │   ├── requirements/
│   │   │   │   └── AI-2026-homeWork-Set-1.pdf
│   │   │   └── README.md
│   │   └── hw02/
│   │       ├── requirements/
│   │       │   └── BFS-DFS-Dijkstra-Astar-homework.pdf
│   │       └── README.md
│   ├── slides/
│   │   ├── AI-Introduction2026-09-01.pdf
│   │   ├── AI_Search_Ding6.pdf
│   │   ├── BFS-DFS-Dijkstra-2026-4-7.pdf
│   │   ├── GamesCDing2026-9-3.pdf
│   │   └── Informed_Search_Ding2026-6-15.pdf
│   └── README.md
├── CSC5036_Network_Programming/
│   ├── assignments/
│   │   └── hw01/
│   │       ├── requirements/
│   │       │   ├── Assignment1.md
│   │       │   ├── ec2(1).pptx
│   │       │   └── ec2_measurement.pdf
│   │       └── README.md
│   ├── slides/
│   │   ├── 01-intro.pdf
│   │   ├── 02-network.pdf
│   │   ├── 03-transport.pdf
│   │   ├── 04-flow_control.pdf
│   │   ├── 05-congestion.pdf
│   │   └── 06-socket.pdf
│   └── README.md
├── CSC5041_Introduction_to_Database_Systems/
│   ├── resources/
│   │   └── tutorials/
│   │       └── Questions.pdf
│   ├── slides/
│   │   ├── Lecture2A.pptx
│   │   ├── Relational_Algebra.pptx
│   │   ├── SQLpart1.pptx
│   │   ├── Week 1A - IntroductionNEW.pptx
│   │   └── Week 1B - Conceptual DB Design.pptx
│   ├── syllabus/
│   │   └── CSC5041_Teaching_Plan.pdf
│   └── README.md
├── CSC5051_Natural_Language_Processing/
│   ├── assignments/
│   │   └── hw01/
│   │       ├── requirements/
│   │       │   └── Assignment_1.pdf
│   │       └── README.md
│   ├── resources/
│   │   └── tutorials/
│   │       └── Tutorial 1.zip
│   ├── slides/
│   │   ├── Lecture 1：Introduction.pdf
│   │   └── Lecture 2：Linguistics Basics and Word Representation.pdf
│   └── README.md
├── Chores/
│   └── （原有行政与个人资料保留，不列出隐私文件名）
├── DDA5001_Machine_Learning/
│   ├── assignments/
│   │   └── hw01/
│   │       ├── requirements/
│   │       │   ├── DDA5001_HW1.pdf
│   │       │   └── code_source.zip
│   │       └── README.md
│   ├── slides/
│   │   ├── slides1_JY(1).pdf
│   │   ├── slides2_JY(1).pdf
│   │   ├── slides2_JY.pdf
│   │   ├── slides3_JY(1).pdf
│   │   ├── slides3_JY.pdf
│   │   ├── slides4_JY.pdf
│   │   ├── slides5_JY.pdf
│   │   ├── slides6_JY.pdf
│   │   └── tutorial1_slides.pdf
│   ├── syllabus/
│   │   ├── Composition_of_Score.jpg
│   │   └── Syllabus.pdf
│   └── README.md
├── templates/
│   └── latex/
│       ├── CUHK-beamer.zip
│       └── README.md
├── .gitignore
└── README.md
```
