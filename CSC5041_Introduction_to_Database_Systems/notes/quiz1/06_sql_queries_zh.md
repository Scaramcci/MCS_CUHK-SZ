# 06 SQL 查询：中文学习笔记

CSC5041 · 第一次课堂测验复习 · 2026-10-19

## 阅读说明与学习目标

本篇接续 [05 关系代数](05_relational_algebra_zh.md)，主要依据教师 [SQLpart1.pptx](../../slides/SQLpart1.pptx) 第 3–58 页，以及 [SQLpart2.pptx](../../slides/SQLpart2.pptx) 第 2–24 页中与查询相关的内容。下文用 P1/P2 区分两份课件，页码按幻灯片顺序计数。

教学计划第 1 页 Week 5 包含 SELECT–FROM–WHERE、排序、聚合、分组与嵌套查询；第 2 页 Tutorial 2 明列 GROUP BY、HAVING、NOT EXISTS、NOT IN with NULLs。因此不能只读文件名为 Part 1 的课件就停止。高级量化比较、DDL/DML、视图及 PL/pgSQL 的边界会另标，不把整份 Part 2 都认定为 Test 1 必考内容。

学完后，应能选择正确的结果粒度，写完整连接条件，处理重复值、NULL、分组、存在性和反存在性。所有例子使用自编数据，**查询结果是静态推演，未在 PostgreSQL 或其他数据库中执行**。补充官方文档用于核对语义，不决定教师考试深度。

## 1. 六个常用子句：书写顺序与逻辑顺序

来源：P1 第 13、26–27、44–45 页；P2 第 18、22–24 页。

```text
SELECT 输出列或表达式
FROM 输入表及连接
WHERE 行条件
GROUP BY 分组属性
HAVING 组条件
ORDER BY 排序属性;
```

WHERE、GROUP BY、HAVING、ORDER BY 按需要使用。P2 第 24 页展示的是本课查询框架，不是现代 SQL 所有语法的完整上限。

理解常规查询时可按以下**逻辑阶段**阅读：

```text
FROM / JOIN → WHERE → GROUP BY / 聚合 → HAVING
            → SELECT → DISTINCT（若指定）→ ORDER BY
```

这不是优化器必须采用的物理执行顺序。WHERE 在组形成前筛行，不能在同一查询层直接用 `AVG(score)` 当行条件；输出别名也不要直接拿到同层 WHERE 中使用。ORDER BY 则可使用输出别名。

SQL 查询通常是声明式的：说明要什么结果。SELECT 中写一个计算表达式，只改变输出，不等于 UPDATE 修改原始数据。

## 2. 贯穿例子：在 05 的基础上加入学期与缺失成绩

以下为自编输入；**不是 Tutorial 原模式**，也不沿用 05 的 Takes 作为完整选课表。

```text
Student(sid, sname, major)                 PK{sid}
Course(cid, title, dept, credits)          PK{cid}
Enrolment(sid, cid, term, score)           PK{sid,cid,term}
Enrolment.sid → Student.sid; Enrolment.cid → Course.cid
```

除 score 外各列均必填；score 是可空数值，NULL 表示成绩尚未获得，不是 0。term 是字符串。

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

Enrolment：

| sid | cid | term | score |
|---|---|---|---|
| S1 | C1 | 2026F | 90 |
| S1 | C2 | 2026F | 80 |
| S1 | C1 | 2027S | NULL |
| S2 | C1 | 2026F | NULL |
| S2 | C3 | 2026F | 80 |
| S3 | C3 | 2026F | NULL |

共有 6 次选课、3 个非空成绩、2 种不同非空成绩（80、90）。S1 重修 C1；S1 与 S3 同名；S4 无选课。后续除明确的假设变更外，都独立使用这份输入。

## 3. 基本查询、别名、字符串与 DISTINCT

来源：P1 第 12–13、18–25、28–40 页。

```sql
SELECT c.cid, c.title, c.credits * 2 AS doubled_credits
FROM Course AS c
WHERE c.dept = 'CS' AND c.credits > 3;
```

结果为 `(C1,Databases,8)`，Course 中的 credits 仍是 4。字符串用半角单引号；字符串内的单引号加倍，例如 `'O''Brien'`。不要把中文弯引号从 PPT 直接复制到代码中。

| 写法 | 含义 |
|---|---|
| `=`、`<>`、`<`、`<=`、`>`、`>=` | 比较运算；本篇用 `<>` 表示不等 |
| `IN ('CS','Math')` | 属于给定值列表 |
| `LIKE 'A%'` | 以 A 开头，`%` 可匹配零个或多个字符 |
| `LIKE '_e%'` | 第二个字符是 e，`_` 匹配一个字符 |
| `BETWEEN 3 AND 4` | 含边界的范围比较 |

BETWEEN 是补充写法。混用 AND、OR 时主动加括号，例如 `(major='CS' OR major='Math') AND sid<>'S4'`，避免把组合条件读错。

### SQL 默认保留输出重复

```sql
SELECT s.sname FROM Student AS s;
SELECT DISTINCT s.sname FROM Student AS s;
```

第一式输出 Amy 两次、Ben 一次、Dana 一次；第二式只有三种姓名。没有 ORDER BY 时不要假定这些行按某个顺序返回。`DISTINCT sid,sname` 对**整个输出属性组**去重，不是单独对每列去重。

只要输出姓名，不表示姓名是键；连接与集合判断仍应优先保留 sid。

## 4. NULL 与三值逻辑

来源：P1 第 18、35–36 页；补充核对 [PostgreSQL 比较运算文档](https://www.postgresql.org/docs/18/functions-comparison.html)。

普通比较遇到 NULL 通常得到 **UNKNOWN**。WHERE 只保留条件为 TRUE 的行；FALSE 与 UNKNOWN 都不保留，但二者不是同一个逻辑值。

| 表达式 | 结果 |
|---|---|
| `NULL = NULL`、`NULL <> NULL`、`NULL > 80` | UNKNOWN |
| `NOT UNKNOWN` | UNKNOWN |
| `TRUE AND UNKNOWN` | UNKNOWN |
| `FALSE AND UNKNOWN` | FALSE |
| `TRUE OR UNKNOWN` | TRUE |
| `FALSE OR UNKNOWN` | UNKNOWN |

**课件措辞辨析**：P1 第 18 页的 “Comparison against NULL yields FALSE” 不应按字面记成逻辑定律。第 35 页明确给出 UNKNOWN；“被 WHERE 过滤掉”不等于“表达式本身为 FALSE”。

```sql
SELECT sid, cid, term
FROM Enrolment
WHERE score IS NULL;
```

得到 `(S1,C1,2027S)`、`(S2,C1,2026F)`、`(S3,C3,2026F)`，结果无保证顺序。不能用 `score = NULL` 替代；也不能用 `score <> 90` 找出未出分记录，因为这些记录的比较结果是 UNKNOWN。

若要“不是 90 分，或者未出分”，明确写 `score <> 90 OR score IS NULL`。数值 0 是一个已知成绩，不应无需求依据地把 NULL 改成 0。

## 5. 多表连接：先确定完整配对条件

来源：P1 第 41–49、52–58 页。

```sql
SELECT s.sid, s.sname, c.title, e.term
FROM Student AS s
JOIN Enrolment AS e ON e.sid = s.sid
JOIN Course AS c ON c.cid = e.cid
WHERE c.dept = 'CS';
```

本例得到 4 行：S1 的 C1 两个学期、C2 一次，以及 S2 的 C1 一次。若只输出姓名，会有三行 Amy、一行 Ben；题目要求不同学生时，可输出 `DISTINCT s.sid,s.sname`，而不是掩盖错误连接。

遗漏连接条件可能产生笛卡尔积；两张有 name 的表写 `name=name` 还可能因歧义报错。用表别名限定列名，也让每条联系更容易检查。

### NATURAL JOIN 的风险

它匹配**所有同名列**并合并它们。P1 第 55–57 页说明教师院系与课程院系未必相同，不能无意增加相等条件。优先用清楚的 JOIN…ON 表达已确认的业务联系。

Tutorial 2 的 Enrolled 与 Teaches 都有 cid、term，教师与选课的关联要同时匹配二者：`e.cid=t.cid AND e.term=t.term`。只按 cid 会把不同学期混在一起。本篇没有 Teaching 表，因此不把该条件当作可直接对本例运行的完整查询。

对 INNER JOIN，某些条件可在 ON 与 WHERE 间等价调整；不要把它理解为固定的物理执行先后，也不要推广为所有外连接都等价，外连接会涉及补 NULL 的行。

## 6. 自连接与排序

来源：P1 第 50–51 页；P2 第 23 页。

找专业相同的不同学生配对：

```sql
SELECT a.sid AS sid1, b.sid AS sid2
FROM Student AS a
JOIN Student AS b ON a.major = b.major
WHERE a.sid < b.sid
ORDER BY sid1, sid2;
```

按本例学号的通常字符顺序，结果为 `(S1,S3)`、`(S2,S4)`。`<` 排除自己和反向重复；只有 `<>` 会保留正反两种顺序。

```sql
SELECT cid, title, credits
FROM Course
ORDER BY credits DESC, cid ASC;
```

结果顺序为 C1、C3、C2。只按 credits 排序时，C1 与 C3 同为 4，二者先后未确定；若题目要求稳定先后，要增加明确的次级排序键。排序不等于去重，也不改变数据在逻辑关系中的身份。

## 7. 聚合：COUNT、SUM、AVG 与 NULL

来源：P2 第 12–16 页；补充核对 [PostgreSQL 聚合文档](https://www.postgresql.org/docs/18/functions-aggregate.html)。

```sql
SELECT COUNT(*) AS n_rows,
       COUNT(score) AS n_scored,
       COUNT(DISTINCT score) AS n_distinct_scores,
       SUM(score) AS total_score,
       AVG(score) AS mean_score
FROM Enrolment;
```

本例为 `(6,3,2,250,250/3)`，平均值约 83.33，显示精度取决于数值类型。

| 写法 | 数什么或如何处理 NULL？ |
|---|---|
| `COUNT(*)` | 输入行数，包括 score 缺失的行 |
| `COUNT(score)` | score 非空的行数，保留重复值的次数 |
| `COUNT(DISTINCT score)` | 不同非空 score 值的个数 |
| `SUM/AVG/MIN/MAX(score)` | 基于非空输入值计算 |

AVG 的分母是本例 3 个非空成绩，不是 6 次选课。`AVG(DISTINCT score)` 则为 `(80+90)/2=85`，已经改变统计问题，不是一般的去重修复。

### 空输入与全 NULL

无 GROUP BY 的汇总在没有匹配行时仍产生一行：COUNT 为 0，SUM、AVG、MIN、MAX 为 NULL。若匹配行存在但 score 全为 NULL，COUNT(*) 仍数这些行，COUNT(score)=0，其他四种 score 聚合仍为 NULL。

例如筛选 `sid='S3'` 后，COUNT(*)=1、COUNT(score)=0、AVG(score)=NULL。NULL 不是自动补零；是否把缺失汇总显示成 0，需要业务含义支持。

## 8. GROUP BY 与 HAVING：每组一行

来源：P2 第 17–22 页。

```sql
SELECT e.sid, COUNT(*) AS n_enrolments,
       COUNT(e.score) AS n_scored, AVG(e.score) AS mean_score
FROM Enrolment AS e
GROUP BY e.sid
HAVING COUNT(*) >= 2
ORDER BY e.sid;
```

| sid | n_enrolments | n_scored | mean_score |
|---|---|---|---|
| S1 | 3 | 2 | 85 |
| S2 | 2 | 1 | 80 |

WHERE 筛选输入行，HAVING 筛选已经形成的组。若先加 `WHERE score IS NOT NULL`，再 COUNT(*)，数的就是有成绩的记录，S2 不再满足至少两行，不能声称与原查询相同。

按本课可直接采用的书写规则：SELECT 中非聚合的列都明确列入 GROUP BY；不要查询 `sid,cid,AVG(score)` 却只按 sid 分组，从一个学生的多门课中任意挑 cid。某些实现存在基于函数依赖的例外，不影响先按这条规则写清楚的做法。

### 统计对象与零记录

本例 S1 有 3 次选课，却只有 2 门不同课程；数课程可用 `COUNT(DISTINCT cid)`。连接 Enrolment 后统计课程数量时，同一课程也可能被多名学生重复计入。必须先回答“数选课记录，还是数不同课程”。

本查询不会为无选课的 S4 生成零计数组。若需要所有学生含零计数，须另设计覆盖全部学生的查询，通常涉及外连接；不能用当前内连接/分组结果冒充已经包含 S4。

## 9. 子查询：先区分标量与多行结果

来源：P2 第 2–5 页；基数边界补充见 [PostgreSQL 子查询文档](https://www.postgresql.org/docs/18/functions-subquery.html)。

### 标量子查询

```sql
SELECT cid, title
FROM Course
WHERE credits > (SELECT AVG(credits) FROM Course);
```

总体平均学分是 11/3，结果包含 C1、C3。这里的内层聚合保证一列一行，适合当一个值使用。

标量位置要求一列且至多一行：零行相当于 NULL，多于一行在 PostgreSQL/标准标量语义下是错误，不是自动取第一行。例如把内层替换成 `SELECT credits FROM Course WHERE dept='CS'` 会返回两行，不能直接当标量比较。这个 AVG 子查询不需要引用外层别名。

### IN：测试一个值是否在结果中

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE s.sid IN (
    SELECT e.sid
    FROM Enrolment AS e
    WHERE e.score >= 85
);
```

本例只有 S1。单值 IN 的子查询应返回一列；右侧重复值不会让同一外层行重复输出。IN 的逻辑与 NULL 的关系在第 11 节说明。

## 10. EXISTS、NOT EXISTS 与相关子查询

来源：P2 第 6 页；Tutorial 2 主题列有 NOT EXISTS。

相关子查询引用外层当前行，例如内层的 `e.sid=s.sid`。可按“对每个外层学生问一个存在性问题”理解，不代表数据库一定逐行执行完整子查询。

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE EXISTS (
    SELECT 1
    FROM Enrolment AS e
    WHERE e.sid = s.sid AND e.score IS NULL
);
```

本例返回 S1、S2、S3。EXISTS 关心子查询是否有行，不关心 SELECT 列表中的 1；这个普通存在性查询即使有多个匹配，也只为每个外层学生返回一次。外层自己若已有重复行，EXISTS 不会额外替它去重。

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM Enrolment AS e
    WHERE e.sid = s.sid
);
```

本例只有 S4。“从未”要检查**没有任何匹配行**，不是找一行 `cid <> 'C1'`。若忘记相关条件，内层只要全表存在任意记录，就会影响所有外层学生。

## 11. NOT IN 遇到 NULL：反例要会解释

来源：教学计划第 2 页 Tutorial 2；补充依据 [PostgreSQL IN/NOT IN 说明](https://www.postgresql.org/docs/18/functions-subquery.html#FUNCTIONS-SUBQUERY-NOTIN)。

对非空数值，`80 NOT IN (90,NULL)` 等价于 `80<>90 AND 80<>NULL`，结果为 UNKNOWN，WHERE 不保留它；`90 NOT IN (90,NULL)` 则因已找到相等值而为 FALSE。**不是任何含 NULL 的 NOT IN 都产生同一个结果。**

| 情况 | 单值比较的结果 |
|---|---|
| 右侧存在相等值 | IN 为 TRUE，NOT IN 为 FALSE |
| 没有相等值，但比较涉及 NULL，且右侧非空 | 可能为 UNKNOWN，不能当作确定“不在” |
| 右侧为空集 | IN 为 FALSE，NOT IN 为 TRUE |

对本例这个“找无选课学生”的特定问题，下面写法安全：

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE s.sid NOT IN (SELECT e.sid FROM Enrolment AS e);
```

原因是两边 sid 都保证非空；本例仍返回 S4。若换成可空列，这个推理就不成立。删除右侧 NULL 也不能自动解决左侧 NULL 的含义；使用相关 NOT EXISTS 时，同样要明确 NULL 键应如何匹配，不能声称它与 NOT IN 在任意空值条件下都等价。

## 12. UNION、INTERSECT、EXCEPT 与身份粒度

来源：P2 第 9 页；与 05 的集合运算对应。

```sql
SELECT e.sid
FROM Enrolment AS e
JOIN Course AS c ON c.cid = e.cid
WHERE c.dept = 'CS'
INTERSECT
SELECT e.sid
FROM Enrolment AS e
JOIN Course AS c ON c.cid = e.cid
WHERE c.dept = 'Math';
```

结果为 S2。两侧课程条件不要求同一条选课记录同时属于两个院系；它们先分别求学生集合，再按身份求交。

| 运算 | 默认行为 |
|---|---|
| UNION | 合并并去除输出重复 |
| UNION ALL | 合并并保留重复次数 |
| INTERSECT | 共有元组，去重 |
| EXCEPT | 左边有、右边没有的元组，去重，方向重要 |

输入列数必须一致，对应位置类型要相容；SQL 集合运算按列位置对应，不要求像本课命名关系代数那样两边列名完全相同。INTERSECT ALL、EXCEPT ALL 另有多重集次数语义，基础复习先与默认去重版本区别，不把 ALL 理解成无作用的装饰。

若先在两边选 sname 再求交，会让 S1 的 CS 记录与 S3 的 Math 记录因同名 Amy 被错误合并；应先求 sid，再连接或用 IN/EXISTS 取得姓名。

## 13. “每个目标都满足”：没有缺失目标

来源：P2 第 10–11 页；下例为将 05 方法写成 SQL 的自编解释，不是 Tutorial 逐题答案。

找选过每门 CS 课程的学生，可以从 Student 候选出发，排除存在某门 CS 课却找不到该学生选课记录的情况：

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM Course AS c
    WHERE c.dept = 'CS'
      AND NOT EXISTS (
          SELECT 1
          FROM Enrolment AS e
          WHERE e.sid = s.sid AND e.cid = c.cid
      )
);
```

本例只有 S1。内层寻找某个学生–课程配对；中层寻找缺失配对的目标课程；外层要求这样的目标不存在。跨学期选过即可，是本例明确采用的含义；若要求某个 term，须在目标与选课条件中明确对应的范围。

这要求覆盖所有目标，允许额外选非 CS 课程；重复选同一门课也不能代替缺失的另一门课。目标来自完整 Course，不能仅从已有人选过的课程产生。

若假设数据库中没有 CS 课程，此式返回所有 Student，包括 S4，因为不存在可缺失的目标。若题意要求至少有一个目标，要另加目标非空要求。课件 P2 第 11 页从 Sells 中枚举候选，空目标时只返回在 Sells 中出现过的 bar；这与本例从完整 Student 枚举候选的范围不同，应联系 05 的空除数讨论。

## 14. 课件其余内容与本轮范围

### ANY / ALL【补充辨识】

来源：P2 第 7–8 页。教学计划 Week 6 列高级子查询及集合比较，本节只帮助识别记号，不据此新增 Test 1 深度要求。

`x > ANY (subquery)` 问是否至少一个比较为真；`x > ALL (subquery)` 问是否所有比较都为真。空右侧时 ANY 为 FALSE、ALL 为 TRUE。含 NULL 时还可能 UNKNOWN；不能无条件将 ALL 改写成与 MAX 比较，因为空集或 NULL 可使语义不同。

### DDL、数据修改、视图与 PL/pgSQL

P2 第 25–52 页还讲 CREATE TABLE、主外键、INSERT、DELETE、UPDATE、视图和结构修改。这些可联系 03–04 理解，但本章不据文件位置将它们全部算作 Test 1 查询重点：

- PRIMARY KEY 结合唯一性与非空；FOREIGN KEY 并不自动要求该列非空，1:1 也不能仅靠一个普通外键保证。
- DELETE 删除记录，DROP TABLE 删除表结构；UPDATE 没有 WHERE 会作用于全表。这里只解释命令，不执行任何修改。
- 普通视图是查询定义的接口，不应将课件“does not take up space”绝对理解为连定义元数据都不占空间，也不等于物化视图保存结果。
- PL/pgSQL、索引、事务、规范化等超出本篇，不展开。

## 15. 写查询的检查顺序与复习清单

1. **确定输出粒度**：每个学生、每次选课、不同课程，还是每组一行？
2. **先核对模式和完整连接键**：尤其 sid、cid、term；区分学生专业与课程院系。
3. **写行条件并处理 NULL**：WHERE 只留 TRUE；选择 IS NULL、IN、EXISTS 等合适形式。
4. **明确重复值要求**：需要 DISTINCT 吗？DISTINCT 是在掩盖错误连接，还是符合输出粒度？
5. **分组后再筛组**：SELECT 中的普通列明确分组；COUNT(*)、COUNT(col)、COUNT(DISTINCT col) 不混用。
6. **检查子查询形状与相关条件**：标量是否至多一行？存在性是否真的关联当前外层对象？
7. **检查边界**：同名、重修、未出分、无匹配、重复匹配、空目标；需要顺序时加 ORDER BY。

| 易混点 | 正确区分 |
|---|---|
| UNKNOWN / FALSE | 逻辑不同；WHERE 都不保留 |
| DISTINCT / GROUP BY | 输出元组去重 / 形成统计组，不可机械互换 |
| WHERE / HAVING | 组形成前筛行 / 聚合后筛组 |
| COUNT(*) / COUNT(score) | 所有输入行 / 非空 score 行 |
| EXISTS / 标量子查询 | 是否有行 / 把结果作为一个值 |
| NOT IN / NOT EXISTS | 比较值集合 / 检查相关匹配；NULL 下不无条件等价 |
| “所有” / “只有” | 覆盖每个目标 / 排除目标之外的联系 |
| SQL 集合运算 / 普通 SELECT | 默认去重 / 默认保留重复 |

以下是复习目标，不是正式模拟卷或官方分值：

- [ ] 不看笔记写出常用子句的书写顺序与逻辑阶段。
- [ ] 手算基本查询、DISTINCT、自连接及带次级键的排序。
- [ ] 用三值逻辑解释为什么未出分记录不满足 `score<>90`。
- [ ] 检查普通连接和跨学期连接的完整条件。
- [ ] 手算三种 COUNT、全 NULL 与空输入汇总。
- [ ] 解释 WHERE 与 HAVING 改变统计结果的方式。
- [ ] 区分标量、IN、EXISTS 子查询的结果要求。
- [ ] 解释 NOT IN 含 NULL 的反例与非空 sid 的安全情形。
- [ ] 用学生身份作集合运算，并解释不能过早投影姓名。
- [ ] 读懂双重 NOT EXISTS 的三层含义及空目标行为。

可用于英文简答的表达：

> WHERE retains only rows for which its condition evaluates to TRUE.

> COUNT(*) counts rows, whereas COUNT(column) counts non-NULL values in that column.

> WHERE filters input rows; HAVING filters groups after aggregation.

> EXISTS tests whether a subquery returns any rows, not the values in its SELECT list.

> A NOT IN comparison can evaluate to UNKNOWN when NULL participates and no equal value is found.

> A universal requirement can be expressed as the absence of a required target without a matching association.

## 来源与整理记录

- 教师课件：[SQLpart1.pptx](../../slides/SQLpart1.pptx)、[SQLpart2.pptx](../../slides/SQLpart2.pptx)。本篇核心来源为 P1 第 3–58 页、P2 第 2–24 页；已读取文字并重点查看 P1 第 18、31、35–36、51、55、58 页，P2 第 2、6、9、11、15–16、20、22、24 页原图。P2 第 25–52 页仅作范围辨识。
- 教学范围：[CSC5041_Teaching_Plan.pdf](../../syllabus/CSC5041_Teaching_Plan.pdf)，第 1 页 Weeks 5–6、第 2 页 Tutorial 2；参考题面：[Tutorial 2.pdf](../../slides/Tutorial%202.pdf)，第 1 页。题面 Week 6 与计划 Week 5 标签差异已在 05 记录，本篇不推断改期。
- 补充核对：PostgreSQL 18 官方文档的 [比较](https://www.postgresql.org/docs/18/functions-comparison.html)、[子查询](https://www.postgresql.org/docs/18/functions-subquery.html)、[聚合](https://www.postgresql.org/docs/18/functions-aggregate.html)、[表表达式](https://www.postgresql.org/docs/18/queries-table-expressions.html)，于本轮在线读取；用于 NULL、子查询基数及聚合等边界，不代表教师规定了 PostgreSQL 18 版本。
- 整理者：Codex 主会话。双语结构、查询语义、例子推演与链接已自查；独立 Reviewer 结论以本轮交付消息为准。**没有执行 SQL，未声称 PostgreSQL 运行验证通过**；代码/实验运行 N/A，不创建 submission，教师原件与 01–05 未修改。
- 输入 SHA-256：SQLpart1 `aa28c989fb3674e780418c78c483bba20ff5a50b7da067b0341e60410a68c8ed`；SQLpart2 `acd25cbd4bbd246f8901ada4c437c3f2d00873385961475cd4c941e9089bf45c`；Tutorial 2 `72c016526c1c0ff02c10fcb5f7f964c1184999c684228671025800936a6cabac`；syllabus 教学计划 `31380a7fe6504e46541b6db0bb2f24859c69188bfeb9681dca73354ebeb68295`。
- 本篇完成后，01–06 的计划主题已有笔记；下一阶段按用户指示依据两套 Tutorial 编写两套英文练习题。本轮未生成题卷。
