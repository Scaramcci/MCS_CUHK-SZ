# 05 关系代数：中文学习笔记

CSC5041 · 第一次课堂测验复习 · 2026-10-19

## 阅读说明与学习目标

本篇接续 [03 关系模型](03_relational_model_and_integrity_zh.md) 和 [04 ER 映射](04_er_to_relational_mapping_zh.md)，主要依据教师 [Relational_Algebra.pptx](../../slides/Relational_Algebra.pptx)，共 61 页。下文未注明文件的页码均指该 PPT 的幻灯片顺序。

范围对应教学计划第 1 页 Week 4；Tutorial 2 第 1 页 Question 1(a)(i)–(vi) 涉及选择投影、连接、集合运算、未参加任何课程、所有目标课程以及分组聚合。聚合虽不是经典基本关系代数的一部分，但课件第 58–59 页和 Tutorial 均有覆盖，故本篇一起整理。SQL 留到 06。

学完后，应能解释每个运算的输入与输出模式，从自然语言组合表达式，并识别错误连接、过早投影、同名混淆和除法候选范围问题。自编数据和结果是静态教学推演，不是真实数据、数据库运行结果或新的模拟卷。

## 1. 关系代数的记号与闭包

来源：第 2–4、55–61 页。

关系代数以关系为输入，产生新的关系，结果可以继续参与运算，这称为**闭包 closure**。课件将它称为过程式 DML：表达式给出逻辑运算的组合，而不是数据库底层必须照做的物理执行顺序。

| 运算 | 本篇写法 | 主要作用 |
|---|---|---|
| 选择 Selection | `σ_{condition}(R)` | 选行 |
| 投影 Projection | `π_{attributes}(R)` | 选列并去重 |
| 重命名 Rename | `ρ_{NewName(newAttributes)}(R)` | 区分关系角色或对齐属性名 |
| 并、交、差 | `R ∪ S`、`R ∩ S`、`R − S` | 合并、共有、左有右无 |
| 笛卡尔积 Product | `R × S` | 所有元组配对 |
| 条件连接 Theta join | `R ⋈_{condition} S` | 满足条件的元组配对 |
| 自然连接 Natural join | `R ⋈ S` | 所有同名属性相等，合并这些属性 |
| 除法 Division | `R ÷ S` | 与 S 中每个目标都关联的候选 |
| 分组聚合 Aggregation | `γ_{groups; aggregates}(R)` | 每组统计 |

本篇用代码块中的 `{...}` 表示下标，便于在 Markdown 中稳定阅读；`←` 表示给中间关系命名，不修改原始数据。关系/属性重命名不改变已有值，完整列重命名列表按原属性顺序一一对应。

**默认采用集合语义且例子不含 NULL**。π 会消除重复；没有隐含行顺序。SQL 的重复值、NULL 和三值逻辑不能不加说明地搬进这些经典运算。Tutorial 中含 NULL 的 grade 不影响只使用其他属性的表达式；NULL 查询语义留到 06。

## 2. 贯穿例子：先写清输入

以下是自编的简化选课数据库，**不是 Tutorial 原模式**：省去 term，Takes 只表示学生是否选过某门课。

```text
Student(sid, sname, major)          PK{sid}
Course(cid, title, dept, credits)   PK{cid}
Takes(sid, cid)                    PK{sid,cid}
Takes.sid → Student.sid; Takes.cid → Course.cid
```

Student：

| sid | sname | major |
|---|---|---|
| S1 | Amy | CS |
| S2 | Ben | Math |
| S3 | Amy | CS |
| S4 | Dana | Math |

Course：

| cid | title | dept | credits |
|---|---|---|---|
| C1 | Databases | CS | 4 |
| C2 | AI | CS | 3 |
| C3 | Linear Algebra | Math | 4 |

Takes：

| sid | cid |
|---|---|
| S1 | C1 |
| S1 | C2 |
| S2 | C1 |
| S2 | C3 |
| S3 | C3 |

S1、S3 同名，故**姓名不是标识**。S3 的专业是 CS，却只选了 Math 课程，故**学生专业与课程院系不是同一个条件**。S4 没有选课，后面判断“从未”和零记录情况时需要保留他。

## 3. 选择 σ：筛选元组，保留全部属性

来源：第 5–10、18 页。

```text
σ_{dept='CS' ∧ credits>3}(Course)
```

结果模式仍是 `(cid,title,dept,credits)`，本例只含 `(C1,Databases,CS,4)`。选择不自动删列，也不修改被保留元组的值。条件可以比较属性与常量，或比较两个属性，并用 `∧`、`∨`、`¬` 组合。

连续选择可合并，并可交换顺序：

```text
σ_{p}(σ_{q}(R)) = σ_{p∧q}(R) = σ_{q}(σ_{p}(R))
```

前提是相关条件都对 R 的属性有定义。本例“CS 课程且超过 3 学分”可用两个连续选择实现；它不等于“CS 课程或超过 3 学分”。

**不要混淆 SQL 的 SELECT 与关系代数的 selection**：σ 选行，SQL 的 SELECT 列表主要决定输出列。

## 4. 投影 π：保留指定属性并消除重复

来源：第 11–18 页。

```text
π_{dept}(Course) = {(CS), (Math)}
```

虽然有两门 CS 课程，结果也只有一个 CS，因为结果是集合。投影后的模式只有 dept，cid、title、credits 已不在结果中。

将选择与投影组合：

```text
π_{title}(σ_{dept='CS' ∧ credits>3}(Course))
```

结果模式为 `(title)`，本例是 `{(Databases)}`。从括号最内层向外读：先按条件筛课程，再取标题。

### 不能过早丢失后续需要的属性

```text
正确：π_{title}(σ_{dept='CS'}(Course))
错误：σ_{dept='CS'}(π_{title}(Course))
```

第二式已经投影掉 dept，条件无法求值。一般而言，只有条件 p 用到的全部属性都保留在 X 中时，才可写：

```text
π_X(σ_p(R)) = σ_p(π_X(R))
```

嵌套投影在 `X ⊆ Y` 时满足 `π_X(π_Y(R)) = π_X(R)`。若外层想要内层已删除的属性，表达式没有定义，不是“结果为空”。

## 5. 重命名 ρ：处理角色和同名列

来源：第 55–56、60 页。

重命名可用于给集合运算对齐模式、区分自连接的两个角色，也能避免积和条件连接中的属性冲突。例如要找专业相同的不同学生对：

```text
A ← ρ_{A(aid,aname,amajor)}(Student)
B ← ρ_{B(bid,bname,bmajor)}(Student)
Pairs ← π_{aid,bid}(A ⋈_{amajor=bmajor ∧ aid<bid} B)
```

本例约定学号顺序 `S1<S2<S3<S4`，输出为 `{(S1,S3),(S2,S4)}`。`aid<bid` 同时排除自己和反向重复配对；若只用 `aid≠bid`，会同时返回 `(S1,S3)` 与 `(S3,S1)`。

重命名只改变关系/属性标识，不是把 Amy 改成另一个姓名。不能把未重命名的 Student 与自身直接自然连接，当作所有不同学生配对；那会按所有同名属性相等来匹配。

## 6. 并、交、差：先保证模式相容

来源：第 19–32、56 页。

| 运算 | 保留哪些元组？ | 是否可交换？ |
|---|---|---|
| `R ∪ S` | 在 R 或 S 中，包含两者都有的情况 | 是 |
| `R ∩ S` | 同时在 R 和 S 中 | 是 |
| `R − S` | 在 R 中但不在 S 中 | 通常否 |

三者都要求 **union compatibility 并相容**。课件第 19 页采用同名且同域的一一对应属性要求；因此应先投影出相同属性组，必要时重命名并对齐。列数一样但含义/域不相容，不能直接相减。

用本例建立两个**学号集合**：

```text
CSIDs   ← π_{sid}(Takes ⋈ σ_{dept='CS'}(Course))
MathIDs ← π_{sid}(Takes ⋈ σ_{dept='Math'}(Course))
```

得到 `CSIDs={S1,S2}`，`MathIDs={S2,S3}`；以下简写省去单属性元组的括号。

| 表达式 | 本例结果 | 自然语言 |
|---|---|---|
| `CSIDs ∪ MathIDs` | `{S1,S2,S3}` | 至少选过其中一类 |
| `CSIDs ∩ MathIDs` | `{S2}` | 两类都选过 |
| `CSIDs − MathIDs` | `{S1}` | 选过 CS，但没选过 Math |
| `MathIDs − CSIDs` | `{S3}` | 选过 Math，但没选过 CS |

这里的 or 为包含两者都成立的 inclusive or。“只选其中一类”需另行表达，例如 `(CSIDs−MathIDs) ∪ (MathIDs−CSIDs)`。

### “从未选课”不是一条记录上的不等条件

```text
NeverIDs ← π_{sid}(Student) − π_{sid}(Takes)
```

本例是 `{S4}`。先给出全部候选学生，再减去至少有一条选课记录的学生。不应以某条记录满足 `cid≠C1` 来表示“从未选 C1”：同一学生可能既选 C1，也选 C3。

## 7. 积与连接：从所有配对到正确配对

来源：第 33–47、61 页。

### 笛卡尔积 ×

R 的每一行与 S 的每一行配对。若 R 有 m 行、S 有 n 行，则积有 `m×n` 行；在属性名已消歧的前提下，度为两者度之和。本例 Student×Course 有 `4×3=12` 行、7 个属性。

积不会自动按主外键匹配。如果有同名属性，先用 ρ 消歧；本篇在条件连接中也用 `关系名.属性名` 指明来源，可理解为对冲突属性作了相应限定重命名。

### θ 连接与等值连接

```text
R ⋈_θ S = σ_θ(R × S)
```

该等式在属性名已消歧、条件有定义时成立。θ 可以是比较条件；若连接条件只使用相等比较，就是等值连接 equi-join。

```text
Takes ⋈_{Takes.cid=Course.cid} Course
```

这只配对课程编号相同的行。本例有 5 行。普通等值连接保留两边的连接属性副本（可用限定名区分）；**不会因两列值相等就自动把它们合并为一列**。

### 自然连接 ⋈

自然连接强制**所有同名属性**相等，并只保留这些属性的一份。不存在同名属性时，它退化为笛卡尔积。

```text
Student ⋈ Takes ⋈ Course
```

在本例中，第一步只有 sid 同名，接着只有 cid 同名；结果模式为 `(sid,sname,major,cid,title,dept,credits)`，共 5 行。

自然连接不会理解“哪些列在业务上应该匹配”。若 Instructor 与 Course 都有 dept，自然连接可能额外要求教师院系等于课程院系；若两者不必相同，就应采用明确连接条件或先重命名无关的同名属性。

第 37 页把等值筛选后去掉一份连接列的结果联系到自然连接；严格使用时仍要按第 40–41 页检查所有同名属性，不能把任意“等值连接后投影”一概称为自然连接。连接只保留有匹配的组合，不自动给没有选课的 S4 补一行。

## 8. 组合查询：保留身份，最后输出姓名

来源：第 25–32、43–47 页；以下同名反例为自编。

找“既选过 CS 又选过 Math 的学生姓名”：先求学号交集，再连接 Student：

```text
BothIDs ← CSIDs ∩ MathIDs
Answer  ← π_{sname}(Student ⋈ BothIDs)
```

本例返回 `{(Ben)}`。若先分别取姓名，两边都含 Amy：CS 来自 S1，Math 来自 S3。姓名交集会错误返回 Amy，即把**两个不同的人**合成一个满足两条件的人。

对“选过 CS 但没选过 Math”也应先作学号差。本例正确者 S1 名叫 Amy，但两边姓名集相减会把 Amy 删掉。**投影对并可分配，但一般不能对交和差随意提前投影。**

输出只要姓名时，最后的 π 会合并同名结果，这是题目要求的姓名集合；若需要区分学生，应保留 sid。不要用输出姓名这一要求反推姓名是键。

### Tutorial 的 term 不能随意丢掉

Tutorial 2 的 Enrolled 和 Teaches 都包含 cid、term。“上过某教师教的课程”需要同一课程、同一开课 term 对应；只按 cid 连接，可能把某学生在另一学期的选课错配给该教师。

本篇 Takes 特意省去 term，不能直接代替 Tutorial 的完整输入模式；套用模板前必须先核对关联所需的完整属性组。

## 9. 除法 ÷：表达“每一个目标都满足”

来源：第 48–54、61 页。

设 R 的属性为不相交的 X 与 Y，S 的属性恰为 Y。`R ÷ S` 输出 X，保留那些在 R 中与 **S 的每个元组**都配对的 X 值，候选取自 `π_X(R)`。

```text
R(X,Y) ÷ S(Y) → Result(X)
```

所以除法不是数值相除，也不是“匹配其中任意一个”。需要先确定候选是什么 X、要求覆盖的目标是什么 Y。

### 本例：选过所有 CS 课程的学生

```text
R ← π_{sid,cid}(Takes)
D ← π_{cid}(σ_{dept='CS'}(Course))
AllCSIDs ← R ÷ D
```

D 为 `{C1,C2}`，S1 同时关联二者，S2 只关联 C1，S3 只关联 C3，故结果为 `{S1}`。最后可用 `π_{sname}(Student ⋈ AllCSIDs)` 返回姓名。

- “所有 CS 课程”要求集合应来自完整 Course，不应只从已有选课中提取，否则无人选过的必需课程会被漏掉。
- “所有 CS 课程”允许额外选 Math 课程，不等于“只选 CS 课程”。
- 被除关系只保留 `(sid,cid)`，不夹带 sname、term、grade 等无关属性，否则除法会保留它们并改变“谁需要覆盖所有目标”的含义。

### 多属性目标与结果模式

课件第 53–54 页有 R(A,B,C)、S(B,C)：

```text
R ÷ S          → 输出 A，要求覆盖 S 中全部 (B,C) 配对
R ÷ π_C(S)     → 输出 (A,B)，要求每个固定 (A,B) 覆盖全部 C
```

两者的问题不同。按该页给定实例，第一式得到 `{a1}`；第二式得到 `{(a1,b1),(a3,b2)}`。不要只看到 “all” 就忽略目标关系的模式。

## 10. 除法的差集展开与空目标

来源：第 57 页；候选全集与空目标的讨论是定义边界的解释性补充。

把“每个目标都有”改写成“没有缺失的目标”：

```text
Candidates ← π_X(R)
Required   ← Candidates × S
Missing    ← Required − R
Bad        ← π_X(Missing)
Result     ← Candidates − Bad
```

这里 R 恰为 `(X,Y)`，Required 与 R 的模式需对齐。若原输入含更多属性，先投影到 X、Y。式中的 `X,Y` 是属性组，不是拿两个关系名作集合差。

在本例中，Candidates 为 `{S1,S2,S3}`。Required 有 6 个学号–课程配对；缺失 `(S2,C2)`、`(S3,C1)`、`(S3,C2)`，故 Bad 为 `{S2,S3}`，剩下 S1。R 中的额外 Math 配对不会造成缺失，因此不影响 S1 的资格。

### 目标为空时，必须说清候选范围

按上式，若 S 为空，Required 和 Missing 都为空，标准除法返回 `π_X(R)`。它**不会自动把从未在 R 中出现的学生补进来**。

如果题意是“所有 Student 都作为候选；每人满足每个目标”，应使用明确全集 U：

```text
U      ← π_{sid}(Student)
Bad    ← π_{sid}((U × D) − R)
Result ← U − Bad
```

这里 R、D 与第 9 节相同。D 非空时，此式与标准除法的结果一致（在本例外键有效的前提下）；D 为空时返回全部 U，包含没有选课的 S4。这体现空集上的全称条件为真，不代表任意实际题目都默认允许无目标；若题目排除这种情形，应说明假设。

## 11. γ：分组与聚合

来源：第 58–59 页；Tutorial 2 Question 1(a)(vi)。以下统一记号是本笔记的书写约定。

γ 可以配合 COUNT、SUM、AVG、MIN、MAX。`γ_{分组属性; 聚合函数→结果名}(R)` 表示每组产生一行，保留分组属性并新增聚合值。

```text
Stats ← γ_{dept; COUNT(cid)→nCourses, AVG(credits)→avgCredits}(Course)
```

| dept | nCourses | avgCredits |
|---|---|---|
| CS | 2 | 3.5 |
| Math | 1 | 4 |

再筛选课程数超过 1 的组：`σ_{nCourses>1}(Stats)`，本例只剩 CS。聚合结果名要先在 γ 中定义，外层 σ 才能使用。

### 数的是哪一种对象？

- 本例 Course 一行一门课且 cid 唯一，因此 COUNT(cid) 数课程。
- 若先与 Takes 连接，同一课程可能按不同学生出现多行，直接计数可能数成选课配对，而非不同课程。
- 为数不同对象，应先在正确标识层面去重。例如从连接结果先投影 `(dept,cid,credits)`，再分组；不能仅投影 `(dept,credits)`，因为同院系两门相同学分的课可能被合并。
- `γ_{sid; COUNT(cid)→nTaken}(Takes)` 只产生 S1、S2、S3 的组，计数分别 2、2、1；不会自动产生 S4 的零计数组。

本例每个被聚合组非空且无 NULL。课件第 58 页提出 NULL 问题但未在此完整定义其语义；空输入或 NULL 的处理需明确约定，SQL 中的 COUNT、NULL 等细节在 06 处理。

## 12. 等价改写：先检查前提

来源：第 10、15–17、57、60 页；下表条件为相应定义的解释。

| 改写 | 成立前提或含义 |
|---|---|
| `σ_p(σ_q(R)) = σ_{p∧q}(R)` | 条件均有定义 |
| `π_X(π_Y(R)) = π_X(R)` | `X ⊆ Y` |
| `π_X(σ_p(R)) = σ_p(π_X(R))` | p 用到的属性全部在 X 中 |
| `R ∩ S = R − (R − S)` | R、S 并相容 |
| `R ⋈_θ S = σ_θ(R×S)` | 属性已消歧，θ 有定义 |
| `π_X(R∪S) = π_X(R)∪π_X(S)` | 输入并相容且 X 可用，采用集合语义 |

一般不能把最后一式的 ∪ 直接换成 ∩ 或 −：投影会丢掉身份信息，第 8 节同名学生就是反例。连接中的提前投影也必须保留输出列、连接列、之后筛选所需列。

课件第 57 页给出基本运算 `σ、π、∪、−、×、ρ`，连接、交、除法可由它们导出。第 58 页的聚合则增加统计能力，**不是仅由这些经典基本运算直接获得的一般计数能力**；不要把“可导出的运算”与“加入更强表达能力的聚合”混为一谈。

## 13. 从英文需求写表达式的步骤

来源：第 25–32、43–54、60–61 页；下列为整理后的解题流程。

1. **先写输出模式**：要 sid、姓名、课程标题，还是每院系一行的统计？
2. **确定对象标识与候选范围**：同名对象用键区分；“未参加”需要完整候选全集。
3. **列完整连接条件**：根据题面核对主外键及 term 等上下文；不要只凭同名就自然连接。
4. **翻译量词与逻辑词**：at least one 通常用连接投影；or 用并；both 用交；never 用全集减存在；every 用除法或“减去缺失者”。
5. **保留中间需要的属性**：先过滤/连接/集合判断身份，最后投影输出展示属性。
6. **逐步写中间模式**：每个 σ 的条件列仍在吗？差集两边同模式吗？除法输出是不是所需候选？
7. **用小实例和反例检查**：同名、多个匹配、无匹配、额外课程、缺一门目标、目标为空。

Tutorial 2(a) 的六类题分别落在：选择投影、跨关系连接、并交、差集、除法、γ。这里给的是知识与方法；本篇没有逐题复写 Tutorial 的整套答案，也没有提前生成英文模拟卷。

## 14. 易混点、复习清单与英文表达

| 容易混淆 | 正确区分 |
|---|---|
| σ / π | 选行保留模式 / 选列并去重 |
| 无法求值 / 空结果 | 引用不存在属性属于表达式错误 / 合法表达式可能无匹配 |
| 并相容 / 列数相同 | 属性对应、名称和域按课件要求对齐 / 只有列数不足 |
| or / only one of | 包含同时满足 / 需要排除同时满足 |
| 等值连接 / 自然连接 | 明确相等条件且保留副本 / 所有同名属性相等且合并列 |
| 学生姓名 / 学生标识 | 可同名 / 用键追踪同一个对象 |
| “有条记录不是” / “从未” | 存在一个不满足的记录 / 不存在任何满足的记录 |
| every / only | 覆盖每个目标 / 排除目标之外的对象，两者不同 |
| 除法目标 / 除法候选 | S 的全部元组 / 通常从 `π_X(R)` 取得 |
| COUNT 连接行 / COUNT 不同课程 | 配对次数 / 需要先保留课程标识并去重 |

以下是复习目标，不是正式模拟测试或官方分值：

- [ ] 写出每个运算的输入条件、输出模式与去重行为。
- [ ] 对本例手算选择、投影、学号并交差与自然连接。
- [ ] 正确使用重命名表达同表的两个角色。
- [ ] 用同名学生反例说明为何不能过早投影姓名。
- [ ] 解释 Tutorial 连接为何需要检查 term。
- [ ] 明确除法的 X、Y 和完整目标关系，并手算结果。
- [ ] 将除法展开成缺失配对的差集运算。
- [ ] 区分空目标下的标准除法与显式全集版本。
- [ ] 计算分组统计，识别连接重复和缺失零计数组。
- [ ] 对每条等价改写说明成立前提。

可用于英文简答的表达：

> Selection filters tuples while preserving the relation's attributes.

> Projection retains the specified attributes and eliminates duplicate tuples.

> Union, intersection, and difference require union-compatible relations.

> A natural join matches all common attributes and retains one copy of each common attribute.

> Perform identity-based set operations before projecting names, because different entities may share a name.

> Division returns candidates associated with every tuple in the divisor.

> Universal conditions can be expressed by removing candidates that have a missing required pairing.

> The object counted depends on the input tuples and the identifiers retained before aggregation.

## 来源与整理记录

- 教师主课件：[Relational_Algebra.pptx](../../slides/Relational_Algebra.pptx)，第 1–61 页文字已读；重点查看第 7、10、17、19、37–38、40、42、48、50、53–54、57、60–61 页原图/公式，核对选择投影条件、并相容、连接、除法与基本运算记号。
- 范围依据：[CSC5041_Teaching_Plan.pdf](../../syllabus/CSC5041_Teaching_Plan.pdf)，第 1 页 Week 4、第 2 页 Tutorial 2；参考题面：[Tutorial 2.pdf](../../slides/Tutorial%202.pdf)，第 1 页 Question 1(a)(i)–(vi)，已查看原页及键下划线。教学计划写 Tutorial 2 为 Week 5，题面标题写 Week 6；本篇按实际题型整理，不用这处差异推断考试改期。
- 自编简化模式、姓名反例、空目标与候选全集说明、聚合书写约定及计数边界均已与教师原句区分；本篇不定义 SQL 的 NULL/重复值完整语义。
- 整理者：Codex 主会话。双语结构、表达式模式、示例推演与相对链接已自查；独立 Reviewer 结论以本轮交付消息为准。没有执行数据库查询，例子为静态分析；代码/实验验证 N/A，不创建 submission，教师原件及 01–04 未修改。
- 输入版本 SHA-256：关系代数课件 `dcacfada73c2f482ab3b83ac7c8312cb2176932906b6d3e6cac071d01932283d`；Tutorial 2 `72c016526c1c0ff02c10fcb5f7f964c1184999c684228671025800936a6cabac`；syllabus 教学计划 `31380a7fe6504e46541b6db0bb2f24859c69188bfeb9681dca73354ebeb68295`。
- 下一步：按用户指示整理 06 SQL 查询；全部笔记完成后，再依据两套 Tutorial 编写两套英文练习题。
