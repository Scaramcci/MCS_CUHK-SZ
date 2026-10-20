# 04 ER-to-Relational Mapping: English Study Notes

CSC5041 · In-class Test 1 revision · 19 October 2026

## Scope and learning goals

This chapter connects [02 ER Modelling](02_er_modelling_en.md) with [03 Relational Model and Integrity Constraints](03_relational_model_and_integrity_en.md): translate ER meaning into relation schemas, then check which constraints are preserved and which require additional expression.

The main source is the lecturer's [Lecture2A.pptx](../../slides/Lecture2A.pptx), slides 33–56, covering “ER-to-relational mapping” in Week 3 on page 1 of the teaching plan. Unless another file is named, slide numbers refer to their order in that deck. Tutorial 1, page 1, Question 1(c)–(d), asks for relational schemas, explanations of which relationships become separate relations, and constraints not enforced by keys and foreign keys alone.

After studying this chapter, you should be able to apply the seven mapping steps and identify primary keys, complete foreign-key groups, relationship-attribute placement, uniqueness, and mandatory references. This chapter covers logical schemas and constraints, not SQL querying or normalization algorithms. Examples restate the lecture or are explicitly original; they are not database execution results or a complete tutorial solution.

## 1. Mapping inputs, outputs, and notation

Source: slides 33 and 54–56; constraint meanings continue Chapter 03.

```text
Input: entities, attributes, keys, relationships, cardinalities, participation, written rules
  ↓ ER-to-relational mapping
Output: relation schemas + primary keys + foreign-key groups + uniqueness/nullability + other rules
```

The following notation improves readability; it is **not complete SQL DDL**:

| Notation | Meaning |
|---|---|
| `R(a, b, c)` | Attribute list of relation R |
| `PK{a,b}` | One composite primary key containing a and b, not two primary keys |
| `FK{a,b} → S{x,y}` | One composite foreign key, with a corresponding to x and b to y |
| `UNIQUE{a}` | Non-NULL a values cannot repeat across rows; preserves the relevant uniqueness rule |
| `NOT NULL{a,b}` | Both a and b must have values |

A primary key already requires uniqueness and non-NULL values for every component. Nullable UNIQUE notation here only expresses that existing associations cannot repeat; it does not prescribe how individual SQL products handle NULL. Implementation belongs to Chapter 06.

Tutorial 1(c) requires **underlined primary keys and an asterisk on each foreign-key attribute**. Follow that convention in an actual answer and additionally specify composite-key groups and their targets. Asterisks alone do not identify which columns jointly form one reference.

## 2. Overview of the seven steps

Source: slides 35, 38, 41, 44, 47, 50, and 53–55.

| Lecture step | Input | Basic output | Key / constraint concern |
|---|---|---|---|
| 1 | Strong entity | One relation per strong entity | Retain the selected entity key; flatten composite attributes |
| 2 | Weak entity | Relation including the owner's complete key | Owner key plus partial key |
| 3 | Binary 1:1 relationship | Usually add one side's key to the other | Foreign-key uniqueness; non-nullability for the carrying side's total participation |
| 4 | Binary 1:N relationship | Add the 1-side key to the N-side relation | N-side foreign key; relationship attributes also go there |
| 5 | Binary M:N relationship | New relationship relation | Usually the combination of both complete participant keys |
| 6 | Multivalued attribute | New attribute relation | Owner key plus all simple components of the attribute value |
| 7 | n-ary relationship, n > 2 | New relationship relation | Collect participant keys, then determine a minimal identifier from the semantics |

Establish complete entity identifiers first, then map regular relationships and multivalued attributes. **Not every diamond requires a new relation**, and not every relationship can be represented by one foreign key. Read uniqueness, nullability, and coverage back against the original model.

**Every tuple in a separate relationship relation must have all its participants.** Every participating role's key must be non-NULL. Primary-key membership already guarantees this for included components; explicitly require it for the remaining components. Partial participation is represented by the absence of a relationship row, not by putting a NULL participant into an existing relationship row.

## 3. Step 1: strong entities and ordinary attributes

Source: slides 35–37; derived attributes continue the ER material on slides 22–23 discussed in Chapter 02.

Create a relation R for strong entity E. Include its simple attributes and the simple components of composite attributes. Use E's selected key as R's primary key. Preserve uniqueness of other candidate keys; selecting one primary key does not remove other identification rules.

**Original example:** Student has key sid and unique email; composite address(city,street,postcode), multivalued phone, stored dateOfBirth, and derived age.

```text
Student(sid, name, email, city, street, postcode, dateOfBirth)
PK{sid}; UNIQUE{email}
```

If email is mandatory in the requirements, also specify non-nullability. This step handles ordinary attributes:

- Flatten address into three attributes rather than mechanically storing a redundant address column as well.
- Do not place phone in a set-valued cell or invent phone1 and phone2; handle it in Step 6.
- Following the lecture's ER example, derive age from dateOfBirth and a reference date rather than automatically storing it again. Materialization would be an additional design choice to justify.
- When an entity key is composite, copy all its components when referencing it elsewhere.

## 4. Step 2: weak entities and identifying relationships

Source: slides 38–40.

Create a relation for weak entity W containing its simple attributes and the simple components of composite attributes. Include the owner's complete primary key as a foreign key. Its primary key combines **the owner key and W's partial key**.

```text
Employee(empID, name)                       PK{empID}
Dependent(empID, dependentName, dateOfBirth, kinship)
  PK{empID, dependentName}
  FK{empID} → Employee{empID}
```

This restates the lecture's Dependent example using consistent names. dependentName is unique only within one Employee's dependents, so it cannot be the sole primary key. empID is both a primary-key component and a foreign key; its non-nullability reflects the weak entity's required owner.

The identifying relationship usually needs no separate relation repeating these keys. If it has attributes, they can accompany the reference in the weak entity's relation under this example's exactly-one-owner condition.

### When the owner is itself weak

**Original example:** roomNo identifies a Room within a Building; deskNo identifies a Desk within a Room.

```text
Building(buildingID, name)                 PK{buildingID}
Room(buildingID, roomNo, floor)
  PK{buildingID, roomNo}; FK{buildingID} → Building{buildingID}
Desk(buildingID, roomNo, deskNo)
  PK{buildingID, roomNo, deskNo}
  FK{buildingID,roomNo} → Room{buildingID,roomNo}
```

Desk references Room through a two-attribute foreign key. Copying only roomNo loses the building context. Do not introduce a new global ID merely because the object is weak and then discard the original local-uniqueness requirements.

## 5. Step 3: binary 1:1 relationships

Source: slides 41–43. Explicit uniqueness and coverage checks below supplement the mapping semantics.

Let S and T represent the two entity types. Usually add the complete primary key of one side to the other as a foreign key, together with relationship attributes. The lecture recommends carrying the foreign key on the totally participating side when one exists.

**Original example:** each Department must have exactly one Employee as manager; each Employee manages at most one Department. MANAGES has attribute startDate.

```text
Employee(empID, name)                      PK{empID}
Department(deptID, name, managerID, managerStartDate)
  PK{deptID}
  FK{managerID} → Employee{empID}
  UNIQUE{managerID}; NOT NULL{managerID}
```

| Meaning to preserve | Rule expressing it |
|---|---|
| The manager is an existing Employee | Foreign key |
| Every Department has exactly one manager | Single-valued managerID plus non-nullability and the foreign key |
| Each Employee manages at most one Department | Uniqueness of managerID |
| The starting date describes this management association | Store it in Department alongside the management reference |

**A foreign key without UNIQUE permits several departments to select the same employee, producing N:1 instead of 1:1.** Slide 41 does not list every constraint declaration; that does not justify dropping the 1:1 semantics. Whether a relationship attribute is mandatory is a separate requirement, not an automatic consequence of total participation.

### Both sides partial, or a separate relationship relation

One option is a nullable, unique foreign key on one side. Another is:

```text
Manages(deptID, empID, startDate)
PK{deptID}; UNIQUE{empID}; NOT NULL{empID}
FK{deptID} → Department{deptID}; FK{empID} → Employee{empID}
```

This permits at most one manager per department and at most one managed department per employee. Non-NULL empID ensures that every existing management association has an employee participant. It **does not require every Department to appear in Manages**. A totally participating side needs an additional coverage requirement when this separate-relation representation is used.

The lecture also mentions merging both types where appropriate, especially when both participate totally and have no other relationships. Do not merge mechanically whenever a relationship is 1:1. Check whether identifiers, independent meanings, and other associations remain correctly represented.

## 6. Step 4: binary 1:N relationships

Source: slides 44–46.

Add the **complete key of the 1 side to the N-side relation as a foreign key**. Place relationship attributes on the N side too. The original N-side primary key usually stays unchanged.

**Original example:** Department:Employee = 1:N. Each Employee must work in one Department; WORKS_FOR has attribute joinedOn.

```text
Department(deptID, name)                   PK{deptID}
Employee(empID, name, deptID, joinedOn)
  PK{empID}; FK{deptID} → Department{deptID}
  NOT NULL{deptID}
```

- Employee.deptID can repeat because a department can have several employees. Adding UNIQUE would incorrectly restrict the association to 1:1.
- joinedOn describes the employee's association with that department and accompanies the foreign key in Employee.
- Employee's total participation requires non-NULL deptID. If employees may have no department, allow a null reference and explain how relationship attributes are handled when no association exists.
- If every Department must have an Employee, Employee.deptID being a non-NULL foreign key still does not guarantee that requirement. A Department could remain unreferenced.

**Do not store a list of employee IDs in one Department cell.** The course's flat relational model does not directly store such multivalued sets as attributes.

## 7. Step 5: binary M:N relationships

Source: slides 47–49.

Create a relationship relation containing both complete participant keys as foreign keys, together with relationship attributes. Under ordinary ER semantics of one relationship instance per participant pair, use their combined keys as the primary key.

```text
Employee(empID, name)                     PK{empID}
Project(projectID, title)                 PK{projectID}
WorksOn(empID, projectID, timeFraction)
  PK{empID, projectID}
  FK{empID} → Employee{empID}
  FK{projectID} → Project{projectID}
```

empID alone would allow at most one project per employee; projectID alone would allow at most one employee per project. timeFraction describes a pair's property and normally does not belong in the key. Including it would permit repeated pairs with different fractions.

**Adding one foreign key to each entity relation also cannot represent arbitrary M:N pairings.** A relationship relation uses separate rows for the pairings without imposing a single-valued association on either participant.

### What if the same pair can participate repeatedly?

If repeated borrowings of the same Book by the same Reader must be stored, explicitly model a Loan event and its identification. An original extension is `Loan(loanID, readerID, bookID, startDate, endDate)`, with primary key loanID, `FK{readerID} → Reader{readerID}`, and `FK{bookID} → Book{bookID}`. Require `NOT NULL{readerID,bookID}` so that each loan has both a reader and a book.

A new event identifier needs a requirement-based justification. Do not arbitrarily add every relationship attribute to the key just to allow repeats. Ordinary M:N mapping and repeated-event modelling have different assumptions.

## 8. Step 6: multivalued attributes

Source: slides 50–52.

Create a separate relation containing the owner's complete key as a foreign key and the attribute value's simple components. Under the lecture's set semantics, and without an additional smaller identification rule, **owner key plus attribute value** forms the primary key.

### A multivalued simple attribute

```text
Department(deptID, name)                   PK{deptID}
DepartmentPhone(deptID, phone)
  PK{deptID, phone}; FK{deptID} → Department{deptID}
```

Using only deptID permits at most one phone per department. Using only phone additionally prohibits departments from sharing a number unless that is actually required. A department with no phone has no corresponding DepartmentPhone row, rather than a `(deptID,NULL)` row: phone is part of the primary key here.

### A multivalued composite attribute

**Original example:** a Person can have several Addresses, each consisting of city, street, and postcode.

```text
PersonAddress(personID, city, street, postcode)
PK{personID, city, street, postcode}
FK{personID} → Person{personID}
```

The complete address value distinguishes addresses for the same person. This assumes the identifying components are available in full and no additional smaller identifier is specified. The same address cannot repeat for one person, matching the attribute's set semantics. Incomplete addresses, address IDs, labels, or independent history require explicit additional requirements before changing this design.

**Slide naming clarification:** slide 34 labels the multivalued attribute Phone, whereas slide 52 names the final relation D_number with Dnumber. This chapter consistently uses DepartmentPhone/phone to explain the mapping rather than treating that naming change as a newly required property.

## 9. Step 7: n-ary relationships and key selection

Source: slide 53. The ternary examples below explain the abbreviated key-selection rule; they are not original lecture questions.

Create a relation for an n-ary relationship, collect each participating role's complete entity key as a foreign key, and add relationship attributes. **Selecting a key is not circling every column or simply looking for the entity labelled 1.**

### A ternary relationship without additional uniqueness restrictions

```text
Supply(supplierID, partID, projectID, quantity)
PK{supplierID, partID, projectID}
FK{supplierID} → Supplier{supplierID}
FK{partID} → Part{partID}
FK{projectID} → Project{projectID}
```

Assume at most one supply association per triple and that no pair of participants determines the third. The three participant keys form the primary key; quantity is a relationship attribute.

### Suppose a fixed Supplier and Part have at most one Project

Then `(supplierID,partID)` already determines the supply association. Assuming no smaller unique group, choose `PK{supplierID,partID}`. projectID remains a foreign key but need not be part of the primary key. Explicitly add `NOT NULL{projectID}` so that every ternary association still has a Project participant; removing it from the primary key does not make that role optional within a relationship tuple.

For example, `(S1,P1,J1,10)` and `(S1,P1,J2,20)` have different three-part keys. Using only the full triple as the key would not prevent one Supplier–Part pair from having two Projects. **Preserving the at-most-one rule requires uniqueness of the participant group that determines that project.**

The exception wording on slide 53 does not spell out which roles are fixed before “at most one” is assessed. This chapter does not infer that the key of the side labelled 1 must alone be the primary key. Check minimal identifiers against explicit uniqueness rules and preserve other candidate-key uniqueness where several candidates exist.

Likewise, do not automatically replace a ternary relationship with three binary ones: that can lose information about which three objects participate together. If the requirements are ambiguous, state which association meaning needs confirmation.

## 10. Worked example: the lecture's company model

Source: slides 34–52. The following retains the entities and associations but uses consistent names: SSN → empID, Department.Name → deptName, Pnumber → projectID, and Dependent.Fname → dependentName. Department still uses its name as its key, as in the lecture; **no new deptID is invented**. This is a given assumption of this example, not a claim that all real department names are unique.

### Input meaning

- Strong entities: Employee, Department, and Project. Weak entity Dependent is identified through Employee and dependentName.
- WORKS_FOR: each Employee works in exactly one Department; a Department can have several employees.
- MANAGES: each Department has exactly one manager; an Employee manages at most one Department. The relationship has attribute managerStartDate.
- WORKS_ON: Employee and Project have an M:N relationship with attribute timeFraction.
- Department has multivalued phone; Dependent also has dateOfBirth and kinship.

### Final schemas and keys

| Relation schema | Primary key | Foreign keys |
|---|---|---|
| Employee(empID, firstName, lastName, dateOfBirth, deptName) | `{empID}` | `{deptName} → Department{deptName}` |
| Department(deptName, location, managerID, managerStartDate) | `{deptName}` | `{managerID} → Employee{empID}` |
| Project(projectID, projectName) | `{projectID}` | None |
| Dependent(empID, dependentName, dateOfBirth, kinship) | `{empID,dependentName}` | `{empID} → Employee{empID}` |
| WorksOn(empID, projectID, timeFraction) | `{empID,projectID}` | `{empID} → Employee{empID}`; `{projectID} → Project{projectID}` |
| DepartmentPhone(deptName, phone) | `{deptName,phone}` | `{deptName} → Department{deptName}` |

Also specify `UNIQUE{Department.managerID}`, `NOT NULL{Department.managerID}`, and `NOT NULL{Employee.deptName}`. Every primary key is already non-NULL. Decide nullability of other ordinary attributes from the requirements rather than guessing from their names.

### Where did each ER association go?

| ER structure | Mapping destination | Separate relationship relation? |
|---|---|---|
| Identifying relationship between Employee and Dependent | Dependent.empID and its composite primary key | Usually no |
| MANAGES, 1:1 | Department.managerID and managerStartDate, with uniqueness | No |
| WORKS_FOR, Department:Employee = 1:N | Employee.deptName | No |
| WORKS_ON, M:N | WorksOn | Yes |
| Department's multivalued phone | DepartmentPhone | Yes as an attribute relation, not a newly introduced ER binary relationship |

Mutual references between Employee and Department are not automatically a design error: they represent different associations. They also **do not automatically ensure that a manager works in the department managed**. If that rule is additionally required, express it explicitly as discussed next.

## 11. Constraints to check after mapping

Source: reading back the semantics of slides 41, 44, 47, and 55; application context from Tutorial 1, Question 1(d). Mechanisms below are explanatory supplements, not implemented database features.

| Business rule | Do ordinary primary/foreign keys already suffice? | Additional expression needed |
|---|---|---|
| An Employee manages at most one Department in a 1:1 relationship | No: a managerID foreign key permits repetition | Uniqueness of managerID |
| Every tuple on the carrying side must have a target | A nullable foreign key is insufficient | Foreign-key non-nullability |
| Every Department has at least one Employee | Employee's foreign key remains insufficient even if non-NULL | Global coverage: every department is referenced by an employee |
| Every Project participates in an M:N association | WorksOn's primary key and two foreign keys are insufficient | Every Project occurs in at least one WorksOn tuple |
| A manager works in the department managed | Keys for the two separate associations are insufficient | A cross-association rule requiring management pairs to be employment pairs |
| startDate is no later than endDate | No | A constraint comparing values |

Uniqueness and mandatory values can be expressed through corresponding declarations; date ordering can use a check constraint. Global coverage needs a suitable global check, trigger, or similar mechanism. The current foreign keys cannot be presented as already guaranteeing it.

**One precise expression of the same-department manager rule:** in Section 10, Department's `(managerID,deptName)` must occur in Employee's `(empID,deptName)`. An implementation supporting the corresponding composite-key references can declare that Employee attribute group unique and add this composite foreign key. Alternatively, triggers or similar mechanisms must correctly cover the relevant changes.

Thus “the current single-column foreign keys are insufficient” differs from “no redesigned schema could ever express this through a composite foreign key.” An answer to Tutorial 1(d) should specify its schema and mechanism rather than make unconditional impossibility claims about keys and foreign keys.

## 12. A practical answer-writing procedure

Source: slides 54–56; the sequence below organizes the material into a workflow.

1. **Record input constraints.** List entity keys, weak-entity owners, minima and maxima for every relationship, and extra written rules.
2. **Create entity relations first.** Flatten ordinary attributes of strong entities; give weak entities complete owner keys and partial keys.
3. **Map regular relationships.** Choose a carrying side and uniqueness for 1:1; use the N side for 1:N; create separate M:N and n-ary relations.
4. **Place relationship and multivalued attributes.** Store the former with their associations and the latter in separate relations. Include simple components of composite attributes.
5. **List primary keys and every foreign-key group.** State the target attribute group rather than marking an unexplained “FK.”
6. **Read maxima and minima back.** Did 1:N accidentally become 1:1? Are uniqueness, non-nullability, or total-participation coverage missing?
7. **Try counterexamples.** Can two departments share one manager? Can a department exist without employees? If forbidden by the requirements but permitted by the schema, another constraint is needed.
8. **State mechanisms and assumptions.** Separate schema guarantees from checks still requiring implementation. Follow requested underlining and asterisk conventions.

These are static schema checks, not SQL execution verification. Listing relation names alone does not establish preservation of all ER semantics.

## 13. Common distinctions

| Pair | Distinction |
|---|---|
| Strong-entity key / weak-entity partial key | Complete independent identifier / identification requiring owner context |
| Composite foreign key / several independent foreign keys | One group referencing one target key / independently targeted references |
| Foreign key / uniqueness in 1:1 | Target existence / preventing several source tuples from selecting the same target |
| N-side foreign key / list of IDs on the 1 side | One reference per tuple / incorrectly storing a multivalued set in one attribute |
| Non-NULL foreign key / target-side total participation | Every referencing tuple has a target / every target has a referencing tuple |
| Relationship attribute / identifying attribute | Property of an association / an identification role requiring a separate semantic justification |
| M:N relation / multivalued-attribute relation | Participant pairings / multiple attribute values of one owner |
| Complete triple of keys / ternary candidate key | Distinguishes triples / may not be minimal under stronger uniqueness rules |
| Foreign-key arrows / complete constraint preservation | Reference directions / uniqueness, nullability, coverage, and remaining rules must also be checked |

## 14. Revision checklist and short-answer language

These are learning goals, not a formal practice paper or an official mark allocation.

- [ ] State the seven mapping steps and their outputs without consulting the notes.
- [ ] Flatten composite attributes and handle multivalued and derived attributes separately.
- [ ] Write complete primary keys and grouped foreign keys for two levels of weak entities.
- [ ] Explain why a 1:1 foreign key normally also needs uniqueness.
- [ ] Place foreign keys and relationship attributes correctly for 1:N.
- [ ] Select a combined key for an ordinary M:N relation without arbitrarily adding relationship attributes.
- [ ] Map simple and composite multivalued attributes and explain how no value is represented.
- [ ] Determine a minimal identifier from explicit ternary uniqueness rules rather than the location of a 1 label.
- [ ] Read every key, reference, uniqueness rule, and mandatory value back in the worked example.
- [ ] Identify total-participation or cross-association rules not yet guaranteed by the foreign keys and describe suitable mechanisms.

Useful short-answer formulations:

> Map a strong entity type to a relation containing its simple attributes and the simple components of composite attributes.

> The primary key of a weak entity's relation combines the owner's primary key with the weak entity's partial key.

> For a binary 1:N relationship, place the foreign key and relationship attributes in the relation on the N side.

> A foreign key alone does not preserve a 1:1 relationship; uniqueness must also be enforced.

> Map a many-to-many relationship to a separate relation containing the keys of both participants and the relationship attributes.

> A non-NULL foreign key ensures that each referencing tuple has a target, not that every target is referenced.

> For an n-ary relationship, choose the key from the stated uniqueness constraints rather than from the diagram labels alone.

## Sources and preparation record

- Main lecture deck: [Lecture2A.pptx](../../slides/Lecture2A.pptx), slides 33–56. Text was read and original diagrams on slides 34, 37, 40, 43, 46, 49–50, 52–53, and 55 were visually inspected for key underlines, foreign-key arrows, participation lines, and multivalued-attribute naming.
- Scope: [CSC5041_Teaching_Plan.pdf](../../syllabus/CSC5041_Teaching_Plan.pdf), page 1, Week 3, and page 2, Tutorial 1. Supporting requirements: [Tutorial1.pdf](../../slides/Tutorial1.pdf), page 1, Question 1(c)–(d). This chapter supplies neither a complete clinic solution nor a practice paper.
- The Step 1 explanation of derived attributes continues ER slides 22–23 as discussed in [Chapter 02](02_er_modelling_en.md). Original examples, consistent renaming, explicit constraint supplements, and clarifications of abbreviated slide rules are identified where used.
- Prepared by Codex in the main conversation. Bilingual structure, relative links, schemas, and constraint expressions were self-checked; the independent Reviewer's conclusion is reported in this turn's delivery message. No SQL was executed: examples are static schema analyses. Code/experimental verification is N/A. No submission directory was created; lecturer originals and Chapters 01–03 were unchanged.
- Input SHA-256: Lecture2A `cecf28254342cf35e9a0b1b86a007fba728ed17a900e9e05182f2f2616081ee0`; Tutorial 1 `316e8b6bb9581a5ecae3fb2f449e395a4ea8a19b4ee16c4191fc20a6079d2c44`; syllabus teaching plan `31380a7fe6504e46541b6db0bb2f24859c69188bfeb9681dca73354ebeb68295`.
- Next: prepare Chapter 05 on relational algebra when requested. After all notes are complete, prepare two English practice papers based on the two tutorials.
