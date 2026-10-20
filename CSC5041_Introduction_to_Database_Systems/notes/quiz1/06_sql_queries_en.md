# 06 SQL Queries: English Study Notes

CSC5041 · In-class Test 1 revision · 19 October 2026

## Scope and learning goals

This chapter follows [05 Relational Algebra](05_relational_algebra_en.md). Its main sources are the lecturer's [SQLpart1.pptx](../../slides/SQLpart1.pptx), slides 3–58, and the query material on slides 2–24 of [SQLpart2.pptx](../../slides/SQLpart2.pptx). P1 and P2 below distinguish the decks; numbers refer to slide order.

Week 5 on page 1 of the teaching plan includes SELECT–FROM–WHERE, sorting, aggregation, grouping, and nested queries. Tutorial 2 on page 2 explicitly lists GROUP BY, HAVING, NOT EXISTS, and NOT IN with NULLs. Stopping at the file named Part 1 would therefore omit listed topics. Advanced quantified comparisons, DDL/DML, views, and PL/pgSQL are distinguished rather than treating all Part 2 material as compulsory for Test 1.

After studying this chapter, you should be able to choose a result granularity, specify complete joins, and handle duplicates, NULL, grouping, existence, and nonexistence. All data is original. **Query results are static deductions; no queries were executed in PostgreSQL or another database.** Supplementary official documentation checks semantics, not the lecturer's examination depth.

## 1. Six common clauses: written and logical order

Source: P1 slides 13, 26–27, and 44–45; P2 slides 18 and 22–24.

```text
SELECT output columns or expressions
FROM input tables and joins
WHERE row conditions
GROUP BY grouping attributes
HAVING group conditions
ORDER BY ordering attributes;
```

Use WHERE, GROUP BY, HAVING, and ORDER BY as needed. P2 slide 24 presents the course framework, not an exhaustive upper limit on modern SQL syntax.

For ordinary queries, use these **logical stages**:

```text
FROM / JOIN → WHERE → GROUP BY / aggregation → HAVING
            → SELECT → DISTINCT (if specified) → ORDER BY
```

This is not a mandatory physical execution order. WHERE filters before groups form, so `AVG(score)` cannot directly be a same-level row condition. Do not use an output alias in the same-level WHERE; ORDER BY can use output aliases.

SQL querying is generally declarative: specify the desired result. A computed SELECT expression changes the output, not the stored values as UPDATE would.

## 2. Running example: add terms and missing scores to Chapter 05

These are original inputs, **not the tutorial schema**, and the simplified Takes relation from Chapter 05 is not reused as a full enrolment table.

```text
Student(sid, sname, major)                 PK{sid}
Course(cid, title, dept, credits)          PK{cid}
Enrolment(sid, cid, term, score)           PK{sid,cid,term}
Enrolment.sid → Student.sid; Enrolment.cid → Course.cid
```

All columns except score are mandatory. score is nullable numeric data; NULL means a score is not yet available, not zero. term is a string.

Student:

| sid | sname | major |
|---|---|---|
| S1 | Amy | CS |
| S2 | Ben | Math |
| S3 | Amy | CS |
| S4 | Dana | Math |

Course:

| cid | title | dept | credits |
|---|---|---|---|
| C1 | Databases | CS | 4 |
| C2 | AI | CS | 3 |
| C3 | Linear Algebra | Math | 4 |

Enrolment:

| sid | cid | term | score |
|---|---|---|---|
| S1 | C1 | 2026F | 90 |
| S1 | C2 | 2026F | 80 |
| S1 | C1 | 2027S | NULL |
| S2 | C1 | 2026F | NULL |
| S2 | C3 | 2026F | 80 |
| S3 | C3 | 2026F | NULL |

There are six enrolments, three non-NULL scores, and two distinct non-NULL scores: 80 and 90. S1 repeats C1, S1 and S3 share a name, and S4 has no enrolments. Unless an explicit hypothetical change is stated, each example independently uses these inputs.

## 3. Basic queries, aliases, strings, and DISTINCT

Source: P1 slides 12–13, 18–25, and 28–40.

```sql
SELECT c.cid, c.title, c.credits * 2 AS doubled_credits
FROM Course AS c
WHERE c.dept = 'CS' AND c.credits > 3;
```

The result is `(C1,Databases,8)`; the stored credits value remains 4. Use straight single quotes for strings and double an embedded quote, as in `'O''Brien'`. Do not paste typographic quotation marks from slides into executable SQL.

| Expression | Meaning |
|---|---|
| `=`, `<>`, `<`, `<=`, `>`, `>=` | Comparisons; these notes use `<>` for inequality |
| `IN ('CS','Math')` | Membership in a value list |
| `LIKE 'A%'` | Starts with A; `%` matches zero or more characters |
| `LIKE '_e%'` | Has e as its second character; `_` matches one character |
| `BETWEEN 3 AND 4` | Inclusive range comparison |

BETWEEN is supplementary syntax. Parenthesize combined AND/OR conditions explicitly, for example `(major='CS' OR major='Math') AND sid<>'S4'`.

### SQL retains output duplicates by default

```sql
SELECT s.sname FROM Student AS s;
SELECT DISTINCT s.sname FROM Student AS s;
```

The first outputs Amy twice, Ben once, and Dana once. The second returns three distinct names. No row order is guaranteed without ORDER BY. `DISTINCT sid,sname` deduplicates the **complete output tuple**, not each column independently.

Requesting names does not make names identifiers. Prefer sid for joins and identity-based set decisions.

## 4. NULL and three-valued logic

Source: P1 slides 18 and 35–36; additional check: [PostgreSQL comparison documentation](https://www.postgresql.org/docs/18/functions-comparison.html).

Ordinary comparisons with NULL generally produce **UNKNOWN**. WHERE retains only TRUE rows. FALSE and UNKNOWN are both rejected, but they are different logical results.

| Expression | Result |
|---|---|
| `NULL = NULL`, `NULL <> NULL`, `NULL > 80` | UNKNOWN |
| `NOT UNKNOWN` | UNKNOWN |
| `TRUE AND UNKNOWN` | UNKNOWN |
| `FALSE AND UNKNOWN` | FALSE |
| `TRUE OR UNKNOWN` | TRUE |
| `FALSE OR UNKNOWN` | UNKNOWN |

**Slide clarification:** do not memorize “Comparison against NULL yields FALSE” on P1 slide 18 as a logical law. Slide 35 explicitly gives UNKNOWN. Rejection by WHERE does not make the expression itself FALSE.

```sql
SELECT sid, cid, term
FROM Enrolment
WHERE score IS NULL;
```

The result contains `(S1,C1,2027S)`, `(S2,C1,2026F)`, and `(S3,C3,2026F)`, without a guaranteed order. `score = NULL` is not a replacement. Nor does `score <> 90` retrieve missing scores: those comparisons are UNKNOWN.

To include scores other than 90 together with missing scores, write `score <> 90 OR score IS NULL`. Zero is a known numeric score; replacing missing values with zero requires a substantive justification.

## 5. Multiple-table joins: identify the full association

Source: P1 slides 41–49 and 52–58.

```sql
SELECT s.sid, s.sname, c.title, e.term
FROM Student AS s
JOIN Enrolment AS e ON e.sid = s.sid
JOIN Course AS c ON c.cid = e.cid
WHERE c.dept = 'CS';
```

There are four rows: S1's two C1 terms and one C2 term, plus S2's C1 term. Selecting only names would produce Amy three times and Ben once. If distinct students are required, use `DISTINCT s.sid,s.sname` rather than masking an incorrect join.

Missing join conditions can create a Cartesian product. With two name columns, `name=name` can also be ambiguous. Qualify columns with aliases to make every association explicit.

### NATURAL JOIN risks

It matches **all common column names** and merges those columns. P1 slides 55–57 explain that instructor and course departments need not agree. Prefer clear JOIN…ON conditions for the business association actually required.

Tutorial 2's Enrolled and Teaches contain both cid and term. Relating teaching assignments to enrolments requires `e.cid=t.cid AND e.term=t.term`. Joining only cid mixes offerings from different terms. This chapter has no Teaching table, so that condition is not presented as a complete runnable query on these inputs.

Some INNER JOIN conditions can move between ON and WHERE without changing the result. This does not dictate physical execution order and does not generalize to all outer joins, which introduce NULL-extended rows.

## 6. Self-joins and ordering

Source: P1 slides 50–51 and P2 slide 23.

Pairs of different students sharing a major:

```sql
SELECT a.sid AS sid1, b.sid AS sid2
FROM Student AS a
JOIN Student AS b ON a.major = b.major
WHERE a.sid < b.sid
ORDER BY sid1, sid2;
```

Under the example's ordinary character ordering of IDs, the result is `(S1,S3)`, then `(S2,S4)`. `<` excludes self-pairs and reverse duplicates; `<>` alone retains both directions.

```sql
SELECT cid, title, credits
FROM Course
ORDER BY credits DESC, cid ASC;
```

The course order is C1, C3, C2. Ordering only by credits leaves the tie between C1 and C3 unresolved. Add an explicit secondary key when a definite order is required. Ordering does not eliminate duplicates or change tuple identity.

## 7. Aggregates: COUNT, SUM, AVG, and NULL

Source: P2 slides 12–16; additional check: [PostgreSQL aggregate documentation](https://www.postgresql.org/docs/18/functions-aggregate.html).

```sql
SELECT COUNT(*) AS n_rows,
       COUNT(score) AS n_scored,
       COUNT(DISTINCT score) AS n_distinct_scores,
       SUM(score) AS total_score,
       AVG(score) AS mean_score
FROM Enrolment;
```

The result is `(6,3,2,250,250/3)`, with a mean of approximately 83.33; displayed precision depends on the numeric type.

| Expression | What is counted or how NULL is handled |
|---|---|
| `COUNT(*)` | All input rows, including rows with missing score |
| `COUNT(score)` | Non-NULL score occurrences, including repeated values |
| `COUNT(DISTINCT score)` | Distinct non-NULL score values |
| `SUM/AVG/MIN/MAX(score)` | Calculated from non-NULL input values |

AVG divides by three non-NULL scores, not six enrolments. `AVG(DISTINCT score)` instead gives `(80+90)/2=85`, changing the statistical question rather than providing a general duplicate repair.

### Empty input and all-NULL input

Without GROUP BY, an aggregate query still returns one row for no matching input: COUNT is zero, while SUM, AVG, MIN, and MAX are NULL. If matching rows exist but every score is NULL, COUNT(*) counts those rows, COUNT(score)=0, and the other four score aggregates remain NULL.

Filtering to `sid='S3'`, for example, gives COUNT(*)=1, COUNT(score)=0, and AVG(score)=NULL. Missing summaries are not automatically zero; choosing a zero display requires appropriate business meaning.

## 8. GROUP BY and HAVING: one row per group

Source: P2 slides 17–22.

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

WHERE filters input rows; HAVING filters formed groups. Adding `WHERE score IS NOT NULL` changes COUNT(*) to a count of scored enrolments. S2 then fails the two-row requirement, so this is not equivalent to the original query.

Use the course's explicit writing rule: include nonaggregated SELECT columns in GROUP BY. Do not select `sid,cid,AVG(score)` while grouping only by sid and arbitrarily choose a course for each student. Some implementations recognize functional-dependency exceptions; writing the grouping explicitly avoids relying on them here.

### Counted objects and zero enrolments

S1 has three enrolments but only two different courses; use `COUNT(DISTINCT cid)` for course count. Joining Enrolment can also repeat a course across students. Decide whether the query counts enrolment records or distinct courses first.

The query does not generate a zero-count group for S4. Covering all students, including zero enrolments, needs another query design, usually involving an outer join. Do not claim that the current inner-join/grouping result includes S4.

## 9. Subqueries: scalar versus multiple rows

Source: P2 slides 2–5; cardinality boundaries additionally checked against [PostgreSQL subquery documentation](https://www.postgresql.org/docs/18/functions-subquery.html).

### Scalar subquery

```sql
SELECT cid, title
FROM Course
WHERE credits > (SELECT AVG(credits) FROM Course);
```

The mean credits value is 11/3, so C1 and C3 qualify. The inner aggregate returns one column and one row, making it suitable as one value.

A scalar position requires one column and at most one row. Zero rows mean NULL; multiple rows are an error under PostgreSQL/standard scalar semantics, not an instruction to take the first row. Replacing the inner query with `SELECT credits FROM Course WHERE dept='CS'` returns two rows and is invalid as a scalar. The inner AVG does not need an outer alias reference.

### IN: value membership

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE s.sid IN (
    SELECT e.sid
    FROM Enrolment AS e
    WHERE e.score >= 85
);
```

Only S1 qualifies. A scalar IN subquery returns one column. Repeated right-side values do not multiply an outer row. Section 11 discusses NULL effects.

## 10. EXISTS, NOT EXISTS, and correlation

Source: P2 slide 6; the Tutorial 2 topic list includes NOT EXISTS.

A correlated subquery references the current outer row, as in `e.sid=s.sid`. Interpret it as asking an existence question for each student; this does not require the engine to execute the complete inner query once per row.

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE EXISTS (
    SELECT 1
    FROM Enrolment AS e
    WHERE e.sid = s.sid AND e.score IS NULL
);
```

S1, S2, and S3 qualify. EXISTS tests for rows, not the selected constant 1. In this ordinary existence query, multiple inner matches still produce one result per outer student. EXISTS does not independently remove duplicates already present in the outer input.

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM Enrolment AS e
    WHERE e.sid = s.sid
);
```

Only S4 qualifies. “Never” means **no matching row**, not one row with `cid <> 'C1'`. Omitting the correlation can make any enrolment in the entire table determine the condition for all students.

## 11. NOT IN with NULL: explain the counterexample

Source: Tutorial 2 on page 2 of the plan; additional reference: [PostgreSQL IN/NOT IN](https://www.postgresql.org/docs/18/functions-subquery.html#FUNCTIONS-SUBQUERY-NOTIN).

For non-NULL numbers, `80 NOT IN (90,NULL)` is `80<>90 AND 80<>NULL`, yielding UNKNOWN and rejection by WHERE. `90 NOT IN (90,NULL)` is FALSE because an equal value exists. **A NULL on the right does not force every NOT IN result to be identical.**

| Situation | Scalar membership result |
|---|---|
| An equal right-side value exists | IN is TRUE; NOT IN is FALSE |
| No equal value, NULL participates, and the right side is nonempty | Can be UNKNOWN rather than definite nonmembership |
| Right side empty | IN is FALSE; NOT IN is TRUE |

This particular query for unenrolled students is safe under the running example:

```sql
SELECT s.sid, s.sname
FROM Student AS s
WHERE s.sid NOT IN (SELECT e.sid FROM Enrolment AS e);
```

Both sid columns are guaranteed non-NULL, so S4 is returned. Replacing them with nullable columns invalidates that reasoning. Filtering NULL out of the right side does not automatically settle a NULL left side's meaning. Correlated NOT EXISTS also requires an explicit interpretation of NULL-key matching; it is not unconditionally equivalent to NOT IN.

## 12. UNION, INTERSECT, EXCEPT, and identity

Source: P2 slide 9; corresponds to set operations in Chapter 05.

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

The result is S2. The two department conditions need not hold for one enrolment row: each side finds students separately, then intersects their identities.

| Operation | Default behaviour |
|---|---|
| UNION | Combine and remove duplicate output tuples |
| UNION ALL | Combine and retain multiplicities |
| INTERSECT | Common tuples, deduplicated |
| EXCEPT | Left tuples absent from the right, deduplicated; direction matters |

Inputs require equal column counts and compatible types at corresponding positions. SQL set operations align columns positionally; unlike the course's named relational-algebra convention, equal column names are not required. INTERSECT ALL and EXCEPT ALL have multiplicity semantics; distinguish them from the default deduplicated forms rather than treating ALL as decorative.

Projecting sname on each side first would combine S1's CS enrolments with S3's Math enrolment through the shared name Amy. Work with sid first, then join or use IN/EXISTS to obtain names.

## 13. Every target: no required match is missing

Source: P2 slides 10–11. This original example translates Chapter 05's method into SQL; it is not a tutorial answer sheet.

Start with Student candidates and exclude anyone for whom a CS course exists without a corresponding enrolment:

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

Only S1 qualifies. The innermost query looks for a student–course match; the middle query looks for a target with a missing match; the outer query requires no such target. This example explicitly allows enrolment in any term. If a specific term is required, state the corresponding target and enrolment scope.

Every target must be covered, but extra non-CS courses are allowed. Repeating one course cannot compensate for a missing course. Derive targets from complete Course, not only courses someone has already taken.

If hypothetically no CS courses exist, this returns all Students, including S4: no target can be missing. Add a nonempty-target requirement if the question demands one. P2 slide 11 enumerates candidates from Sells and therefore returns only bars occurring in Sells when its target set is empty. That differs from starting with all Student candidates here; connect this to Chapter 05's empty-divisor discussion.

## 14. Remaining slide material and scope

### ANY / ALL [recognition supplement]

Source: P2 slides 7–8. Week 6 lists advanced subqueries and set comparison. This section only identifies the notation rather than imposing extra Test 1 depth.

`x > ANY (subquery)` asks whether at least one comparison is TRUE; `x > ALL (subquery)` asks whether all are TRUE. For an empty right side, ANY is FALSE and ALL is TRUE. NULL may produce UNKNOWN. Replacing ALL with a MAX comparison is not unconditional because empty or NULL input can change the meaning.

### DDL, data modification, views, and PL/pgSQL

P2 slides 25–52 also cover CREATE TABLE, keys, INSERT, DELETE, UPDATE, views, and schema changes. Connect these to Chapters 03–04 without assuming that every topic in that file is a Test 1 query priority:

- PRIMARY KEY combines uniqueness and non-nullability. FOREIGN KEY does not automatically require non-NULL values, and one ordinary foreign key alone does not preserve 1:1.
- DELETE removes rows; DROP TABLE removes the table structure. UPDATE without WHERE affects the whole table. These commands are explained, not executed.
- An ordinary view is an interface defined by a query. Do not read “does not take up space” as claiming that even its definition metadata occupies no storage; it also differs from a materialized view storing results.
- PL/pgSQL, indexes, transactions, and normalization are outside this chapter.

## 15. Query-writing checks and revision checklist

1. **Specify result granularity.** One row per student, enrolment, distinct course, or group?
2. **Check schemas and complete join keys.** Pay attention to sid, cid, and term; distinguish student majors from course departments.
3. **Write row predicates and handle NULL.** WHERE retains only TRUE; choose IS NULL, IN, or EXISTS appropriately.
4. **Decide duplicate requirements.** Is DISTINCT appropriate to the result, or masking a faulty join?
5. **Group before filtering groups.** Explicitly group ordinary selected columns and distinguish COUNT(*), COUNT(column), and COUNT(DISTINCT column).
6. **Check subquery shape and correlation.** Is a scalar result at most one row? Does existence concern the current outer entity?
7. **Check boundaries.** Namesakes, repeated enrolments, missing scores, no matches, multiple matches, and empty targets; add ORDER BY when order matters.

| Common confusion | Distinction |
|---|---|
| UNKNOWN / FALSE | Different logical results; WHERE retains neither |
| DISTINCT / GROUP BY | Output deduplication / forming statistical groups; not mechanical substitutes |
| WHERE / HAVING | Filter rows before grouping / filter groups after aggregation |
| COUNT(*) / COUNT(score) | All input rows / non-NULL score rows |
| EXISTS / scalar subquery | Any rows? / treat the result as one value |
| NOT IN / NOT EXISTS | Compare a value set / test correlated matches; not unconditionally equivalent with NULL |
| Every / only | Cover all required targets / exclude associations outside the target |
| SQL set operation / ordinary SELECT | Deduplicates by default / retains duplicates by default |

These are learning goals, not a formal practice paper or an official mark allocation:

- [ ] State the written clause order and logical query stages.
- [ ] Work out basic queries, DISTINCT, self-joins, and ordering with secondary keys.
- [ ] Explain with three-valued logic why missing scores do not satisfy `score<>90`.
- [ ] Check complete conditions for ordinary and cross-term joins.
- [ ] Calculate the three COUNT variants and all-NULL/empty-input aggregates.
- [ ] Explain how WHERE and HAVING change the statistical result.
- [ ] Distinguish scalar, IN, and EXISTS subquery requirements.
- [ ] Explain the NULL counterexample for NOT IN and the safe non-NULL sid case.
- [ ] Perform identity-based set operations before projecting names.
- [ ] Explain all three levels of double NOT EXISTS and its empty-target behaviour.

Useful short-answer formulations:

> WHERE retains only rows for which its condition evaluates to TRUE.

> COUNT(*) counts rows, whereas COUNT(column) counts non-NULL values in that column.

> WHERE filters input rows; HAVING filters groups after aggregation.

> EXISTS tests whether a subquery returns any rows, not the values in its SELECT list.

> A NOT IN comparison can evaluate to UNKNOWN when NULL participates and no equal value is found.

> A universal requirement can be expressed as the absence of a required target without a matching association.

## Sources and preparation record

- Lecturer's decks: [SQLpart1.pptx](../../slides/SQLpart1.pptx) and [SQLpart2.pptx](../../slides/SQLpart2.pptx). Core sources are P1 slides 3–58 and P2 slides 2–24. Text was read and original slides P1 18, 31, 35–36, 51, 55, 58 and P2 2, 6, 9, 11, 15–16, 20, 22, 24 were visually inspected. P2 slides 25–52 are used only for scope recognition.
- Teaching scope: [CSC5041_Teaching_Plan.pdf](../../syllabus/CSC5041_Teaching_Plan.pdf), page 1, Weeks 5–6, and page 2, Tutorial 2. Supporting questions: [Tutorial 2.pdf](../../slides/Tutorial%202.pdf), page 1. Chapter 05 records the sheet's Week 6 versus plan's Week 5 discrepancy; this chapter infers no rescheduling.
- Additional checks: PostgreSQL 18 official documentation on [comparisons](https://www.postgresql.org/docs/18/functions-comparison.html), [subqueries](https://www.postgresql.org/docs/18/functions-subquery.html), [aggregates](https://www.postgresql.org/docs/18/functions-aggregate.html), and [table expressions](https://www.postgresql.org/docs/18/queries-table-expressions.html), read online this turn for NULL, subquery cardinality, aggregation, and related boundaries. This does not imply that the lecturer requires PostgreSQL 18.
- Prepared by Codex in the main conversation. Bilingual structure, query semantics, deductions, and links were self-checked; the independent Reviewer's conclusion is reported in this turn's delivery message. **No SQL was executed and no PostgreSQL runtime verification is claimed.** Code/experimental execution is N/A. No submission directory was created; lecturer originals and Chapters 01–05 were unchanged.
- Input SHA-256: SQLpart1 `aa28c989fb3674e780418c78c483bba20ff5a50b7da067b0341e60410a68c8ed`; SQLpart2 `acd25cbd4bbd246f8901ada4c437c3f2d00873385961475cd4c941e9089bf45c`; Tutorial 2 `72c016526c1c0ff02c10fcb5f7f964c1184999c684228671025800936a6cabac`; syllabus teaching plan `31380a7fe6504e46541b6db0bb2f24859c69188bfeb9681dca73354ebeb68295`.
- With this chapter, the planned topics in Chapters 01–06 now have notes. The next stage, when requested, is to prepare two English practice papers based on the tutorials. No papers were generated this turn.
