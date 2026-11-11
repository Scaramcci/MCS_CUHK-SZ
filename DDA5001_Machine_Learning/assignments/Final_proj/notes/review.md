# Final Project Part I 独立交付审查

2026-11-11，独立 Reviewer `/root/review`。受审版本为 `local_artifacts/candidate/part1-results.zip`，SHA-256 为 `37e478f6db821a87fd31c38d8468da0326c8ee5734984ecf449e921f177092a7`。解包后的 `part1-report.pdf` 与本地报告逐字节一致，SHA-256 为 `a738a4ef048363bb98f89574fb8b52724a3224be30dd941578836880e7c3eb7c`。本次直接审查该 ZIP，未参与实现、报告写作或本轮独立技术验证。

## Critical issues

在本次审查范围内未发现错误版本、凭据泄露、数据或模型误装等问题。ZIP 的 73 项成员名唯一，CRC 检查通过。

## Major issues

手册第 7 页 §3.4 要求列明每位组员贡献。报告的 Member 1、Member 2 两栏按用户要求留空。两位组员需自行填写各自真实贡献；补齐并重新封包前，不满足最终提交条件。

## Minor issues

未发现影响阅读或复现的其他问题。

## Submission checklist

| 手册来源与要求 | 受检材料与结果 |
| --- | --- |
| 第 5–6 页 §3.1–3.3，七处填空、原生优化器、固定评估、先检查再 smoke | 通过。已核验包中核心代码的散列与六组 environment.json 中实际训练代码一致。独立 Verifier 核对教师模板、前后检查及 CPU smoke，记录于 notes/verification.md 和 results/verification/preflight/。 |
| 第 6–7 页 §3.3.2，三种优化器各两档 LR、同预算、比较终点 | 通过。六份 CSV 均有 11 个评估点，以第 5,000 步、92,160,000 个 token 收尾。每份 CSV 的终点损失及训练秒数换算为分钟后与报告全部六行一致。半学习率选择与默认曲线匹配。AdamW 两档的验证损失在第 500–1,000 步之间换序，SGDM 在第 3,000–3,500 步之间换序。|
| 第 7 页 §3.4.1，曲线、时长、分析、困难与解决 | 通过。实际 ZIP 解出的 PDF 为 A4 一页。已渲染整页，十二条训练/验证曲线按优化器分为三图，图例、图注、表格、样本和贡献栏可读，无截断或互相遮挡。报告解释较早最优点与最终预算的区别，并说明因果掩码和优化器步进处理。|
| 第 7 页 §3.3.2、§3.4.1，终点文本 | 通过。包中 AdamW 默认学习率 0.0003 的 samples.txt 与运行原件一致，运行命令指定 last.pt。报告所选片段及采样参数匹配；复核训练划分内最长逐字匹配为 386 字符。 |
| 第 7 页 §3.4.1、§3.4.3，双人贡献与按组提交 | 两条贡献待本人填写。每组提交一次，由组员执行。|
| 第 7 页 §3.4.2，代码及运行材料 | 通过。完整清单见 notes/candidate-files.txt。包内为 25 个 code/ 文件、46 个 results/ 文件、一份说明及一份 PDF。每组包含配置、环境、CSV、摘要、运行日志和两个图。另有两张汇总图、比较索引与代表性样本。与原始结果逐项比较，差异限于六份 config.json 和六份 summary.json 的数据或输出目录相对化。|
| 第 7 页 §3.4.2，不打包数据和 checkpoint，另备份权重 | 通过。包中无权重、数据集、缓存或内部角色文档。候选文本未检出账户路径、私钥或访问凭据；README.txt 说明放置原数据的位置。十二个本地 best.pt/last.pt 的独立校验及元数据抽检见 results/verification/six/checkpoint-sha.log 与 backups-cpu.log。|

独立技术验证见 `notes/verification.md` 和 `results/verification/six/final-check.log`。该验证包括本机 smoke、六组训练证据与备份核对、一次终点样本前缀的 CPU 前向抽查。六组正式训练和随机生成使用原始 GPU 执行记录。Reviewer 此次没有重训。

## Final readiness

**Not ready。** 技术结果和交付清单已通过本次审查，提交余项为两位组员的真实贡献。填写后重新导出 PDF、替换 ZIP 内的报告并复核最终包页数、呈现、清单和哈希；本结论对应上列候选版本。
