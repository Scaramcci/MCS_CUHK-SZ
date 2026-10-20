# 03 关系模型与完整性约束：中文学习笔记

CSC5041 · 第一次课堂测验复习 · 2026-10-19

## 阅读说明与学习目标

本篇接续 [02 ER 概念建模](02_er_modelling_zh.md)，对应教学计划第 1 页 Week 3 的 “The Relational Data Model” 与 “integrity constraints”。主要依据教师 [Lecture2A.pptx](../../slides/Lecture2A.pptx) 第 4–32 页；下文未注明文件的页码均按该 PPT 的幻灯片顺序计数。

学完后，应能读懂关系模式和实例，解释关系的集合性质，找出各类键及外键引用方向，区分键约束、实体完整性与参照完整性，并判断插入、删除、修改是否破坏约束。第 33 页开始的 ER 映射留到 04；关系代数留到 05；SQL 实现细节留到 06。

文中的学生选课数据是**自编教学示例**，不是真实学生资料、运行结果或考试题。对课件简化表述的辨析会明确标出。

## 1. 从 ER 模型走到关系模型

来源：第 4–7、32 页。

02 用实体、属性和关系表达应用含义；关系模型用一组相互关联的**关系 relation** 组织数据。这里的 relation 可直观理解为表，**不是 ER 图中连接实体的 relationship**。

| 数学术语 | 常见数据术语 | 含义 |
|---|---|---|
| Relation 关系 | Table 表 | 一组具有相同属性结构的元组 |
| Tuple 元组 | Row / record 行、记录 | 某组属性的一组取值 |
| Attribute 属性 | Column / field 列、字段 | 被命名的性质 |
| Domain 域 | Allowed values 允许值集合 | 该属性允许取得哪些值 |

例如 `Student(sid, name, email)` 是一个关系模式；`(S01, Amy, amy@example.test)` 是按该属性顺序书写的一个元组。Student 与 Course 之间的选课联系也可以由一个单独的关系 Enrolment 表示，不是靠把两张表放在相邻位置表示。

## 2. 模式、实例、度与基数

来源：第 8、32 页；以下形式化记法与 degree / cardinality 术语是解释性补充。

### 单个关系

```text
关系模式：Student(sid, name, email)

一个关系实例：
sid   name   email
S01   Amy    amy@example.test
S02   Ben    ben@example.test
```

关系模式规定关系名、属性及其域；关系实例是某一时刻该结构下的实际元组集合。常写作 `R(A1, ..., An)` 与 `r(R)`，或在上下文清楚时简写为 `r`。

不考虑 NULL 的经典定义中，每个元组从各属性域各取一个值，因此 `r ⊆ dom(A1) × ... × dom(An)`。符号只说明“每列从哪里取值、实例是哪些组合的集合”，不要求把所有可能组合都存进去。

| 术语 | 数什么？ | 上例 |
|---|---|---|
| 度 Degree / arity | 属性数 | 3 |
| 基数 Cardinality | 当前元组数 | 2 |

空实例仍有模式：Student 暂时没有记录时，度仍为 3，基数为 0。这里的 cardinality 是**当前关系有多少行**；02 的 ER cardinality ratio 是**业务规则允许关联多少个对方实体**，不要混用。

### 整个数据库

第 32 页将关系数据库模式定义为**一组关系模式及一组完整性约束**。因此仅列 Student、Course、Enrolment 的列名，还没有完整写出数据库模式；也要说明主键、外键等规则。

数据库状态包含各关系的实例；全部相关约束都满足时，才是合法状态。以下讨论的“非法状态”用来说明操作为何应被拒绝，并不表示系统应该保存它。

## 3. 一个关系的基本性质

来源：第 8–10 页；SQL 对照另见 SQLpart1 第 31–32 页。

| 性质 | 正确理解 |
|---|---|
| 元组无顺序 | 交换两行的显示位置，不会得到另一个关系 |
| 元组不能完全重复 | 经典关系是集合，相同元组不作为两个不同元素出现 |
| 每个属性位置取一个原子值 | 本课的平面关系模型不直接保留 ER 复合或多值属性 |
| 属性按名称区分 | 同一关系的属性名需要能区分各列；不同关系可有同名属性 |
| 重排显示列不改变含义 | 必须把列名和各自的值一起移动，不能只随意交换元组中的值 |

### 列无语义顺序，不等于元组值可以乱放

第 10 页将 PLAYER 的列连同列名与值一起重排，得到相同关系。用命名属性理解时，重要的是“哪个值属于哪个属性”。

但在 `Student(sid, name)` 下，`(S01, Amy)` 与 `(Amy, S01)` 不一样：按位置书写元组时，位置必须与所声明的属性顺序对应。重排展示与交换属性值是两件事。

### 原子值与 ER 属性

02 中的 `address(city, street, postcode)` 是复合属性，`{phoneNumber}` 是多值属性。第 8 页明确排除在本课平面关系中直接使用这两种属性结构。原子性取决于当前模型所采用的域与操作，不是指一个字符串在字符层面无法拆开。具体怎样转换留到 04。

### 经典关系与 SQL 表

经典关系遵循集合语义；SQLpart1 第 31–32 页另指出 SQL 可以保留重复，查询结果可用 DISTINCT 去重。因此不能把“关系无重复”直接当作“任何 SQL 表都自动禁止重复”的结论。SQL 语法与具体约束声明留到 06。

## 4. 超键、候选键与主键

来源：第 12–15 页；与 02 第 4 节衔接。

| 键 | 条件 | 自编例子：假定 sid 与 email 分别唯一且必填 |
|---|---|---|
| 超键 Superkey | 能唯一确定一个元组 | `{sid}`、`{email}`、`{sid, name}` |
| 候选键 Candidate key | 是超键，且没有多余属性 | `{sid}`、`{email}` |
| 主键 Primary key | 被选定的一个候选键 | 选择 `{sid}` |
| 复合键 Composite key | 由多个属性组成 | Course 的 `{dept, courseNo}`，见第 8 节 |

最小性检查的是**删掉属性后还能否保证唯一**，不是“在全体候选键中挑属性数最少的”。一张表可以有多个候选键，选定一个主键也不意味着其他候选键失去唯一性要求。

第 13 页以“没有两人同名”为**显式假设**，才把 PLAYER 的 Name 当候选键；不能从示例的三个人恰好不同名推导现实中姓名总是唯一。

### 为什么无重复元组还需要键约束？

```text
(S01, Amy, amy@example.test)
(S01, Ada, ada@example.test)
```

这两个完整元组不同，集合性质并不排除它们同时出现。但是它们具有相同 sid，若 sid 是主键，就违反键约束。**无完全重复行**与**指定键不能重复**是不同要求。

### 第 15 页的 `2^n − 1` 怎么理解？

该页列出所有非空属性子集。对 n 个属性，非空子集确实有 `2^n − 1` 个，**但不是每个子集都能唯一识别元组**，所以不能将它当作任意关系的超键数公式。

**自编反例**：R(A,B,C) 只有候选键 `{A}`，B、C 及 `{B,C}` 都不保证唯一。超键只有 `{A}`、`{A,B}`、`{A,C}`、`{A,B,C}`，共 4 个，不是 7 个。只有在每个单属性本身都能作键等额外条件下，所有非空子集才全是超键。

## 5. 外键：方向、重复值与复合引用

来源：第 16–19 页。

外键 Foreign key 是引用方关系中的一个或一组属性，用其取值引用被引用关系的键。课件本节采用引用**主键**的定义；本篇按这一范围讲解，不把它扩展成所有 SQL 系统的完整规则。

```text
引用方 referencing relation                 被引用方 referenced relation
Enrolment.sid                  ─────────→   Student.sid
Enrolment.(dept, courseNo)      ─────────→   Course.(dept, courseNo)
```

核对外键时，要写清楚**引用方属性组 → 目标关系的键属性组**。不要求两边属性名相同，但对应域应兼容；仅仅都是字符串或列名相同，不能自动成立外键。

### 外键自身不要求唯一

多条选课记录可以有相同 sid，表示同一名学生选了多门课。Student.sid 必须唯一，Enrolment.sid 作为外键则可以重复。外键也可以同时是主键的一部分，这两个身份不冲突。

### 复合外键必须作为一个组合匹配

若 Course 中只有 `(CS,101)` 和 `(Math,201)`，那么 `(CS,201)` **不能**引用它们。虽然 CS 和 201 分别出现过，但它们没有在**同一个目标元组的对应键位置**共同出现。

课件第 19 页中的 `(Department, Degree)` 也是**一组复合外键**，不是 Department 和 Degree 各自单独引用 COURSE 的两个外键。遗漏任一部分，可能无法确定具体课程。

## 6. NULL 与外键的边界

来源：第 18、20、22、30 页；NULL 的未知/不适用含义已在 02 解释。

| 所在位置 | 本篇采用的规则 |
|---|---|
| 主键的任何组成属性 | 不能为 NULL，即使其他组成属性已有值 |
| 非主键属性 | 是否允许 NULL 取决于该属性的必填约束 |
| 可空外键 | 只有在其他约束也允许时，才可用 NULL 表示暂不引用 |
| 同时属于主键的外键属性 | 不能因为它也是外键就放宽主键非空规则 |

**课件第 18、22 页的复合外键规则是：要么全部 NULL，要么全部非 NULL 且完整匹配目标键。** 本篇按这个明确给出的课堂规则判断，不将其泛化为所有 SQL 实现的默认行为。

**自编小例子**：给定 `Plan(planID, dept, courseNo)`，主键为 planID，`(dept,courseNo)` 是可空且遵守上述规则的外键，引用第 5 节的 Course。

| 外键值 | 判定 |
|---|---|
| `(CS,101)` | 合法，完整匹配 |
| `(NULL,NULL)` | 合法，假定两列都允许缺失且没有其他必填要求 |
| `(CS,NULL)` | 不合法，不符合本课“全空或全非空”的规则 |
| `(CS,201)` | 不合法，不存在这个组合 |

**“参照完整性允许空引用”不等于“业务上允许没有关联”。** 若要求每条记录必须引用目标，还需要禁止外键为空。02 的全参与约束不能只靠“有一个可空外键”完整表达。

## 7. 三类完整性约束检查什么？

来源：第 20–22、32 页。

| 约束 | 要防止的问题 | 典型违规 |
|---|---|---|
| 键约束 Key constraint | 不同元组共享同一个候选键值 | 两名学生使用相同 sid；或 sid 不同但唯一 email 重复 |
| 实体完整性 Entity integrity | 主键不能完整识别一个元组 | 复合主键中某一属性为 NULL |
| 参照完整性 Referential integrity | 外键引用不存在的目标键 | 选课记录引用数据库中没有的学生 |

“主键唯一”属于键约束，“主键非空”属于实体完整性。它们共同支持标识，但答题时应分别说明。一个操作也可能同时违反多条规则；不要找到第一项就认定没有其他问题。

### 域约束和业务约束【解释性补充】

第 6、8 页的域规定值的范围。例如 grade 必须取规定等级或允许缺失，整数编号不能随意填自由文本。其他业务规则还可能要求费用非负、开始日期不晚于结束日期。

本篇三类约束是课件第 20 页重点列出的约束，**不是数据库全部可能约束的清单**。仅主键和外键全部合法，也不保证业务状态一定正确。

## 8. 贯穿例子：先明确模式、约束与初始状态

以下全部为自编教学例子。模式是已给定输入，不在这里演示 ER 映射。

### 模式与约束

| 关系模式 | 主键 PK | 其他候选键 | 外键 FK |
|---|---|---|---|
| Student(sid, name, email) | `{sid}` | `{email}` | 无 |
| Course(dept, courseNo, title) | `{dept, courseNo}` | 本例未指定其他候选键 | 无 |
| Enrolment(sid, dept, courseNo, term, grade) | `{sid, dept, courseNo, term}` | 本例未指定其他候选键 | `{sid} → Student.sid`；`{dept,courseNo} → Course.(dept,courseNo)` |

本例规定：Student 的三个属性都必填；课程三个属性都必填；sid、email、dept、title、name、term 是字符串，courseNo 是正整数；term 允许 `2026F`、`2027S`；grade 允许 A、B、C、D、F 或 NULL。NULL 表示尚未获得成绩。所有主键组成属性均非空。

一名学生可以选多门课，也可在不同 term 再选同一门课；**同一学生、同一课程、同一 term 最多一条选课记录**。这正是 Enrolment 四属性主键表达的规则。dept 或 courseNo 单独都不能唯一识别 Course。

### 初始状态

Student：

| sid | name | email |
|---|---|---|
| S01 | Amy | amy@example.test |
| S02 | Ben | ben@example.test |

Course：

| dept | courseNo | title |
|---|---|---|
| CS | 101 | Database Basics |
| Math | 201 | Linear Algebra |

Enrolment：

| sid | dept | courseNo | term | grade |
|---|---|---|---|---|
| S01 | CS | 101 | 2026F | A |
| S02 | CS | 101 | 2026F | NULL |

这个状态满足本例列出的约束：Student 两个候选键都唯一；所有主键完整非空；每个外键组合都能找到目标。Enrolment.sid 重复与否不决定它是否满足参照完整性；关键是它是否引用有效学生。

**下文每个操作都从这个初始状态独立判断，不串联执行。** 以下是根据规则进行的静态推演，未在数据库中实际运行。

## 9. 插入：检查新元组与被引用目标

来源：第 21–28 页；以下操作使用第 8 节自编数据。

| 拟执行操作 | 判定与原因 |
|---|---|
| 向 Student 插入 `(S01, Ada, ada@example.test)` | 不合法：sid 已存在，违反键约束 |
| 向 Student 插入 `(S03, Chen, amy@example.test)` | 不合法：email 候选键重复，不能只检查主键 |
| 向 Enrolment 插入 `(S03, CS, 101, 2026F, A)` | 不合法：Student 没有 S03，违反参照完整性 |
| 向 Enrolment 插入 `(S01, CS, 201, 2026F, B)` | 不合法：Course 没有 `(CS,201)`；不能拆开匹配 |
| 向 Enrolment 插入 `(S01, CS, 101, NULL, B)` | 不合法：主键组成属性 term 为 NULL，违反实体完整性 |
| 向 Enrolment 插入 `(S01, CS, 101, 2026F, B)` | 不合法：四属性主键已存在，即使 grade 不同也不能再插一行 |
| 向 Enrolment 插入 `(S01, CS, 101, 2027S, NULL)` | 合法：term 不同使主键不同，两组外键均有目标，grade 允许 NULL |

答题顺序可以固定为：**域与必填要求 → 所有候选键 → 主键非空 → 每组外键**。题目要求列出全部违规时，需要查完所有相关规则。

对照课件原例：第 24 页向 RESEARCHER 插入已存在的 Person#=2，说明键冲突；第 26 页向 COURSE 插入 `(Comp.Sci., NULL)`，说明复合主键不能缺一部分；第 28 页用不存在的 Supervisee=6 插入 ENROLMENT，说明引用目标缺失。

## 10. 删除：沿外键反向查找引用者

来源：第 29–30 页。

判断删除时，不只看被删元组自身是否合法，还要看**有没有其他元组引用它的键**。

| 从初始状态拟删除什么？ | 直接删除的影响 |
|---|---|
| Student 中 S01 | 有 Enrolment 引用 S01；若不处理这些引用，违反参照完整性 |
| Course 中 `(CS,101)` | 两条 Enrolment 引用它；若不处理引用，违反参照完整性 |
| Course 中 `(Math,201)` | 本例没有记录引用它，删除后仍满足已列约束 |
| Enrolment 中 S01 的那条记录 | 本例没有别的关系引用 Enrolment，删除后仍满足已列约束 |

因此“主键不能被删除”不正确；真正要查的是依赖关系和已声明的处理规则。

第 30 页讨论的处理思路包括：

- **拒绝删除**：保留被引用元组，避免产生悬空引用。
- **级联删除引用者**：删除相关元组，但还要检查它们是否继续被其他关系引用。
- **将引用设为 NULL**：只在外键允许为空且不违反其他约束时可行。
- **改成另一个有效引用**：新值必须符合域及全部相关约束，不能随意写一个占位编号。

在本例中，Enrolment 的两个外键属性组都包含在主键中，因此**不能用设为 NULL 处理它们**。级联或改引用也必须符合业务含义；不能默认数据库自动选择一种方案。

## 11. 修改：同时考虑旧值与新值

来源：第 31 页；最后一段为对课件适用范围的解释。

| 修改位置 | 需要检查什么？ | 本例 |
|---|---|---|
| 主键或其他候选键 | 新值是否重复；主键是否变空；旧键是否仍被引用 | 把 Student S01 的 sid 改为 S02 会键冲突；改为 S03 又会让原 S01 引用失去目标，除非同时妥善处理 |
| 外键 | 新的完整组合是否能匹配目标；是否允许 NULL；是否兼任主键 | 把 S01 那条选课的 courseNo 从 101 改为 201，会形成不存在的 `(CS,201)` |
| 非键属性 | 仍需检查域、必填和其他业务约束 | 把 grade 改为 Z，虽然没有改键，仍违反本例 grade 允许值规则 |

若将 S01 那条选课的 `(dept,courseNo)` 一起改为 `(Math,201)`，新的目标存在，且结果主键不与其他行重复，因此在本例约束下合法。**改变复合外键时，要检查变更后的整个组合。**

课件把修改主键类比为“删除旧键再插入新键”，便于记住要查旧引用和新值冲突；这是约束分析方法，不要求真的先删除学生再重新插入。

**课件措辞辨析**：第 31 页 “Not unless you're modifying the value of a key” 与 “all relational integrity constraints are to do with the key values” 应结合该页讨论的键相关约束理解。它们不能推广成“所有非键更新都安全”：域、必填要求及业务规则同样可能被非键更新破坏。

## 12. 易混点速查

| 容易混淆 | 正确区分 |
|---|---|
| Relation / ER relationship | 元组集合 / 实体之间的联系 |
| Schema / instance | 结构和规则 / 某时刻的内容 |
| Degree / cardinality | 属性数 / 当前元组数 |
| 关系的 cardinality / ER cardinality ratio | 实际行数 / 关联数量的业务上限 |
| 无完全重复元组 / 键唯一 | 整行不重复 / 指定属性组不能在不同行中重复 |
| Candidate key / primary key | 所有最小超键之一 / 被选定的一个候选键 |
| 主键 / 外键 | 标识本关系元组 / 引用目标关系的键；同一属性可兼任 |
| 外键值重复 / 悬空引用 | 多行引用同一目标通常允许 / 引用不存在的目标不允许 |
| 复合外键匹配 / 分别查每列 | 同一目标元组中整体匹配 / 分别存在不足以证明合法 |
| Key constraint / entity integrity | 唯一性 / 主键非空 |
| NULL / 0 / 空字符串 | 缺失标记 / 一个数字值 / 一个字符串值 |
| 约束允许的状态 / 业务完全正确 | 满足已声明规则 / 还取决于是否把需要的业务规则声明完整 |

## 13. 复习清单与英文表达

以下是自我复习目标，不是正式模拟测试或官方分值安排。

- [ ] 从一组表中指出 relation、tuple、attribute、domain、schema 和 instance。
- [ ] 给出关系的 degree 与 cardinality，并解释空实例。
- [ ] 说明交换显示列与交换元组值的区别。
- [ ] 区分无重复行、超键、候选键和主键。
- [ ] 解释为何不能无条件使用 `2^n − 1` 计算超键数。
- [ ] 标出每组外键的引用方向，整体核对复合外键。
- [ ] 分别解释键约束、实体完整性、参照完整性。
- [ ] 根据课件规则判断外键全空、部分空及非空不匹配情况。
- [ ] 从同一初始状态独立判断插入、删除与修改，说明具体冲突元组或缺失目标。
- [ ] 说明级联删除与设为 NULL 的前提，不把它们当作自动行为。

可用于英文简答的表达：

> A relation is a set of tuples defined over a collection of named attributes.

> A relation schema describes the structure; a relation instance contains the tuples at a particular time.

> A candidate key is a minimal superkey, and a primary key is a selected candidate key.

> Entity integrity requires every component of a primary key to be non-NULL.

> Referential integrity requires a non-NULL foreign-key value to match a referenced key value.

> A composite foreign key must match the corresponding key components in the same referenced tuple.

> Deleting a referenced tuple requires checking the tuples that refer to it.

## 来源与整理记录

- 教师主课件：[Lecture2A.pptx](../../slides/Lecture2A.pptx)，主要第 4–32 页。已读取文字并查看第 7、10、15、17、19、24、26、28–29、31 页原图，核对表头下划线、复合外键与操作例子；第 33–55 页的映射步骤不在本篇展开。
- 补充对照：[SQLpart1.pptx](../../slides/SQLpart1.pptx)，第 31–32 页，仅用于区分经典集合语义与 SQL 重复值；不在此教授 SQL 查询。
- 范围依据：[CSC5041_Teaching_Plan.pdf](../../syllabus/CSC5041_Teaching_Plan.pdf)，第 1 页 Week 3。degree/cardinality、域约束与业务约束的解释、自编模式与数据、课件措辞的限定均已与原文区分。
- 整理者：Codex 主会话。双语结构、相对链接与来源页码已自查；独立 Reviewer 结论以本轮交付消息为准。本篇没有执行数据库操作；操作结果为显式约束下的静态推演，代码/实验验证 N/A，不创建 submission，教师原件及 01、02 未修改。
- 输入版本 SHA-256：Lecture2A `cecf28254342cf35e9a0b1b86a007fba728ed17a900e9e05182f2f2616081ee0`；SQLpart1 `aa28c989fb3674e780418c78c483bba20ff5a50b7da067b0341e60410a68c8ed`；syllabus 教学计划 `31380a7fe6504e46541b6db0bb2f24859c69188bfeb9681dca73354ebeb68295`。
- 下一步：按用户指示整理 04 ER 到关系模式的映射；全部笔记完成后再依据两套 Tutorial 编写两套英文练习题。
