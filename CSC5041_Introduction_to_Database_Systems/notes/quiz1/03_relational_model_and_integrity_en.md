# 03 Relational Model and Integrity Constraints: English Study Notes

CSC5041 · In-class Test 1 revision · 19 October 2026

## Scope and learning goals

This chapter follows [02 ER Modelling](02_er_modelling_en.md). It covers “The Relational Data Model” and “integrity constraints” in Week 3 on page 1 of the teaching plan. The main source is the lecturer's [Lecture2A.pptx](../../slides/Lecture2A.pptx), slides 4–32. Unless another file is named, slide numbers below refer to their order in that deck.

After studying this chapter, you should be able to interpret relation schemas and instances, explain set properties, identify keys and foreign-key directions, distinguish key constraints from entity and referential integrity, and assess insertions, deletions, and modifications. ER mapping begins on slide 33 and belongs to Chapter 04; relational algebra belongs to Chapter 05; SQL implementation details belong to Chapter 06.

The student-enrolment data below is an **original teaching example**, not real student information, measured output, or examination questions. Clarifications of simplified slide statements are labelled explicitly.

## 1. From the ER model to the relational model

Source: slides 4–7 and 32.

Chapter 02 expresses application meaning through entities, attributes, and relationships. The relational model organizes information into a collection of interconnected **relations**. A relation can be visualized as a table; it is **not the same thing as an ER relationship** connecting entities.

| Mathematical term | Common data terminology | Meaning |
|---|---|---|
| Relation | Table | A set of tuples sharing an attribute structure |
| Tuple | Row / record | Values for a collection of attributes |
| Attribute | Column / field | A named property |
| Domain | Allowed values | The set of values permitted for an attribute |

For example, `Student(sid, name, email)` is a relation schema. `(S01, Amy, amy@example.test)` is a tuple written in that attribute order. The enrolment association between Student and Course can itself be represented by an Enrolment relation; placing tables next to each other does not encode the association.

## 2. Schemas, instances, degree, and cardinality

Source: slides 8 and 32. The formal notation and degree/cardinality terminology below are explanatory supplements.

### One relation

```text
Relation schema: Student(sid, name, email)

A relation instance:
sid   name   email
S01   Amy    amy@example.test
S02   Ben    ben@example.test
```

A relation schema specifies the relation name, attributes, and their domains. An instance is the actual set of tuples at a particular time. Common notation is `R(A1, ..., An)` and `r(R)`, or simply `r` when the schema is clear.

In the classical definition without NULL, each tuple takes one value from each attribute domain, so `r ⊆ dom(A1) × ... × dom(An)`. This specifies where values come from and which combinations are included. It does not require storing every possible combination.

| Term | What it counts | Example above |
|---|---|---|
| Degree / arity | Attributes | 3 |
| Cardinality | Current tuples | 2 |

An empty instance still has a schema: if Student has no rows, its degree remains 3 and its cardinality is 0. Here cardinality means **the actual number of rows**. The ER cardinality ratio in Chapter 02 constrains **the permitted number of associated entities**. Keep the meanings separate.

### The database as a whole

Slide 32 defines a relational database schema as **a collection of relation schemas together with integrity constraints**. Listing the columns of Student, Course, and Enrolment alone does not fully describe the database schema; primary keys, foreign keys, and other rules also matter.

A database state contains instances of its relations. It is valid only when all relevant constraints hold. Invalid states discussed below explain why operations should be rejected; they are not states the system is expected to preserve.

## 3. Basic properties of a relation

Source: slides 8–10. The SQL comparison additionally uses SQLpart1, slides 31–32.

| Property | Interpretation |
|---|---|
| Tuples are unordered | Swapping displayed rows does not produce a different relation |
| Complete tuples do not repeat | A classical relation is a set; identical tuples are not separate elements |
| Each attribute position contains one atomic value | The course's flat relational model does not directly retain composite or multivalued ER attributes |
| Attributes are distinguished by names | Attribute names must distinguish columns within one relation; different relations may reuse names |
| Rearranging displayed columns preserves meaning | Move each column's name and its values together; do not arbitrarily exchange values within a tuple |

### No semantic column order does not mean arbitrary value order

Slide 10 rearranges PLAYER's column headings together with their corresponding values, preserving the relation. With named attributes, what matters is which value belongs to which attribute.

However, under `Student(sid, name)`, `(S01, Amy)` differs from `(Amy, S01)`. Positional tuple notation must follow the declared attribute order. Rearranging the display is different from exchanging attribute values.

### Atomic values and ER attributes

In Chapter 02, `address(city, street, postcode)` is composite and `{phoneNumber}` is multivalued. Slide 8 excludes these structures as direct attributes in the course's flat relations. Atomicity depends on the domains and operations adopted by the model; it does not mean that a string cannot be divided into characters. Chapter 04 covers the conversion.

### Classical relations and SQL tables

Classical relations use set semantics. SQLpart1, slides 31–32, separately explains that SQL can retain duplicates and that DISTINCT removes duplicate query results. “Relations have no duplicate tuples” therefore does not mean that every SQL table automatically forbids duplicates. SQL syntax and explicit constraint declarations belong to Chapter 06.

## 4. Superkeys, candidate keys, and primary keys

Source: slides 12–15; continues Section 4 of Chapter 02.

| Key | Condition | Original example: sid and email are each unique and mandatory |
|---|---|---|
| Superkey | Uniquely determines a tuple | `{sid}`, `{email}`, `{sid, name}` |
| Candidate key | A superkey containing no redundant attribute | `{sid}`, `{email}` |
| Primary key | The selected candidate key | Choose `{sid}` |
| Composite key | Consists of several attributes | Course's `{dept, courseNo}` in Section 8 |

Minimality asks **whether removing an attribute destroys guaranteed uniqueness**. It does not mean selecting the smallest key among all candidate keys. A relation can have several candidate keys; choosing a primary key does not remove the uniqueness requirements of the others.

Slide 13 explicitly **assumes that no two people share a name** before treating PLAYER.Name as a candidate key. Three different names in a sample do not establish that names are always unique in reality.

### Why are key constraints needed if tuples cannot repeat?

```text
(S01, Amy, amy@example.test)
(S01, Ada, ada@example.test)
```

These complete tuples differ, so set membership alone does not exclude their coexistence. They share sid, however, and violate a key constraint if sid is the primary key. **No duplicate complete rows** and **uniqueness of a specified key** are different requirements.

### Interpreting `2^n − 1` on slide 15

The slide lists all nonempty attribute subsets. An n-attribute set has `2^n − 1` such subsets, **but not every subset uniquely identifies tuples**. This is not an unconditional formula for the number of superkeys.

**Original counterexample:** R(A,B,C) has only candidate key `{A}`; B, C, and `{B,C}` do not guarantee uniqueness. Its superkeys are `{A}`, `{A,B}`, `{A,C}`, and `{A,B,C}`: four, not seven. All nonempty subsets are superkeys only under additional conditions, such as every individual attribute already being a key.

## 5. Foreign keys: direction, repetition, and composite references

Source: slides 16–19.

A foreign key consists of one or more attributes in the referencing relation whose values reference a key in the referenced relation. This lecture section defines references to **primary keys**. This chapter follows that scope rather than claiming to give the complete rules of every SQL system.

```text
Referencing relation                        Referenced relation
Enrolment.sid                  ─────────→   Student.sid
Enrolment.(dept, courseNo)      ─────────→   Course.(dept, courseNo)
```

Write each reference as **referencing attribute group → key attribute group in the target relation**. Attribute names need not match, but corresponding domains must be compatible. Matching names or simply using strings on both sides does not automatically establish a foreign key.

### Foreign-key values need not be unique

Several enrolment rows can contain the same sid because one student may take several courses. Student.sid must be unique, but Enrolment.sid need not be unique merely because it is a foreign key. An attribute can also belong to both a foreign key and a primary key.

### A composite foreign key must match as a combination

If Course contains only `(CS,101)` and `(Math,201)`, `(CS,201)` **does not** reference either tuple. CS and 201 occur separately, but not together in the corresponding key positions of **one target tuple**.

Likewise, `(Department, Degree)` on slide 19 is **one composite foreign key**, not two independent foreign keys referencing COURSE. Omitting either component may fail to identify the course.

## 6. NULL and the limits of foreign-key rules

Source: slides 18, 20, 22, and 30. Chapter 02 explains NULL as unknown or inapplicable information.

| Location | Rule used in this chapter |
|---|---|
| Any component of a primary key | Cannot be NULL, even when other components have values |
| Non-primary-key attribute | Nullability depends on its mandatory-value constraints |
| Nullable foreign key | Can use NULL for no reference only when other constraints permit it |
| Foreign-key attribute also in a primary key | The foreign-key role does not override primary-key non-nullability |

**Slides 18 and 22 require a composite foreign key to be either entirely NULL or entirely non-NULL and matching a referenced key.** This chapter follows that explicit lecture rule. It does not claim that this is the default behaviour of every SQL implementation.

**Original small example:** `Plan(planID, dept, courseNo)` has primary key planID and a nullable foreign key `(dept,courseNo)` referencing Course from Section 5, using the rule above.

| Foreign-key value | Decision |
|---|---|
| `(CS,101)` | Valid: a complete match exists |
| `(NULL,NULL)` | Valid assuming both columns permit missing values and no other rule requires a reference |
| `(CS,NULL)` | Invalid under the lecture's all-NULL-or-all-non-NULL rule |
| `(CS,201)` | Invalid: this combination does not exist |

**Permission for a null reference does not establish that the business permits no association.** If every record must reference a target, the foreign key must additionally be non-NULL. Merely having a nullable foreign key does not fully encode total participation from Chapter 02.

## 7. What do the three integrity constraints check?

Source: slides 20–22 and 32.

| Constraint | Problem prevented | Typical violation |
|---|---|---|
| Key constraint | Distinct tuples share a candidate-key value | Two students have the same sid, or different sid values but the same unique email |
| Entity integrity | A primary key cannot completely identify a tuple | One component of a composite primary key is NULL |
| Referential integrity | A foreign key references a nonexistent target key | An enrolment references a student absent from the database |

Primary-key **uniqueness** belongs to key constraints; primary-key **non-nullability** belongs to entity integrity. They jointly support identification, but distinguish them in answers. One operation may violate several rules; finding one violation does not establish that no others exist.

### Domain and business constraints [explanatory supplement]

Domains on slides 6 and 8 restrict allowed values. For example, grade must be an allowed grade or permitted missing value; an integer identifier cannot arbitrarily contain free text. Other business rules may require nonnegative fees or a start date no later than the end date.

The three constraints emphasized on slide 20 are **not an exhaustive list of every possible database constraint**. Valid primary and foreign keys alone do not guarantee a correct business state.

## 8. Running example: schema, constraints, and initial state

Everything in this section is an original teaching example. The schemas are given inputs; this is not an ER-mapping demonstration.

### Schema and constraints

| Relation schema | Primary key (PK) | Other candidate keys | Foreign keys (FK) |
|---|---|---|---|
| Student(sid, name, email) | `{sid}` | `{email}` | None |
| Course(dept, courseNo, title) | `{dept, courseNo}` | No others specified here | None |
| Enrolment(sid, dept, courseNo, term, grade) | `{sid, dept, courseNo, term}` | No others specified here | `{sid} → Student.sid`; `{dept,courseNo} → Course.(dept,courseNo)` |

The example requires all three Student attributes and all three Course attributes. sid, email, dept, title, name, and term are strings; courseNo is a positive integer. Allowed term values are `2026F` and `2027S`. grade permits A, B, C, D, F, or NULL, with NULL meaning that a grade is not yet available. Every primary-key component is non-NULL.

A student may take several courses and may repeat a course in another term. **At most one enrolment exists per student, course, and term.** This is the rule represented by Enrolment's four-attribute primary key. Neither dept nor courseNo alone identifies Course tuples.

### Initial state

Student:

| sid | name | email |
|---|---|---|
| S01 | Amy | amy@example.test |
| S02 | Ben | ben@example.test |

Course:

| dept | courseNo | title |
|---|---|---|
| CS | 101 | Database Basics |
| Math | 201 | Linear Algebra |

Enrolment:

| sid | dept | courseNo | term | grade |
|---|---|---|---|---|
| S01 | CS | 101 | 2026F | A |
| S02 | CS | 101 | 2026F | NULL |

This state satisfies the stated constraints: both Student candidate keys are unique, primary keys are complete and non-NULL, and every foreign-key value has a target. Repetition of Enrolment.sid does not determine referential validity; the issue is whether it references an existing student.

**Each operation below is assessed independently against this initial state, not executed in sequence.** The decisions are static deductions from the constraints, not results of database execution.

## 9. Insertion: check the new tuple and reference targets

Source: slides 21–28. Operations below use the original data from Section 8.

| Proposed operation | Decision and reason |
|---|---|
| Insert `(S01, Ada, ada@example.test)` into Student | Invalid: sid already exists; key constraint violation |
| Insert `(S03, Chen, amy@example.test)` into Student | Invalid: candidate key email repeats; checking only the primary key is insufficient |
| Insert `(S03, CS, 101, 2026F, A)` into Enrolment | Invalid: Student has no S03; referential integrity violation |
| Insert `(S01, CS, 201, 2026F, B)` into Enrolment | Invalid: Course has no `(CS,201)`; components cannot be matched separately |
| Insert `(S01, CS, 101, NULL, B)` into Enrolment | Invalid: primary-key component term is NULL; entity integrity violation |
| Insert `(S01, CS, 101, 2026F, B)` into Enrolment | Invalid: the four-attribute primary key already exists, even though grade differs |
| Insert `(S01, CS, 101, 2027S, NULL)` into Enrolment | Valid: a different term gives a different key, both foreign keys have targets, and grade permits NULL |

A useful order is **domains and mandatory values → all candidate keys → primary-key non-nullability → each foreign-key group**. If asked for all violations, complete all relevant checks.

In the lecturer's examples, slide 24 inserts the existing Person#=2 into RESEARCHER to demonstrate a key conflict. Slide 26 inserts `(Comp.Sci., NULL)` into COURSE to demonstrate a missing composite-primary-key component. Slide 28 inserts an ENROLMENT with nonexistent Supervisee=6 to demonstrate a missing reference target.

## 10. Deletion: follow references in the reverse direction

Source: slides 29–30.

When deleting, check not only the tuple itself, but also **whether other tuples reference its key**.

| Proposed deletion from the initial state | Effect of deleting without further action |
|---|---|
| Student S01 | An Enrolment references S01; leaving that reference unchanged violates referential integrity |
| Course `(CS,101)` | Two Enrolment tuples reference it; leaving them unchanged violates referential integrity |
| Course `(Math,201)` | No tuple references it here; the remaining state satisfies the stated constraints |
| S01's Enrolment tuple | No other relation references Enrolment here; the remaining state satisfies the stated constraints |

“Primary keys cannot be deleted” is therefore incorrect. Check dependencies and declared handling rules.

Slide 30 discusses these responses:

- **Reject deletion:** retain the referenced tuple and avoid dangling references.
- **Cascade to referencing tuples:** delete related tuples, checking whether further relations reference them.
- **Set the reference to NULL:** possible only when the foreign key is nullable and other constraints permit it.
- **Change to another valid reference:** the replacement must satisfy domains and all relevant constraints; an arbitrary placeholder identifier is insufficient.

In this example, both foreign-key groups in Enrolment are included in its primary key, so **setting them to NULL is not an available repair**. Cascading or changing a reference must also respect business meaning. Do not assume that the database automatically chooses a response.

## 11. Modification: consider both old and new values

Source: slide 31. The final paragraph clarifies the scope of its statements.

| Modified attributes | Checks needed | Example |
|---|---|---|
| Primary or other candidate key | New duplicates, NULL in the primary key, and references to the old key | Changing Student S01's sid to S02 creates a key conflict; changing it to S03 instead leaves the old S01 reference without a target unless references are handled |
| Foreign key | Complete target match, permitted nullability, and any simultaneous primary-key role | Changing courseNo from 101 to 201 in S01's enrolment creates nonexistent `(CS,201)` |
| Non-key attribute | Domains, mandatory values, and other business constraints still apply | Changing grade to Z violates the allowed-grade rule despite changing no key |

Changing S01's enrolment `(dept,courseNo)` together to `(Math,201)` has an existing target and creates no duplicate result key. It is valid under the example's constraints. **Check the entire resulting combination when modifying a composite foreign key.**

The lecture compares changing a primary key to deleting the old key and inserting a new one. This helps remember old references and new conflicts; it does not require physically deleting and reinserting the student.

**Clarifying the slides:** “Not unless you're modifying the value of a key” and “all relational integrity constraints are to do with the key values” on slide 31 should be read in the context of that slide's key-related constraints. They do not establish that every non-key update is safe: domains, mandatory attributes, and business rules may also be violated.

## 12. Common distinctions

| Pair | Distinction |
|---|---|
| Relation / ER relationship | Set of tuples / association among entities |
| Schema / instance | Structure and rules / contents at a particular time |
| Degree / cardinality | Attribute count / current tuple count |
| Relation cardinality / ER cardinality ratio | Actual row count / business limits on associations |
| No duplicate tuples / key uniqueness | No complete-row repetition / no repeated specified key group across distinct rows |
| Candidate key / primary key | Any minimal superkey / the selected candidate key |
| Primary key / foreign key | Identifies this relation's tuples / references a target key; attributes may serve both roles |
| Repeated foreign-key value / dangling reference | Several tuples referencing the same target is usually permitted / referencing a missing target is invalid |
| Composite-key matching / separate column checks | Match the combination in one target tuple / separate occurrences do not establish validity |
| Key constraint / entity integrity | Uniqueness / primary-key non-nullability |
| NULL / zero / empty string | Missing-value marker / a numeric value / a string value |
| Constraint-valid state / fully correct business state | Obeys declared rules / also depends on whether all necessary business rules have been declared |

## 13. Revision checklist and short-answer language

These are learning goals, not a formal practice test or an official mark allocation.

- [ ] Identify relations, tuples, attributes, domains, schemas, and instances in given tables.
- [ ] State degree and cardinality, including for an empty instance.
- [ ] Explain the difference between rearranging displayed columns and exchanging tuple values.
- [ ] Distinguish no duplicate rows, superkeys, candidate keys, and primary keys.
- [ ] Explain why `2^n − 1` is not an unconditional superkey-count formula.
- [ ] Label the direction of every foreign key and check composite references as combinations.
- [ ] Explain key constraints, entity integrity, and referential integrity separately.
- [ ] Apply the lecture's rules to all-NULL, partly NULL, and nonmatching foreign keys.
- [ ] Assess insertions, deletions, and modifications independently from one initial state, identifying conflicting tuples or missing targets.
- [ ] State the conditions for cascading and setting references to NULL without assuming automatic actions.

Useful short-answer formulations:

> A relation is a set of tuples defined over a collection of named attributes.

> A relation schema describes the structure; a relation instance contains the tuples at a particular time.

> A candidate key is a minimal superkey, and a primary key is a selected candidate key.

> Entity integrity requires every component of a primary key to be non-NULL.

> Referential integrity requires a non-NULL foreign-key value to match a referenced key value.

> A composite foreign key must match the corresponding key components in the same referenced tuple.

> Deleting a referenced tuple requires checking the tuples that refer to it.

## Sources and preparation record

- Main lecture deck: [Lecture2A.pptx](../../slides/Lecture2A.pptx), mainly slides 4–32. Text was read and original diagrams/tables on slides 7, 10, 15, 17, 19, 24, 26, 28–29, and 31 were visually inspected, including key underlines, composite references, and operation examples. Mapping steps on slides 33–55 are not developed here.
- Additional comparison: [SQLpart1.pptx](../../slides/SQLpart1.pptx), slides 31–32, only to distinguish classical set semantics from SQL duplicates; SQL querying is not taught here.
- Scope: [CSC5041_Teaching_Plan.pdf](../../syllabus/CSC5041_Teaching_Plan.pdf), page 1, Week 3. Explanations of degree/cardinality, domain and business constraints, original schemas/data, and limitations of slide wording are distinguished from the original material.
- Prepared by Codex in the main conversation. Bilingual structure, relative links, and source numbering were self-checked; the independent Reviewer's conclusion is reported in this turn's delivery message. No database operations were executed: operation decisions are static deductions under explicit constraints. Code/experimental verification is N/A. No submission directory was created; lecturer originals and Chapters 01–02 were unchanged.
- Input SHA-256: Lecture2A `cecf28254342cf35e9a0b1b86a007fba728ed17a900e9e05182f2f2616081ee0`; SQLpart1 `aa28c989fb3674e780418c78c483bba20ff5a50b7da067b0341e60410a68c8ed`; syllabus teaching plan `31380a7fe6504e46541b6db0bb2f24859c69188bfeb9681dca73354ebeb68295`.
- Next: prepare Chapter 04 on ER-to-relational mapping when requested. After all notes are complete, prepare two English practice papers based on the two tutorials.
