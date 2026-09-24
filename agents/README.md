# 课程多 Agent 工作体系

这是六份可复用角色 Prompt 和交接约定，不是自动调度框架。所有角色先遵守[根 AGENTS.md](../AGENTS.md)，再读取目标路径规则与对应角色文件。本次只建立规则，不运行任何作业。

## 从任意课程或作业目录使用

1. 确认目标作业目录；在对话中说“请作为 Planner 处理当前作业，读取仓库根 agents/planner.md”。所有文档中的 `agents/...` 均相对仓库根，工作产物路径均相对目标作业。
2. 单个角色调用只执行该角色职责；想完成整个流程时明确说“按 agents/README.md 的多 Agent 工作流执行”。从课程目录开始且未指明作业时，先定位目标，不能自动批量处理所有作业。
3. 下列角色文件各自包含可复制 Prompt。调度者可以是当前主对话，负责传递输入、安排顺序和汇总；不需要新增 Coordinator Agent 文件。
4. 本仓库没有注册自定义 Agent 类型或斜杠命令。读取 `agents/verifier.md` 不会自动启动独立 Agent。运行环境支持子 Agent 时，由调度者分别创建独立执行者；否则用户将对应 Prompt 交给独立新会话。
5. 不把同一会话的角色切换当作独立验证。若尚未启动独立 Verifier/Reviewer，只能标为自查或“未完成独立验证”，不能宣称整个工作流完成。

Codex 按项目根到当前工作目录发现指令文件，更近目录的规则可覆盖较远规则；因此从根启动处理子目录时，本仓库要求显式读取目标路径规则。新增/修改规则后，新会话应确认加载了哪些文件。机制依据：[OpenAI 官方 AGENTS.md 文档](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

## 职责与产物

| 角色 | 核心工作 | 默认产物（仅需要时创建） | 不承担 |
| --- | --- | --- | --- |
| [Planner](planner.md) | 题意、评分点、提交物、计划与风险 | notes/plan.md | 大量实现、最终报告 |
| [Researcher](researcher.md) | 背景研究、核实可靠来源 | notes/research.md | 最终报告、虚构引用 |
| [Implementer](implementer.md) | 实现、计算、自测、实际运行与修复 | src/、tests/、results/、运行说明 | 独立验收、代签审查 |
| [Report Writer](report-writer.md) | 依据代码与证据写报告/论文/文档 | report/、必要时 notes/report-evidence.md | 补造实验、改代码迎合报告 |
| [Verifier](verifier.md) | 独立技术验证、复现、边界检查 | notes/verification.md、results/verification/ | 修改被测实现、最终质量批准 |
| [Reviewer](reviewer.md) | 逐项验收内容与确切提交包 | notes/review.md | 实现、修复后自行批准 |

Implementer 可以写测试并自测；Verifier 需独立执行和设计必要检查。Report Writer 可以自查版面；Reviewer 仍需独立审最终稿。技术正确性与任务完整性存在必要交叉，但实现、技术验证、最终批准的责任不合并。

## 推荐流程

```text
普通代码作业：
Planner → Implementer → Verifier → Report Writer（如需报告）→ Reviewer

需要文献/背景的编程或实验：
Planner → Researcher → Implementer → Verifier → Report Writer → Reviewer

纯文档 / 课程论文：
Planner → Researcher → Report Writer → Reviewer

简单手写题辅助：
Planner → Implementer（承担 Solver）→ Reviewer
```

包含代码/实验的课程论文走实验流程；依赖复杂数值计算的手写题在 Reviewer 前加 Verifier。项目采用与实验相同的流程，按阶段拆分而非增加角色。教师不要求的报告、研究或代码不强制生成，省略原因记入计划。

### 执行、修复与提交候选

1. Planner 给出要求—提交物—验收映射。Researcher 在确有知识缺口时介入。
2. Implementer 实现并保存真实运行证据；Verifier 针对当前版本独立检查。依赖未完成时不得提前宣称完成下游阶段。
3. 技术失败退回 Implementer → Verifier 重验；Report Writer 可先写有证据的部分，缺失结果必须标明。关键实验未完成不能出具最终完成报告。
4. Report Writer 写完并自查所需文档。无需文档时跳过。报告提出新实验需求则回到 Implementer → Verifier，不由写作者填数值。
5. 在进入最终 Reviewer 前，调度者依据已确定的提交清单，将核验后的交付文件复制/打包到 `submission/`，作为最终准备提交版本。记录文件清单与 SHA-256（压缩包同时记录内部清单）；不把内部工作记录一并打包。组装可以委托产物作者，但批准仍由独立 Reviewer 做。
6. Reviewer 审实际候选包。技术问题退回 Implementer/Verifier，文字问题退回 Report Writer，要求歧义退回 Planner。更新候选后重新核对包及受影响检查；不能沿用旧版 Ready。已有 submission 版本不静默覆盖或删除，替换前按需归档到 `results/submission-history/<version>/` 并区分版本。
7. Ready 后由用户决定提交；“准备最终文件”不等于授权 Agent 上传、发信或发布。

只有独立、无文件写入冲突的子任务才适合并行。Verifier 开始后保持受检文件稳定；中途发生改动则记录旧结论失效，选择新版本重验。

## 最小交接协议

每阶段在自己的记录或任务 README 的独立小节提供以下内容。简单任务可简化为几行，不创建无用文件；不要让多个 Agent 同时改同一 README。

```text
Role / Executor: 角色、执行者或会话标识；不能声称不存在的独立执行者
Task directory: 当前目标作业/项目
Scope: 本次授权内容、允许写入路径、不得修改的输入
Inputs: 原始要求与页码/题号、计划、代码/数据/结果版本
Version: Git commit（若有）＋未提交改动说明，或相关文件 SHA-256
Work done: 实际完成内容；实现/运行/验证状态分开
Evidence: 产物路径、真实运行命令、退出状态、日志/结果位置
Open issues: 未执行、失败、阻断及适用的局限
Next role: 下一角色及具体验收事项
```

内部文档放当前任务 `notes/`，运行证据放 `results/`；这些文件不是默认提交物。旧失败记录保留，不将新结果冒充旧运行证据。没有测试可执行的文档任务写明 N/A，不伪造运行记录。

## 课程级与作业级规则

在有实际课程规则时添加 `course-name/AGENTS.md`；只针对某次作业的限制可放其目录的 `AGENTS.md`，不要把单次要求扩大为整门课程规则。无需复制六个角色文件。

下面只是格式示例，使用时填写已确认内容，未知写“待确认”，不直接当作任何当前课程的要求：

```markdown
# <课程编号 / 作业编号> 补充规则

继承仓库根 AGENTS.md；不得放宽真实性、原件保护、隐私与独立验证规则。

- 规则来源：<教师文件、页码/章节、适用作业与日期>
- 编程语言/版本：<例如 Python 或 C++；按原文填写>
- 依赖与禁用库：<按原文填写>
- 运行环境/硬件：<Python 版本、CPU/GPU 等>
- 随机种子：<教师指定值；未指定时由实现记录所用值>
- 报告语言/模板/格式：<按原文填写>
- 提交命名与打包方式：<按原文填写>
- 未解决冲突：<冲突原文位置及待确认事项>
```

这些是仓库协作约定，不是沙箱权限。若某级规则或 `AGENTS.override.md` 弱化基础规则，必须指出冲突；不要假设 Markdown 能提供不可绕过的访问控制。

## 作业 README 建议字段

后续有真实任务时增补已有 README；保留已有内容，不批量创建不存在作业的空文件。

```markdown
# <作业名称>

## Task
<目标、题号、原件路径>
## Deadline
<日期、时区、来源；未知明确标记>
## Requirements
<编号、原文位置与评分点>
## Deliverables
<需提交的内容与格式>
## Constraints
<语言、库、环境、数据与协作限制>
## Status
<未开始/规划中/实现中/待验证/待修复/待审查/Ready；检查版本及证据链接>
## Run commands
<环境、依赖、工作目录、实际命令；未执行标明，纯文档按需写编译命令或 N/A>
## Submission files
<确切文件名、对应要求、候选版本；尚未生成不得写已存在>
## Notes
<计划、研究、运行与审查记录链接，未解决事项>
```

## NLP 作业目录使用示例

目标：`CSC5051_Natural_Language_Processing/assignments/hw01/`。以下都是未来调用示例，本次未执行：

1. 进入目标目录，发送：“请作为 Planner，读取仓库根 agents/planner.md 和当前作业原始要求，只制定计划，暂不实现。”
2. 若计划需要背景，调用 Researcher，核实 Word2Vec 与相关 API，保存研究笔记。
3. 发送：“按计划让 Implementer 完成已授权范围，保留教师 notebook 原件，记录真实运行输出。”
4. 调度独立 Verifier，使用 verifier.md 的 Prompt，验证当前 notebook/代码及输出；失败退回修复。
5. 只有原文要求报告或解释文字时调用 Report Writer，形式以原文为准，不擅自追加 PDF 提交物。
6. 按教师要求组装最终候选，再由另一独立 Reviewer 审核 notebook、完整性、命名和最终包。确认 Ready 后由用户提交。

也可一次明确授权整个流程：

```text
目标是当前作业目录。请按仓库根 agents/README.md 的多 Agent 流程处理：
先读全局/课程/作业规则及教师原件，由 Planner 制定计划，再按需要调用 Researcher、Implementer、Report Writer。
将 Verifier 和 Reviewer 分别交给未参与创作的不同独立子 Agent；交接目标路径、角色规则、版本和允许写入范围。
按阶段验收，问题退回作者修复后复验；无法独立执行时明确说明缺口并提供新会话 Prompt，不把角色切换当作独立验证。
只在当前作业内工作，准备最终提交文件但不要上传，不访问 Chores 或 _private。
```

目前六个角色足够。手写题的解题/计算由 Implementer 承担，打包与交接由主对话协调，暂不增加 Solver、Publisher 或复杂配置系统。
