# CSC5041 — Practice Paper 1

**Scope:** Weeks 1–5 · **Total:** 100 marks · **Suggested time:** 120 minutes

Original practice questions based on the teaching plan and Tutorials 1–2. The time and marks are practice settings, not the lecturer's announced examination format. No answers are included.

## Instructions

- Attempt all questions. Label answers by question and subpart.
- Prefer formulas, schemas, diagrams, and SQL. Use at most one or two sentences when an explanation is requested.
- Use the lecture's Chen ER notation. Underline primary keys and mark foreign-key attributes with `*`; state complete composite foreign-key groups and targets.
- Relational algebra uses set semantics. You may use σ, π, ρ, ∪, ∩, −, ×, ⋈, ÷, and γ. Define any intermediate relations.
- Write PostgreSQL-compatible SQL using ordinary SELECT, joins, aggregation, and subqueries. No window functions, recursive queries, or PL/pgSQL are needed.
- Names and titles need not be unique. Unless stated otherwise, all attributes except explicitly nullable ones are non-NULL, and every declared foreign key is valid.
- Each question is independent. Q2's ER model is not the schema used in Q3–Q5.

## Q1. Database fundamentals [10 marks]

**(a) [2 marks]** Distinguish a database from a DBMS. Give one short definition of each.

**(b) [3 marks]** Name the three-schema level corresponding to each description:

1. A research assistant sees only the projects assigned to that assistant.
2. The complete logical definitions of Scientist, Project, and their constraints.
3. The organization of database records into disk pages and access paths.

**(c) [3 marks]** Classify each change as demonstrating physical data independence, logical data independence, or neither. Assume any stated interface preservation is achieved successfully.

1. A file organization changes while relation definitions and application queries remain unchanged.
2. A logical relation is split into two, but suitable mappings preserve the existing external interfaces.
3. A scientist's phone number is replaced by a new value.

**(d) [2 marks]** Classify `CREATE TABLE` and `UPDATE` as DDL or DML, using the course's terminology.

## Q2. Conceptual design and relational mapping [30 marks]

A research organization maintains the following information.

A research centre has a unique `centreID`, a name, an address consisting of city and street, and zero or more phone numbers. A centre employs one or more scientists. A scientist has a unique `scientistID`, a name, and a salary, and works at exactly one centre. Each centre has exactly one head, who must be a scientist employed at that centre. A scientist heads at most one centre.

A project has a unique `projectID`, a title, and a budget, and is hosted by exactly one centre. A centre may host zero or more projects. Scientists may work on zero or more projects, and each project must have one or more scientists working on it. Record `hoursPerWeek` for each scientist–project association. Each recorded value is positive, and a scientist's total `hoursPerWeek` across all projects must not exceed 40. Scientists may work on projects hosted by other centres.

A project may have zero or more experimental runs. Runs are numbered `1,2,3,...` within their project; different projects may use the same `runNo`. Each run has a date and an outcome and is led by exactly one scientist. A scientist may lead zero or more runs. No further condition connects leadership with project membership.

A material has a unique `materialCode`, a name, and a unit cost. A run may consume zero or more materials; a material may be consumed by zero or more runs. Record the quantity consumed for each run–material pair. There is at most one such association per pair.

**(a) [5 marks]** List entity types and attributes. Identify keys; for each weak entity give its partial key, owner, and full identifier.

**(b) [9 marks]** Draw the ER diagram, including attributes, relationship attributes, cardinality ratios, participation constraints, and identifying relationships. State any additional assumptions.

**(c) [12 marks]** Produce the relational schema using the standard mapping. Show all primary keys, foreign keys, and any uniqueness or non-null requirements needed to preserve the stated associations. State which relationships or attributes create separate relations.

**(d) [4 marks]** Give two stated business constraints not guaranteed by the primary-key and foreign-key declarations in your mapping alone. Express each constraint as a formula or a short sentence, and name a suitable enforcement mechanism.

## Q3. Relational integrity [10 marks]

Use the following independent schema:

```text
Catalogue(supplierID, partNo, label)
  PK{supplierID, partNo}

Request(requestID, supplierID, partNo, quantity)
  PK{requestID}
  FK{supplierID,partNo} → Catalogue{supplierID,partNo}
  All attributes NOT NULL; quantity is an integer with CHECK(quantity > 0).
```

Initial state:

| Catalogue.supplierID | partNo | label |
|---|---|---|
| S1 | P1 | Sensor |
| S2 | P2 | Cable |

| Request.requestID | supplierID | partNo | quantity |
|---|---|---|---|
| R1 | S1 | P1 | 2 |

Assess each operation **independently from this initial state**. No automatic cascades or reference repairs are configured. State **valid/invalid** and the applicable constraint or reason. **[2 marks each]**

1. Insert `(S1,P1,'Replacement sensor')` into Catalogue.
2. Insert `(R2,S1,P2,1)` into Request.
3. Insert `(NULL,S2,P2,1)` into Request.
4. Delete `(S1,P1,'Sensor')` from Catalogue.
5. Change the quantity of Request R1 from 2 to −1.

## Schema for Q4 and Q5

```text
Trainee(tid, tname, track, level)       PK{tid}
Module(mid, title, area, hours)        PK{mid}
Enrolment(tid, mid, term, score)       PK{tid,mid,term}
Trainer(rid, rname, area)              PK{rid}
Teaching(rid, mid, term)               PK{rid,mid,term}
```

- Enrolment.tid references Trainee.tid; Enrolment.mid and Teaching.mid reference Module.mid; Teaching.rid references Trainer.rid.
- A Teaching tuple states that a trainer teaches that module in that term. A module offering may have several trainers.
- A trainee may take the same module in different terms. `score` is numeric and NULL until assessment. All other attributes are non-NULL.
- Terms are strings such as `'2026F'`. Module hours are positive numbers. Names and titles may repeat.
- “Has taken” means has an Enrolment tuple, whether or not score is available.

## Q4. Relational algebra [25 marks]

**(a) [3 marks]** Return the titles of modules in area `'Data'` with more than 12 hours.

**(b) [4 marks]** Return the names of trainees who took at least one module taught by trainer `'R7'` in the same term as their enrolment. Consider all terms.

**(c) [5 marks]** Return the names of trainees who have taken:

1. At least one `'Data'` module or at least one `'Systems'` module, using a set union.
2. At least one module from each of those two areas, using a set intersection.

**(d) [4 marks]** Return the names of trainees who have never enrolled in any module. Use set difference.

**(e) [6 marks]** Return the names of trainees who have taken every module in area `'Data'`. Enrolments may be in different terms, and additional modules in other areas are allowed. Assume at least one Data module exists. Use division, or a correct expression using basic operators.

**(f) [3 marks]** For each area represented in Module, return the area, number of modules, and average number of hours. Use γ.

## Q5. SQL [25 marks]

**(a) [3 marks]** Return `mid`, `title`, and `hours` for Data modules with at least 12 hours. Sort by hours descending, then mid ascending.

**(b) [5 marks]** Return distinct trainee IDs and names for trainees enrolled in term `'2026F'` in a module taught by trainer `'R7'` in that term. Write the complete joining conditions.

**(c) [5 marks]** For each trainee who enrolled in at least two distinct modules in `'2026F'`, return `tid`, the number of distinct modules, and the average available score for that term. Unassessed enrolments count towards the module requirement. Return only groups that satisfy it, sorted by tid.

**(d) [5 marks]** Return trainee IDs and names of trainees with no assessed enrolment in any term, including trainees with no enrolments. An enrolment is assessed exactly when score is non-NULL. Use NOT EXISTS.

**(e) [7 marks]** This subpart uses only the following table:

| TestScore.attemptID | score |
|---|---|
| A1 | 90 |
| A2 | 80 |
| A3 | NULL |
| A4 | 80 |
| A5 | NULL |

1. Give the single result row of the following query. **[3 marks]**

   ```sql
   SELECT COUNT(*), COUNT(score), COUNT(DISTINCT score)
   FROM TestScore;
   ```

2. Give the attempt IDs returned below, and explain the treatment of NULL in one sentence. **[2 marks]**

   ```sql
   SELECT attemptID FROM TestScore WHERE score <> 80;
   ```

3. Give the attempt IDs returned below, and justify the result in one sentence. **[2 marks]**

   ```sql
   SELECT attemptID FROM TestScore WHERE score NOT IN (90, NULL);
   ```

---

**End of Paper 1 — 100 marks.**

Scope sources: [Teaching plan](../../syllabus/CSC5041_Teaching_Plan.pdf), p. 1 Weeks 1–5 and p. 2 Tutorials 1–2; [Tutorial 1](../../slides/Tutorial1.pdf), p. 1; [Tutorial 2](../../slides/Tutorial%202.pdf), p. 1. Questions, scenarios, data, timings, and mark allocations in this paper are original practice material.
