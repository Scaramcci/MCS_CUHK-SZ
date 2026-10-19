# 01 数据库基础：中文学习笔记

CSC5041 · 第一次课堂测验复习 · 2026-10-19

## 阅读说明与学习目标

本篇对应数据库基础，不提前展开 ER 作图、关系代数或 SQL 查询技巧。主要依据教师导论课件第 17–57 页，页码按 PPT 幻灯片顺序计数。第 7、8 节是教学计划第 1 页明确列出、但导论 PPT 未充分展开的补充讲解，不能当作教师课件原文。文中的例子用于解释概念，并非真实考试题或实测结果。

学完后，应能区分数据、数据库、DBMS 和数据库系统；解释文件方式的局限；区分模式与实例；说明设计层次、三级模式和数据独立性；按功能读懂 DBMS 组件图。

## 1. 四个基础概念

来源：导论第 17–18、33、41、45 页。

| 概念 | 定义 | 学生选课系统中的例子 |
|---|---|---|
| 数据 Data | 可以记录、具有隐含意义的已知事实 | 学号 S01、姓名 Amy、课程 CSC5041 |
| 数据库 Database | 相互关联、描述现实世界某一部分的数据集合 | 学生、课程、选课记录的集合 |
| 数据库管理系统 DBMS | 支持创建、维护、查询和管理数据库的软件 | PostgreSQL 等数据库管理软件 |
| 数据库系统 Database system | 按课件的简化定义，数据库与 DBMS 的组合 | 选课数据及管理这些数据的 DBMS |

**数据库保存数据，DBMS 管理数据。** SQL 是与关系数据库交互的语言，不是数据库或 DBMS。应用程序通过 DBMS 读写数据；例如选课网页属于应用程序，不等同于 DBMS。

“相互关联”不要求每条记录直接连接所有其他记录，而是指数据共同描述一个有意义的应用领域。

### 结构化与非结构化数据

来源：第 34 页。

- **结构化数据 Structured data**：具有预先规定的组织方式，例如每条学生记录包含学号、姓名、专业。
- **非结构化数据 Unstructured data**：没有按固定记录模式组织，例如自由文本、录音、图片；分析前通常需要额外处理。

“非结构化”不是“完全没有信息或内部结构”；“放在电脑文件里”也不代表它就是关系表。

## 2. 为什么不直接用文件管理所有数据？

来源：第 35–40 页。

课件的选课例子使用三个文件：

```text
STUDENT(name, id, major)
COURSE(code, name, department)
SELECTION(student_id, course_code, term)
```

想判断 Amy 是否选了一门课，需要先从学生文件得到她的学号，再到选课文件匹配学号、课程和学期。文件本身可以保存这些信息，困难在于每个应用都要反复实现访问、约束、并发和恢复逻辑。

| 文件方式的问题 | 含义 | 说明例子 |
|---|---|---|
| 数据冗余 Redundancy | 同一事实被重复保存 | 多个部门各存一份学生地址 |
| 数据不一致 Inconsistency | 同一事实的副本互相冲突 | 地址只在一个文件中更新 |
| 访问困难 | 新查询需要新的程序或处理逻辑 | 每增加一个统计需求就重新编写文件处理代码 |
| 数据分散/隔离 Data isolation | 数据分散在不同文件和格式中，难以统一访问 | 学生资料是 CSV，课程资料是另一种格式 |
| 完整性问题 Integrity problems | 业务约束散落在程序里，难以统一维护 | 一段程序检查余额非负，另一段忘记检查 |
| 原子更新困难 | 多步更新可能只完成一部分 | 转账扣款成功、入账前系统崩溃 |
| 并发访问问题 | 多个用户的操作互相干扰 | 两次取款读到相同旧余额，后写覆盖先写 |

**冗余可能导致不一致，但重复存储并不意味着此刻一定存在冲突。** 课件强调消除不必要的冗余；实践中有目的、受控制的复制与任意重复不同。

这里的 **data isolation 指文件和格式造成的数据分散**，不要与后续事务章节的 isolation 混淆。

### 两个必须能讲清的例子

**转账与原子性 Atomicity**：从 A 转出 100 元、向 B 转入 100 元构成一个整体。要么两步都生效，要么失败后撤销已做的部分，不能只扣不加。

**并发与丢失更新 Lost update（术语补充）**：初始余额 100。两个操作都读取 100，各取 50，随后都写入 50。若两次取款均被接受，正确余额应为 0，最终却为 50。问题来自操作交错和旧值覆盖，不能仅靠一次“余额是否足够”的检查解决。

本篇只理解问题；并发控制和恢复算法留待后续课程。

## 3. DBMS 提供什么？

来源：第 41–42、44、47–48 页。

DBMS 支持定义数据结构、构建和装载数据库、查询数据、插入/删除/修改数据，以及管理访问。

| 能力 | 需要理解的作用 |
|---|---|
| 数据独立性 Data independence | 降低应用对底层数据表示和存储的依赖 |
| 高效访问 Efficient access | 由数据库机制支持数据查询和更新，而非让每个应用手写文件扫描 |
| 完整性 Integrity | 通过已声明的约束维持有效数据状态 |
| 安全性 Security | 控制谁可以读取或修改哪些数据 |
| 数据管理 Administration | 集中管理结构、权限及运行维护 |
| 并发与恢复 Concurrency and recovery | 协调共享访问，并在故障后恢复到一致状态 |
| 减少开发工作 | 让应用复用共同的数据管理能力 |

**完整性与安全性不同**：阻止不合法的选课记录是完整性；阻止学生修改他人成绩是安全性。DBMS 提供机制，但业务规则仍需正确设计与配置。

课件还提出及时响应、可修改、健壮、多用户、安全等要求。这些是系统目标，不表示使用数据库就会自动满足所有性能或正确性要求。

## 4. 数据模型、元数据、模式与实例

来源：第 50、53 页；元数据说明结合第 56 页结构图。

### 数据模型 Data model

数据模型是一套描述数据库结构的概念和规则。它回答“可以用什么结构表达数据”，而不是某个时刻具体存了哪些记录。

| 层次 | 关注点 | 例子 |
|---|---|---|
| 高层/概念模型 Conceptual model | 应用中的实体、属性和关系 | ER 模型 |
| 实现/记录模型 Implementation or record-based model | 可用于数据库逻辑实现的数据结构 | 关系、层次、网状模型 |
| 低层/物理模型 Physical model | 记录格式、存储组织、访问路径 | 记录如何排列、如何定位 |

“关系模型”是一类模型；“学生表包含哪些列”是某个数据库采用该模型得到的模式；“表里当前有哪些学生”是实例。

### 模式 Schema 与实例 Instance / state

```text
模式：Student(sid, name, major)

时刻 t1 的实例：
(S01, Amy, CS)
(S02, Ben, Math)

时刻 t2 的实例：
(S01, Amy, CS)
(S02, Ben, Math)
(S03, Chen, CS)
```

- 插入第三名学生：**实例变化，模式不变**。
- 将 Amy 的专业改成 Math：**实例变化，模式不变**。
- 给 Student 增加 email 属性：**模式变化**。
- 表已经定义但没有记录：存在模式，对应一个空实例。

**元数据 Metadata 是描述数据的数据**，如表名、列名、类型和约束；系统目录/数据字典保存这类描述，供 DBMS 使用。学生姓名 Amy 是业务数据，不是元数据。

## 5. 数据库设计的三个阶段

来源：第 54 页。

| 阶段 | 主要问题 | 选课例子 |
|---|---|---|
| 概念设计 Conceptual design | 应用需要表达什么事物和业务规则？ | 有学生、课程以及选课关系 |
| 逻辑设计 Logical design | 如何用目标数据模型表示？ | 转换为 Student、Course、Selection 等关系及约束 |
| 物理设计 Physical design | 如何实际存储并高效访问？ | 选择文件组织、索引和存储安排 |

不要在需求尚未弄清时直接从磁盘格式开始设计。概念设计也不是“开始填写具体记录”。

**这三个设计阶段与第 7 节的三级模式有关，但不是同一个分类。** 设计阶段描述工作过程；三级模式描述数据抽象和接口层次。尤其不要把“三个设计阶段”当作“三模式”的标准答案。

## 6. 数据库语言与用户

来源：第 49、55 页。

### DDL 与 DML

| 类别 | 用途 | 识别用的示例，SQL 语法后续再学 |
|---|---|---|
| DDL：Data Definition Language | 定义或修改数据库结构和约束 | CREATE TABLE、ALTER TABLE、DROP TABLE |
| DML：Data Manipulation Language | 查询、插入、删除、修改数据 | SELECT、INSERT、DELETE、UPDATE |

本课导论采用广义 DML，包括查询；不要因为其他资料把 SELECT 单列为 DQL 就认为课件分类错误。

**声明式/非过程式 Declarative / non-procedural**：说明想要什么结果，让 DBMS 决定如何执行。例如“返回 CS 专业学生的姓名”。

**过程式 Procedural**：给出完成任务的操作过程。例如逐条读取学生记录、检查专业、输出姓名。SQL 查询通常是声明式的，但课程后面会学习 PL/pgSQL 的变量、分支和循环。

### 谁使用数据库？

| 用户 | 职责 |
|---|---|
| DBA：Database Administrator | 管理模式、安全与授权、可用性、故障恢复和性能调优 |
| 应用程序员 Application programmer | 根据应用需求编写访问数据库的程序 |
| 最终用户 End user | 使用查询工具或应用程序完成业务任务 |

DBA 与应用程序员是职责不同，不意味着现实组织中绝对不能由同一人承担。

## 7. 三级模式架构 Three-schema architecture【补充】

范围依据：教学计划第 1 页 Week 1。概念定义参考下方补充来源；不是 PPT 的逐页摘录。

| 层次 | 描述什么 |
|---|---|
| 外模式 External schema | 某类用户或应用所见的数据视图，可有多个 |
| 概念模式 Conceptual schema | 数据库整体的逻辑结构，包含数据及约束 |
| 内模式 Internal schema | 数据的物理存储组织和访问方式 |

上下层通过映射联系；外模式可以隐藏数据，也可以提供计算后的表示。各用户视图并不意味着各自保存一份独立数据库。

本节核心定义参考 [UCT 数据库课程第 1 章](https://www.cs.uct.ac.za/mit_notes/database/htmls/chp01.html) 的 “ANSI/SPARC three-level architecture”。

**贯穿例子（本笔记自编）**：教务员需要完整选课资料，学生只需要自己的选课清单，这是不同外模式。Student、Course、Selection 及其约束构成整体逻辑结构。底层的文件组织和访问路径属于内模式。

注意：这里的三级模式不是应用部署中的“界面层、业务层、数据库层”。后者是另一种架构分类。

## 8. 数据独立性 Data independence【补充】

范围依据：教学计划第 1 页及导论第 42 页。

| 类型 | 允许哪一层改变？ | 希望哪一层保持不变？ |
|---|---|---|
| 物理数据独立性 Physical data independence | 内模式 | 概念模式及其上层应用接口 |
| 逻辑数据独立性 Logical data independence | 概念模式 | 外模式及使用它们的应用 |

映射需要随下层变化而调整。数据独立性不表示所有结构变化都能自动兼容。

定义参考 [Emory 的三级模式课程材料](https://www.cs.emory.edu/~cheung/Courses/377/Syllabus/1-files/3-schemas.html)；物理层与逻辑层分离亦见 [Oracle Database Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/introduction-to-oracle-database.html)。

### 如何判断？

**例 A（自编）**：调整底层文件组织，Student 的逻辑定义和应用查询保持不变。改变的是物理存储，因此体现物理数据独立性。

**例 B（自编）**：原来的学生逻辑结构拆成基本信息和联系信息两部分，通过更新视图映射，旧应用仍看到原先的学生信息接口。改变的是整体逻辑结构，因此体现逻辑数据独立性。前提是旧接口需要的信息仍能得到，不能假定任意拆表都无影响。

**例 C（自编）**：给 Amy 修改电话号码只是数据内容变化，不是逻辑数据独立性的例子。

记忆顺序：**用户视图 → 整体逻辑结构 → 物理存储**。先判断变化在哪层，再判断上层是否被隔离。

## 9. 读懂 DBMS 组件图

来源：导论第 56 页，已查看原图。以下为功能性概括，不是对真实产品固定执行顺序的保证。

| 图中组件 | 基本职责 |
|---|---|
| DDL compiler | 处理结构定义，将相关描述提供给系统目录 |
| System catalog / data dictionary | 保存数据库结构等元数据 |
| Query compiler | 处理查询，使其成为可供后续执行的表示 |
| Query optimizer | 选择合适的查询执行方案 |
| Runtime database processor | 在运行时处理数据库请求 |
| Stored data manager | 管理底层数据访问和 I/O |
| Concurrency control / backup / recovery subsystems | 协调并发，支持备份与故障恢复 |

对交互式查询，可用下面的简化流程理解：

```text
用户查询 → 查询编译 → 优化 → 运行时处理 → 数据访问 → 返回结果
                            ↕
                      系统目录提供元数据
```

原图还画出了应用程序的预编译、DML 编译和宿主语言编译路径。理解它们是不同入口即可，不需要在本篇展开编译器实现。

**两个视角分开记**：三级模式讨论“数据怎样分层描述”；组件图讨论“哪些软件模块处理请求”。

## 10. 数据库类型：掌握分类，不背实时排名

来源：第 20、51–52 页。

关系数据库以关系/表为主要组织方式；课件还列出键值、文档、图和列族等类型。课件中的例子包括 PostgreSQL、MySQL（关系），Redis（键值），MongoDB（文档），Cassandra（列族）。这些用于识别模型，不构成最新市场排名或完整产品能力描述。

NoSQL 不等于“没有结构”，关系数据库也不只是一堆互不关联的电子表格。当前测验的后续复习以关系数据库为主。

## 11. 易混点速查

| 容易混淆 | 正确区分 |
|---|---|
| Database / DBMS | 数据集合 / 管理该集合的软件 |
| Schema / instance | 结构描述 / 某时刻实际内容 |
| Data model / schema | 描述结构的概念体系 / 用它定义的具体数据库结构 |
| Metadata / data | 对结构等信息的描述 / 应用领域中的事实 |
| Redundancy / inconsistency | 重复存储 / 副本发生矛盾 |
| Integrity / security | 数据是否符合规则 / 谁有权访问和操作 |
| DDL / DML | 定义结构 / 查询和修改内容 |
| 设计阶段 / 三级模式 | 设计工作过程 / 数据抽象层次 |
| Physical / logical independence | 存储变化隔离 / 整体逻辑结构变化隔离 |
| 原子性 / 并发 | 单个工作整体是否完整生效 / 多个操作如何交错共享数据 |

## 12. 复习清单与英文表达

以下是自我复习目标，不是正式模拟测试，也不代表官方分值。

- [ ] 不看笔记区分四个基础概念，并各给一个例子。
- [ ] 用因果关系解释文件方式的至少四个问题。
- [ ] 讲清转账失败和并发取款分别说明什么问题。
- [ ] 判断插入记录、修改属性值、增加列分别改变模式还是实例。
- [ ] 区分数据模型、设计阶段和三级模式。
- [ ] 对给定变化指出其层次，并解释物理或逻辑数据独立性。
- [ ] 用功能说明 DDL、DML、DBA 及核心 DBMS 组件。

可用于英文简答的表达：

> A database is a collection of related data, whereas a DBMS is the software used to create and manage it.

> A schema describes the database structure; an instance contains the actual data at a particular time.

> Physical data independence allows storage changes without changing the conceptual schema.

> Logical data independence allows conceptual-schema changes while preserving existing external interfaces through suitable mappings.

> Atomicity means that a transaction's changes take effect as a whole or do not take effect at all.

## 来源与整理记录

- 教师导论：[Week 1A - IntroductionNEW.pptx](../../slides/Week%201A%20-%20IntroductionNEW.pptx)，主要第 17–57 页；组件图为第 56 页。
- 教师计划：[CSC5041_Teaching_Plan.pdf](../../slides/CSC5041_Teaching_Plan.pdf)，第 1 页 Week 1 与 Test 1。
- 补充网页仅用于第 7–8 节的架构与独立性定义；自编例子已明确标注。补充资料不决定教师实际考查深度。
- 整理者：Codex 当前会话；已自查来源页码及双语对应，未进行独立 Reviewer 审查。原件未修改；本篇为个人学习资料，不是提交作业或官方题库。
- 输入版本：导论 SHA-256 `d36c2d15a77083931046168738d794558c2e9821d452701f64ef524e45e87a7c`；教学计划 SHA-256 `b62c7356961bf10585f2e7d5fbf29bcb8401970a99d09d80fe6675fa63cea463`。
- 下一步：按用户指示继续下一部分笔记；全部笔记完成后，再依据 Tutorial 1、Tutorial 2 各生成一份英文测试题。当前尚未生成测试题。
