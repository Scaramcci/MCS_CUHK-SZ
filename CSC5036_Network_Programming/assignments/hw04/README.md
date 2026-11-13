# hw04 — Chord DHT

教师要求：[Assignment-4.md](requirements/Assignment-4.md)；[原始代码包](requirements/Assignment-4.zip)。截止 2026-11-15 23:59（UTC+8）。沿用课程目录 CSC5036，原文课程号 CSC4303。

## 状态

**Ready** · [最终提交 ZIP](submission/226040255_hw4.zip) 已通过[实机独立验证](results/ec2-20261112103924264Z/verification.md)和[最终包审查](results/ec2-20261112103924264Z/final-review.md)。

2026-11-12 已在用户提供的课程 EC2 实例运行教师测试。实例为 t3.small，Ubuntu 24.04.5 LTS x86_64，系统 Python 3.12.3。运行与证据见[实机记录](results/ec2-20261112103924264Z/run.md)。

代码在 [src/Assignment-4/chord_node.py](src/Assignment-4/chord_node.py)。仅替换 13 个 TODO 的异常占位并增加必要辅助方法；原有初始化、网络方法、测试文件和测试端口不变。不需要额外 Python 库或报告。

## 运行

从作业目录运行本地补充检查（需本机 TCP socket 权限，先确认教师端口未被占用）：

```bash
python3 tests/run_checks.py
```

测试依次运行原件一致性检查、未经修改的教师测试和补充断言，保存独立目录到 results/selftest-*。本地测试用合成键值，只用于协议检查；并非云端运行证据。教师脚本的随机发送节点不固定，额外断言固定输入。原测试会吞掉异常，必须检查实际输出，不能仅凭退出码或结束横幅判断通过。

实机复现可按[操作指南](notes/EC2实机操作.md)上传已审查的 ZIP 并解压，在 Assignment-4 目录运行系统 Python。

```bash
python3 --version
python3 test_dht.py > output_dht.txt 2>&1
cat output_dht.txt
```

节点通过 127.0.0.1 通信。在日志中核对每次存取、数据迁移及故障后的完整 finger table。

## 证据与交付

- [11 月 4 日本地候选包复审](notes/review.md)
- [本地独立验证](notes/verification.md)，包含 15 次远程重复迁移调用。
- [本地候选 ZIP](results/candidate/20261104T074144997572Z/226040255_hw4.zip) 与 [文件清单及哈希](results/candidate/20261104T074144997572Z/manifest.json)。
- [计划及代码梳理](notes/plan.md)
- [实现与自测记录](notes/implementation.md)
- [本机运行记录](results/selftest-20261104T074111219925Z/run.json)、[教师原始输出](results/selftest-20261104T074111219925Z/teacher.txt)、[补充断言输出](results/selftest-20261104T074111219925Z/assertions.txt)

提交物为 `226040255_hw4.zip`，内含 `Assignment-4/chord_node.py` 和教师原始 `Assignment-4/test_dht.py`。

保留教师网络代码的单次 recv(4096) 限制；未声称支持任意大 JSON 值、迁移时并发写的线性一致性、任意网络分区或数据副本恢复。已失败节点独有数据的恢复不属于本次加分要求。
