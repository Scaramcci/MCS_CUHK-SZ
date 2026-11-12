# hw04 最终提交包审查

**Ready。** 独立 Reviewer `/root/reviewer` 于 2026-11-12 审查了 `submission/226040255_hw4.zip`。包大小 7,646 字节，SHA-256 为 `12b0688cd6bce4012f075a532f853a144277c98cc11b00009c468a6fa4389121`。代码作者、技术验证者与本轮 Reviewer 分别承担各自职责。审查依据为教师原文 Required Experimental Environment、Testing、Submission Guidelines 和 Grading Criteria。

直接读取最终 ZIP 后，CRC 校验通过，ZIP 字节与已审候选完全相同。`submission/` 中只有这一个文件，包内两个成员的内容均与 EC2 运行记录一致。

| 成员 | 字节 | SHA-256 |
| --- | ---: | --- |
| `Assignment-4/chord_node.py` | 21,907 | `4427dab102a41527aff9567d26c660fc52a868739714dde0e268d19d50b77374` |
| `Assignment-4/test_dht.py` | 8,587 | `ea237f6b59cb24ff18edace676c0821d9e9ae9a091f4d6c0895efaca646d4d11` |

测试文件与教师原始 ZIP 逐字节一致。前轮对同一源码版本的独立验证覆盖全环查找、指表、键所有权、重复迁移和节点故障。最终包沿用通过验证的版本。[候选审查记录](../../notes/review.md)

课程实例运行记录显示 `t3.small`、Ubuntu 24.04.5 LTS、x86_64、系统 Python 3.12.3。账号归属依据用户提供的课程实例上下文。原端口教师测试退出码为 0。原始日志的 SHA-256 为 `e73367e3a7d5544d1311c03bf13faa26d8c21f4d8510e62e89da35aec3fe3cdc`。日志记录了键读取、覆盖、迁移和故障恢复的实际结果。独立 Verifier 核对了 80 次读取、三个阶段的键归属和 65 个 finger 条目。节点 15 故障后，节点 23 清空失效前驱，后继环恢复为 1 → 8 → 23 → 30 → 1。[实机环境](environment.txt) · [源码指纹](source-sha256.txt) · [原始输出](output_dht.txt) · [独立验证](verification.md)

此确切 ZIP 已满足准备提交的要求。审查范围内无未解决的 Critical、Major 或 Minor 问题。Blackboard 提交由用户办理。
