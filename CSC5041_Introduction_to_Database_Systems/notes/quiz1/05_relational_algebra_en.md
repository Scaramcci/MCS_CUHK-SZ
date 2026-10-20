# 05 Relational Algebra: English Study Notes

CSC5041 · In-class Test 1 revision · 19 October 2026

## Scope and learning goals

This chapter follows [03 Relational Model](03_relational_model_and_integrity_en.md) and [04 ER Mapping](04_er_to_relational_mapping_en.md). The main source is the lecturer's [Relational_Algebra.pptx](../../slides/Relational_Algebra.pptx), 61 slides. Unless another file is named, slide numbers refer to their order in that deck.

The scope corresponds to Week 4 on page 1 of the teaching plan. Tutorial 2, page 1, Question 1(a)(i)–(vi), covers selection/projection, joins, set operations, students taking no courses, every target course, and grouped aggregation. Aggregation is not part of the classical basic algebra, but both slides 58–59 and the tutorial cover it, so it is included here. SQL belongs to Chapter 06.

After studying this chapter, you should be able to explain input and result schemas, compose expressions from written requirements, and detect incorrect joins, premature projection, name collisions, and division candidate-scope problems. Original data and results are static teaching deductions, not real data, database execution results, or a new practice paper.

## 1. Notation and closure

Source: slides 2–4 and 55–61.

Relational algebra takes relations as inputs and produces relations that can be used in further operations. This is **closure**. The lecture calls it a procedural DML: an expression specifies a composition of logical operations, not an obligatory physical execution sequence for the database engine.

| Operation | Notation used here | Main purpose |
|---|---|---|
| Selection | `σ_{condition}(R)` | Filter rows |
| Projection | `π_{attributes}(R)` | Retain columns and remove duplicates |
| Rename | `ρ_{NewName(newAttributes)}(R)` | Distinguish roles or align attribute names |
| Union, intersection, difference | `R ∪ S`, `R ∩ S`, `R − S` | Either, both, or left but not right |
| Cartesian product | `R × S` | All tuple pairings |
| Theta join | `R ⋈_{condition} S` | Pairings satisfying a condition |
| Natural join | `R ⋈ S` | Match all common attributes and merge them |
| Division | `R ÷ S` | Candidates associated with every target in S |
| Grouping and aggregation | `γ_{groups; aggregates}(R)` | Statistics per group |

Braces `{...}` in code blocks represent subscripts for stable Markdown display. `←` names an intermediate relation without updating the stored data. Renaming changes relation/attribute identifiers, not existing values; a full attribute-renaming list corresponds positionally to the original schema.

**Examples use set semantics and contain no NULL values.** Projection eliminates duplicates, and there is no implicit row order. Do not import SQL duplicate handling, NULL, or three-valued logic into these classical operations without defining the extension. NULL in the tutorial's grade does not affect expressions using only other attributes; NULL query semantics belong to Chapter 06.

## 2. Running example: specify the inputs first

This is an original simplified enrolment database, **not the tutorial schema**. It omits term; Takes records whether a student has taken a course.

```text
Student(sid, sname, major)          PK{sid}
Course(cid, title, dept, credits)   PK{cid}
Takes(sid, cid)                    PK{sid,cid}
Takes.sid → Student.sid; Takes.cid → Course.cid
```

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

Takes:

| sid | cid |
|---|---|
| S1 | C1 |
| S1 | C2 |
| S2 | C1 |
| S2 | C3 |
| S3 | C3 |

S1 and S3 share a name: **names are not identifiers**. S3 majors in CS but has taken only a Math course: **a student's major and a course's department are different conditions**. S4 has no enrolments and must remain available when considering “never” and missing zero-count groups.

## 3. Selection σ: filter tuples, retain all attributes

Source: slides 5–10 and 18.

```text
σ_{dept='CS' ∧ credits>3}(Course)
```

The result schema remains `(cid,title,dept,credits)` and contains only `(C1,Databases,CS,4)` here. Selection does not remove columns or change retained values. Conditions can compare an attribute to a constant or another attribute and combine predicates with `∧`, `∨`, and `¬`.

Consecutive selections can be combined and reordered:

```text
σ_{p}(σ_{q}(R)) = σ_{p∧q}(R) = σ_{q}(σ_{p}(R))
```

The conditions must be defined over R's attributes. “CS courses with more than 3 credits” can use consecutive selections; it differs from “CS courses or courses with more than 3 credits.”

**Do not confuse SQL SELECT with algebraic selection:** σ filters rows; the SQL SELECT list mainly specifies output columns.

## 4. Projection π: retain attributes and eliminate duplicates

Source: slides 11–18.

```text
π_{dept}(Course) = {(CS), (Math)}
```

Two CS courses still produce only one CS tuple because the result is a set. The result schema contains only dept; cid, title, and credits are no longer available.

Combine selection and projection:

```text
π_{title}(σ_{dept='CS' ∧ credits>3}(Course))
```

Its schema is `(title)` and its result is `{(Databases)}`. Read from the innermost parentheses outward: filter courses, then retain titles.

### Do not discard attributes needed later

```text
Valid:   π_{title}(σ_{dept='CS'}(Course))
Invalid: σ_{dept='CS'}(π_{title}(Course))
```

The second expression projects dept away before trying to use it. In general, the following requires all attributes used by p to remain in X:

```text
π_X(σ_p(R)) = σ_p(π_X(R))
```

Nested projections satisfy `π_X(π_Y(R)) = π_X(R)` when `X ⊆ Y`. Requesting an attribute already removed by the inner projection makes the expression undefined, not an empty result.

## 5. Rename ρ: distinguish roles and conflicting names

Source: slides 55–56 and 60.

Renaming aligns schemas for set operations, distinguishes roles in self-joins, and prevents attribute conflicts in products and conditional joins. For pairs of distinct students with the same major:

```text
A ← ρ_{A(aid,aname,amajor)}(Student)
B ← ρ_{B(bid,bname,bmajor)}(Student)
Pairs ← π_{aid,bid}(A ⋈_{amajor=bmajor ∧ aid<bid} B)
```

Assume ID order `S1<S2<S3<S4`. The result is `{(S1,S3),(S2,S4)}`. `aid<bid` excludes self-pairings and reverse duplicates. Using only `aid≠bid` returns both `(S1,S3)` and `(S3,S1)`.

Renaming does not change Amy's actual name. A natural join of Student with an unrenamed copy of itself does not enumerate different-student pairs: it matches equality on all common attributes.

## 6. Union, intersection, and difference: align schemas first

Source: slides 19–32 and 56.

| Operation | Tuples retained | Commutative? |
|---|---|---|
| `R ∪ S` | In R or S, including those in both | Yes |
| `R ∩ S` | In both R and S | Yes |
| `R − S` | In R but not S | Generally no |

All three require **union compatibility**. Slide 19 requires a one-to-one correspondence of attributes with the same names and domains. Project matching attribute groups and rename/align them if necessary. Equal column counts alone do not make relations compatible.

Build two **student-ID sets** in the running example:

```text
CSIDs   ← π_{sid}(Takes ⋈ σ_{dept='CS'}(Course))
MathIDs ← π_{sid}(Takes ⋈ σ_{dept='Math'}(Course))
```

Then `CSIDs={S1,S2}` and `MathIDs={S2,S3}`. The shorthand below omits parentheses around individual one-attribute tuples.

| Expression | Result here | Meaning |
|---|---|---|
| `CSIDs ∪ MathIDs` | `{S1,S2,S3}` | At least one course from either department |
| `CSIDs ∩ MathIDs` | `{S2}` | Courses from both departments |
| `CSIDs − MathIDs` | `{S1}` | CS courses but no Math courses |
| `MathIDs − CSIDs` | `{S3}` | Math courses but no CS courses |

“Or” here is inclusive. “Exactly one category” needs an additional exclusion, for example `(CSIDs−MathIDs) ∪ (MathIDs−CSIDs)`.

### “Never enrolled” is not an inequality on one record

```text
NeverIDs ← π_{sid}(Student) − π_{sid}(Takes)
```

The result is `{S4}`. Start with all candidate students, then subtract those with at least one enrolment. A row satisfying `cid≠C1` does not show that its student never took C1: the same student may have taken both C1 and C3.

## 7. Products and joins: all pairings versus correct pairings

Source: slides 33–47 and 61.

### Cartesian product ×

Pair each R tuple with each S tuple. If R has m rows and S has n, the product has `m×n` rows. After disambiguating attribute names, its degree is the sum of the input degrees. Student×Course has `4×3=12` rows and seven attributes here.

A product does not automatically match primary and foreign keys. Rename conflicting attributes first. In conditional joins, this chapter also uses `relation.attribute` to identify origins; this can be understood as correspondingly qualifying/renaming conflicting attributes.

### Theta and equi-joins

```text
R ⋈_θ S = σ_θ(R × S)
```

The identity assumes disambiguated attributes and a well-defined condition. A theta condition can compare values; a join using only equality comparisons is an equi-join.

```text
Takes ⋈_{Takes.cid=Course.cid} Course
```

Only matching course IDs are paired, producing five rows here. An ordinary equi-join retains both copies of the join attributes, distinguished by qualified names. **Equal values do not automatically merge the two columns.**

### Natural join ⋈

A natural join equates **all identically named attributes** and retains one copy of each. With no common attribute names, it reduces to a Cartesian product.

```text
Student ⋈ Takes ⋈ Course
```

Here the first join shares only sid, and the next shares only cid. The result schema is `(sid,sname,major,cid,title,dept,credits)`, with five tuples.

A natural join does not infer which columns should match semantically. If Instructor and Course both contain dept, it can impose equality between instructor and course departments. If that is not required, use explicit join conditions or rename unrelated common attributes first.

Slide 37 connects equality filtering followed by removing a duplicate join column with natural joining. Apply the all-common-attributes rule on slides 40–41: not every equi-join followed by projection is automatically a natural join. Joins retain matching combinations; they do not automatically add a row for unenrolled S4.

## 8. Composing queries: preserve identity, project names last

Source: slides 25–32 and 43–47. The shared-name counterexample is original.

To find names of students who have taken both CS and Math courses, intersect IDs and then join Student:

```text
BothIDs ← CSIDs ∩ MathIDs
Answer  ← π_{sname}(Student ⋈ BothIDs)
```

This returns `{(Ben)}`. If names are projected first, both sets contain Amy: S1 supplies the CS occurrence and S3 supplies the Math occurrence. Intersecting names wrongly returns Amy by combining **two different people** into one person satisfying both conditions.

For “CS but no Math,” also subtract IDs first. The correct student S1 is named Amy, but subtracting the name sets removes Amy. **Projection distributes over union, but cannot generally be moved ahead of intersection or difference.**

If only names are requested, the final projection merges namesakes as a name set. Retain sid when students must remain distinguishable. Requested name output does not make names keys.

### Do not drop the tutorial's term prematurely

Tutorial 2's Enrolled and Teaches both include cid and term. Taking a course taught by an instructor requires matching the course and its offering term. Matching only cid can incorrectly associate an enrolment from another term with that instructor.

Takes deliberately omits term here and is not a direct replacement for the tutorial's complete schema. Check the full linking attribute group before reusing a template.

## 9. Division ÷: express “every target is covered”

Source: slides 48–54 and 61.

Let R have disjoint attribute groups X and Y, and let S have exactly attributes Y. `R ÷ S` returns X values paired in R with **every tuple of S**, taking candidates from `π_X(R)`.

```text
R(X,Y) ÷ S(Y) → Result(X)
```

This is not numeric division or matching any one target. Identify the candidate group X and the required target group Y first.

### Students who have taken every CS course

```text
R ← π_{sid,cid}(Takes)
D ← π_{cid}(σ_{dept='CS'}(Course))
AllCSIDs ← R ÷ D
```

D contains `{C1,C2}`. S1 covers both; S2 covers only C1; S3 covers only C3. The result is `{S1}`. Names can then be returned with `π_{sname}(Student ⋈ AllCSIDs)`.

- Take “all CS courses” from the complete Course relation, not only existing enrolments, or an unchosen required course may disappear from the target set.
- Taking every CS course permits additional Math courses. It does not mean taking only CS courses.
- Project the dividend to `(sid,cid)`. Extra sname, term, or grade attributes would remain in the quotient and change which fixed candidates must cover all targets.

### Multiple target attributes and result schemas

Slides 53–54 use R(A,B,C) and S(B,C):

```text
R ÷ S          → returns A; covers every (B,C) pair in S
R ÷ π_C(S)     → returns (A,B); each fixed (A,B) covers every C
```

These ask different questions. For the given slide instance, the first returns `{a1}`, while the second returns `{(a1,b1),(a3,b2)}`. Seeing “all” does not remove the need to inspect the target schema.

## 10. Expanding division with difference, and empty targets

Source: slide 57. Candidate-universe and empty-target discussion clarifies the definition's boundaries.

Rewrite “every target is present” as “no required target is missing”:

```text
Candidates ← π_X(R)
Required   ← Candidates × S
Missing    ← Required − R
Bad        ← π_X(Missing)
Result     ← Candidates − Bad
```

R has exactly `(X,Y)` here; align the schemas of Required and R. Project wider inputs to X and Y first. X and Y denote attribute groups, not a set difference between relation names.

In the running example, Candidates contains `{S1,S2,S3}`. Required contains six student–course pairs. Missing contains `(S2,C2)`, `(S3,C1)`, and `(S3,C2)`, so Bad is `{S2,S3}` and only S1 remains. Additional Math pairs in R do not create missing pairs and therefore do not disqualify S1.

### Empty targets require an explicit candidate scope

If S is empty, Required and Missing are empty, and standard division returns `π_X(R)`. It **does not automatically include students who never occur in R**.

If all Student tuples should be candidates for a universal condition, use an explicit universe U:

```text
U      ← π_{sid}(Student)
Bad    ← π_{sid}((U × D) − R)
Result ← U − Bad
```

R and D are from Section 9. For nonempty D this agrees with standard division under the running example's valid foreign keys. For empty D it returns all U, including unenrolled S4. This is the truth of a universal condition over an empty target set, not a guarantee that every practical question allows an empty target. State assumptions if the question excludes that case.

## 11. γ: grouping and aggregation

Source: slides 58–59 and Tutorial 2, Question 1(a)(vi). The notation below is the convention used in these notes.

γ supports COUNT, SUM, AVG, MIN, and MAX. `γ_{groupAttributes; aggregate→resultName}(R)` produces one tuple per group, retaining group attributes and adding summary values.

```text
Stats ← γ_{dept; COUNT(cid)→nCourses, AVG(credits)→avgCredits}(Course)
```

| dept | nCourses | avgCredits |
|---|---|---|
| CS | 2 | 3.5 |
| Math | 1 | 4 |

Filter groups with more than one course using `σ_{nCourses>1}(Stats)`; only CS remains. Define an aggregate result name in γ before using it in an outer selection.

### What object is being counted?

- Course has one tuple per course and unique cid, so COUNT(cid) counts courses here.
- Joining Takes first can give several tuples for one course, one per student. Counting directly may then count enrolment pairings rather than distinct courses.
- To count distinct objects, deduplicate at the correct identifier level. For example, project a joined result to `(dept,cid,credits)` before grouping. Projecting only `(dept,credits)` can merge different courses with equal credits.
- `γ_{sid; COUNT(cid)→nTaken}(Takes)` produces groups for S1, S2, and S3 with counts 2, 2, and 1. It does not automatically generate S4 with a zero count.

All groups aggregated here are nonempty and contain no NULL. Slide 58 raises NULL but does not fully specify its semantics there. Empty-input and NULL handling require explicit conventions; SQL COUNT and NULL details belong to Chapter 06.

## 12. Equivalent rewrites: check the conditions first

Source: slides 10, 15–17, 57, and 60. Conditions below explain the relevant definitions.

| Rewrite | Condition or meaning |
|---|---|
| `σ_p(σ_q(R)) = σ_{p∧q}(R)` | Both predicates are defined |
| `π_X(π_Y(R)) = π_X(R)` | `X ⊆ Y` |
| `π_X(σ_p(R)) = σ_p(π_X(R))` | X retains every attribute used by p |
| `R ∩ S = R − (R − S)` | R and S are union-compatible |
| `R ⋈_θ S = σ_θ(R×S)` | Attributes are disambiguated and θ is defined |
| `π_X(R∪S) = π_X(R)∪π_X(S)` | Compatible inputs, available X attributes, and set semantics |

Replacing ∪ by ∩ or − in the last rule is not generally valid: projection can discard identity, as the namesake example in Section 8 shows. Projection pushed before a join must also retain output attributes, join attributes, and attributes needed for later filters.

Slide 57 lists basic operators `σ, π, ∪, −, ×, ρ`; joins, intersection, and division can be derived from them. Aggregation on slide 58 adds statistical power. **General counting is not simply derived from these classical basic operators.** Distinguish derived operations from aggregation that extends expressive power.

## 13. A procedure for translating English requirements

Source: slides 25–32, 43–54, and 60–61; the steps below organize the material into a workflow.

1. **Specify the result schema.** Student IDs, names, course titles, or one statistics tuple per department?
2. **Identify objects and the candidate universe.** Use keys for namesakes; “never” requires the complete candidate population.
3. **List complete join conditions.** Check keys and context such as term; do not natural-join merely because names match.
4. **Translate quantifiers and logical words.** At least one usually uses joins/projection; or uses union; both uses intersection; never subtracts existing matches from all candidates; every uses division or removal of candidates with missing pairs.
5. **Keep attributes needed later.** Filter, join, and make identity-based set decisions before projecting presentation attributes.
6. **Track intermediate schemas.** Are selection attributes available? Are difference inputs compatible? Does division return the intended candidate attributes?
7. **Try small counterexamples.** Shared names, several matches, no matches, extra courses, one missing target, and an empty target.

The six Tutorial 2(a) categories correspond to selection/projection, cross-relation joins, union/intersection, difference, division, and γ. These notes teach the concepts and methods; they do not reproduce a complete tutorial answer set or create the later English practice papers.

## 14. Common distinctions, revision checklist, and short-answer language

| Pair | Distinction |
|---|---|
| σ / π | Filters rows and preserves schema / retains columns and deduplicates |
| Undefined expression / empty result | Referring to an unavailable attribute is an error / a valid expression can have no matches |
| Union-compatible / equal column count | Aligned attributes, names, and domains under the lecture convention / column count alone is insufficient |
| Or / exactly one category | Includes both / must exclude both |
| Equi-join / natural join | Explicit equality with attribute copies retained / equality on all common names with columns merged |
| Student name / identifier | Names can coincide / keys track the same object |
| Some record does not match / never matches | Existence of a nonmatching record / absence of every matching record |
| Every / only | Covers the required targets / excludes objects outside the target set |
| Division targets / candidates | All tuples of S / usually values from `π_X(R)` |
| Counting join rows / counting distinct courses | Pairing count / requires retaining course identity and deduplicating appropriately |

These are learning goals, not a formal practice test or an official mark allocation:

- [ ] State input requirements, result schemas, and duplicate behaviour for every operator.
- [ ] Work out selections, projections, ID set operations, and natural joins on the example.
- [ ] Use renaming correctly for two roles of one relation.
- [ ] Explain premature name projection with the namesake counterexample.
- [ ] Explain why tutorial joins require checking term.
- [ ] Identify division's X, Y, and complete target relation and calculate the quotient.
- [ ] Expand division using differences of missing required pairings.
- [ ] Distinguish standard division from an explicit-universe version for empty targets.
- [ ] Calculate grouped statistics and detect join multiplication or absent zero-count groups.
- [ ] State the conditions required for each equivalent rewrite.

Useful short-answer formulations:

> Selection filters tuples while preserving the relation's attributes.

> Projection retains the specified attributes and eliminates duplicate tuples.

> Union, intersection, and difference require union-compatible relations.

> A natural join matches all common attributes and retains one copy of each common attribute.

> Perform identity-based set operations before projecting names, because different entities may share a name.

> Division returns candidates associated with every tuple in the divisor.

> Universal conditions can be expressed by removing candidates that have a missing required pairing.

> The object counted depends on the input tuples and the identifiers retained before aggregation.

## Sources and preparation record

- Main lecture deck: [Relational_Algebra.pptx](../../slides/Relational_Algebra.pptx), text of slides 1–61 read. Original diagrams/formulas on slides 7, 10, 17, 19, 37–38, 40, 42, 48, 50, 53–54, 57, and 60–61 were visually inspected for selection/projection conditions, union compatibility, joins, division, and basic-operator notation.
- Scope: [CSC5041_Teaching_Plan.pdf](../../syllabus/CSC5041_Teaching_Plan.pdf), page 1, Week 4, and page 2, Tutorial 2. Supporting questions: [Tutorial 2.pdf](../../slides/Tutorial%202.pdf), page 1, Question 1(a)(i)–(vi); the original page and underlined keys were inspected. The plan labels Tutorial 2 Week 5, while the question sheet labels it Week 6. This chapter follows the actual topics without inferring an examination rescheduling from that discrepancy.
- The simplified schema, namesake counterexample, empty-target/candidate-universe discussion, aggregation notation, and counting boundaries are distinguished from verbatim lecture statements. Full SQL NULL and duplicate semantics are outside this chapter.
- Prepared by Codex in the main conversation. Bilingual structure, expression schemas, example deductions, and relative links were self-checked; the independent Reviewer's conclusion is reported in this turn's delivery message. No database queries were executed: examples are static analyses. Code/experimental verification is N/A. No submission directory was created; lecturer originals and Chapters 01–04 were unchanged.
- Input SHA-256: algebra deck `dcacfada73c2f482ab3b83ac7c8312cb2176932906b6d3e6cac071d01932283d`; Tutorial 2 `72c016526c1c0ff02c10fcb5f7f964c1184999c684228671025800936a6cabac`; syllabus teaching plan `31380a7fe6504e46541b6db0bb2f24859c69188bfeb9681dca73354ebeb68295`.
- Next: prepare Chapter 06 on SQL queries when requested. After all notes are complete, prepare two English practice papers based on the two tutorials.
