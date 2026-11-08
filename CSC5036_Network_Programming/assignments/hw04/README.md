# hw04 — Chord DHT

教师要求：[Assignment-4.md](requirements/Assignment-4.md)；[原始代码包](requirements/Assignment-4.zip)。截止 2026-11-15 23:59（UTC+8）。沿用课程目录 CSC5036，原文课程号 CSC4303。

## 状态

已实现必需功能及可选故障恢复；本机教师测试与补充断言通过。**尚未完成必需的 AWS Academy Learner Lab t3.small 实机运行，不能标为 Ready。** 用户正在查找实例连接信息。本地使用 Python 3.14.7，不能替代教师指定的 Python 3.12 / Ubuntu 24.04 AMD64。

代码在 [src/Assignment-4/chord_node.py](src/Assignment-4/chord_node.py)。仅替换 13 个 TODO 的异常占位并增加必要辅助方法；原有初始化、网络方法、测试文件和测试端口不变。不需要额外 Python 库或报告。

## 运行

从作业目录运行本地补充检查（需本机 TCP socket 权限，先确认教师端口未被占用）：

```bash
python3 tests/run_checks.py
```

测试依次运行原件一致性检查、未经修改的教师测试和补充断言，保存独立目录到 results/selftest-*。本地测试用合成键值，只用于协议检查；并非云端运行证据。教师脚本的随机发送节点不固定，额外断言固定输入。原测试会吞掉异常，必须检查实际输出，不能仅凭退出码或结束横幅判断通过。

教师环境运行步骤（尚未执行）：将 `src/Assignment-4/` 中两个 Python 文件复制至课程 Learner Lab 的单台 t3.small 实例，核对 Ubuntu 24.04、AMD64、系统 Python 3.12，进入该目录执行：

```bash
python3 --version
python3 test_dht.py > output_dht.txt 2>&1
cat output_dht.txt
```

需核对每次存取、数据迁移和故障后的完整 finger table。节点只通过 127.0.0.1 通信，不开放 5001–5010 入站端口。无需创建多台实例。实验完成后按课程要求停止实例。此说明不代表已启动、连接或运行 EC2。

## 证据与交付

- [独立候选包复审](notes/review.md)：新版代码和打包检查通过，仅待必需 Learner Lab 运行；旧候选勿用。
- [独立验证](notes/verification.md)：修复重复迁移 RPC 后，本地全套及 15 次远程重复调用检查通过；必需课程环境仍待运行。
- [本地候选 ZIP](results/candidate/20261104T074144997572Z/226040255_hw4.zip) 与 [文件清单及哈希](results/candidate/20261104T074144997572Z/manifest.json)。
- [计划及代码梳理](notes/plan.md)
- [实现与自测记录](notes/implementation.md)
- [本机运行记录](results/selftest-20261104T074111219925Z/run.json)、[教师原始输出](results/selftest-20261104T074111219925Z/teacher.txt)、[补充断言输出](results/selftest-20261104T074111219925Z/assertions.txt)

最终格式：`226040255_hw4.zip`，仅含 `Assignment-4/chord_node.py` 和原始 `Assignment-4/test_dht.py`。候选审查包留在 results/candidate/，待必需环境检查通过后再进入 submission/。不包含 README、日志、报告、额外测试或缓存。未上传 Blackboard，未提交或推送 Git。

保留教师网络代码的单次 recv(4096) 限制；未声称支持任意大 JSON 值、迁移时并发写的线性一致性、任意网络分区或数据副本恢复。已失败节点独有数据的恢复不属于本次加分要求。
