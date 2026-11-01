# DDA5001 Homework 3

## 状态

2026-10-29：资料核查完成，等待实际 HW3 题目或用户确认材料位置。尚未实现、运行实验、编写答案或组装提交包。

## 已有材料与缺失项

当前 `requirements/` 只有两个原件，均保持不变：

| 原件 | 核查依据 | SHA-256 |
| --- | --- | --- |
| `DDA5001_HW1_Solution.pdf` | 共 16 页；已提取文本并查看首页渲染。第 1 页明确标为 DDA5001 Homework 1，截止 Sep 30、提交命名 hw1；包含参考解答，不能据此确定 HW3 要求。 | `9dec12e49bf7bc18042ba7fa698db18ab9cbace4dfdc78e0e1c9b25534fa9e1d` |
| `code_solution.zip` | 已查看完整条目清单及根 README、依赖说明。内部 `code_solution/README.md` 明确标为 Homework 1 第 3、5 题的教师代码答案；包含数据和参考输出，未执行。 | `3f94adfc2de59c633c57c13dd283f143de3404eb169395991be3767a2a685da9` |

未找到实际 HW3 题目、配套起始代码或要求说明。HW3 的题号、评分点、截止时间、提交格式、语言/库限制及 AI 使用要求均待原文确认，不继承 HW1/HW2 的教师要求。课程级、assignments 级及 hw03 级未发现 AGENTS.md 或 AGENTS.override.md；本作业原先无 README。

## 后续工作

已参考 hw01/hw02 的目录与完成记录。取得正确原件后，先按题号建立要求—来源—交付物—验收映射，再按实际任务安排实现、运行、报告、独立 Verifier 与独立 Reviewer；若需提交包，审查实际候选文件。可沿用此前代码、报告源文件、真实运行证据与提交包分开的组织形式，具体交付内容以 HW3 原文为准。

## 阶段记录

- Role / Executor：Planner，当前主会话 `/root`。
- Scope：仅核查 hw03 材料，参考前次作业完成形式；未修改教师原件或其他作业。
- Inputs：根 README、AGENTS.md、agents/README.md、agents/planner.md、课程 README、hw01/hw02 README，以及上述原件。
- Version：上述 SHA-256；开始时分支为 master，工作区干净。
- Evidence：PDF 首页视觉核对、PDF 文本提取、ZIP 清单与内部 README；课程文件名检索未找到其他 HW3 题目。没有开展代码运行或独立验证。
- Open issues：需提供实际 HW3 原件位置，或说明现有材料与目标任务的关系。
- Next role：Planner 继续解析正确题目，再启动有依据的后续阶段。
