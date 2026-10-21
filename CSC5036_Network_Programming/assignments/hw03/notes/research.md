# Research: hw03 starter

Date: 2026-10-21. Scope: internal codebase. Baseline: 900f713 + unchanged original ZIP.

## Question / Scope

定位 TODO 和线程/UDP 调用路径；不查其他学生代码或外部库。

## Codebase Findings

- `src/Assignment-3/main.c:12` CLI 初始化与输入主线程；四处 TODO 补共享状态和发送。
- `src/Assignment-3/server.c:13` 接收线程与分发；QUERY 先去重，再查目录，再判断 TTL。
- `src/Assignment-3/utils.h:46` 原生 packet ABI；ID 数组 128、邻居 16、字符串 64；转发保留源 IP、监听端口、ID。
- `src/Assignment-3/network.c:60` 接收返回 UDP 真实发送者 IPv4。发送使用临时 socket，监听端口需由 packet 携带。
- `src/Assignment-3/network.c:17` 地址函数不可重入，需锁保护；不修改 helper。
- `src/Assignment-3/utils.c:115` 目录查找早返回资源问题位于非 TODO，保留并记录。

## Synthesis

只填 TODO、增辅助函数和日志条件。首个接收节点为空 hostname QUERY 填实际发送者 IP，此后保留源地址，响应直回源；显示 RESPONSE 的实际发送 IP。服务绑定完成后用条件变量唤醒发送 CONNECT 的主线程。

## Sources

教师原文 Basic Requirements、Objectives、Three-Party Example、Grading Criteria Parts、Submission；原 ZIP 全 15 条目。详细计划见 plan.md。
