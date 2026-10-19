# 01 Database Fundamentals: English Study Notes

CSC5041 · In-class Test 1 revision · 19 October 2026

## Scope and learning goals

This chapter covers database fundamentals. ER diagram construction, relational algebra, and SQL query techniques will be covered separately. The main source is slides 17–57 of the lecturer's introductory deck; slide numbers refer to their order in the PPTX. Sections 7 and 8 supplement topics explicitly named in Week 1 of the teaching plan but not fully developed in this deck. They are not quotations from the lecturer's slides. Examples illustrate concepts; they are neither actual examination questions nor measured results.

After studying this chapter, you should be able to distinguish data, a database, a DBMS, and a database system; explain limitations of file-based processing; distinguish a schema from an instance; explain design stages, schema levels, and data independence; and identify the functions of the main DBMS components.

## 1. Four foundational concepts

Source: slides 17–18, 33, 41, and 45.

| Term | Meaning | Course-enrolment example |
|---|---|---|
| Data | Recorded facts with implicit meaning | Student ID S01, the name Amy, course CSC5041 |
| Database | A collection of related data modelling part of the real world | Student, course, and enrolment records |
| Database management system (DBMS) | Software for creating, maintaining, querying, and managing databases | PostgreSQL database management software |
| Database system | In the slides' simplified definition, the database together with its DBMS | Enrolment data and the DBMS managing it |

**The database contains the data; the DBMS manages the data.** SQL is a language for interacting with relational databases, rather than a database or a DBMS. An application uses the DBMS to access data: a course-registration website is an application, not the DBMS itself.

Related data describes a meaningful application domain. It does not require every record to be directly linked to every other record.

### Structured and unstructured data

Source: slide 34.

- **Structured data** follows a predefined organization, such as a student record with ID, name, and major.
- **Unstructured data** is not organized into a fixed record schema, such as free text, recordings, or images. Analysis commonly requires additional preparation.

Unstructured does not mean meaningless or completely without internal structure. Storing something in a computer file does not make it a relational table.

## 2. Why not manage everything with files?

Source: slides 35–40.

The lecture uses three files for course enrolment:

```text
STUDENT(name, id, major)
COURSE(code, name, department)
SELECTION(student_id, course_code, term)
```

To check whether Amy takes a course, an application first finds her ID in the student file, then matches that ID, the course code, and the term in the selection file. Files can store the information. The difficulty is repeatedly implementing access, integrity, concurrency, and recovery logic in individual applications.

| Limitation | Meaning | Illustrative example |
|---|---|---|
| Data redundancy | The same fact is stored repeatedly | Several departments store separate copies of a student's address |
| Data inconsistency | Copies of the same fact disagree | An address is updated in only one file |
| Difficult data access | New requests require new processing logic | Each reporting requirement needs another file-processing program |
| Data isolation | Data is scattered across files and formats | Student and course information use incompatible formats |
| Integrity problems | Rules are buried in separate application programs | One program checks nonnegative balances; another omits the check |
| Difficult atomic updates | A multi-step operation may finish only partly | Money is deducted before a crash prevents the corresponding credit |
| Concurrent-access problems | Overlapping operations interfere | Two withdrawals read the same old balance and overwrite each other's result |

**Redundancy can cause inconsistency, but duplicate copies need not disagree at every moment.** The slides emphasize avoiding unnecessary redundancy. Deliberate, controlled replication is different from unmanaged duplication.

Here, **data isolation means separation across files and formats**. Do not confuse this use of the term with transaction isolation in later lectures.

### Two examples you should be able to explain

**A transfer and atomicity:** transferring 100 from A to B requires both a debit and a credit. Either both changes take effect, or a failed operation undoes any partial changes. A debit without the credit is not an acceptable completed transfer.

**Concurrent withdrawals and a lost update (supplementary terminology):** start with a balance of 100. Two operations both read 100, each withdraws 50, and both write 50. If both withdrawals are accepted, the correct final balance is 0, but the stored result is 50. Interleaving operations and overwriting an old value cause the problem; a separate balance check alone is insufficient.

For this chapter, understand the problems. Detailed concurrency-control and recovery algorithms belong to later lectures.

## 3. What does a DBMS provide?

Source: slides 41–42, 44, and 47–48.

A DBMS supports defining structures, constructing and loading a database, querying data, inserting/deleting/updating data, and administering access.

| Capability | Purpose |
|---|---|
| Data independence | Reduce application dependence on lower-level representations and storage |
| Efficient data access | Provide shared query and update mechanisms rather than requiring custom file scans in every application |
| Integrity | Maintain valid data states using declared constraints |
| Security | Control who can read or change particular data |
| Administration | Manage structures, permissions, and operation centrally |
| Concurrency and recovery | Coordinate shared access and recover to a consistent state after failures |
| Reduced development effort | Let applications reuse common data-management services |

**Integrity and security are different.** Preventing an invalid enrolment record concerns integrity. Preventing a student from changing another student's grades concerns security. The DBMS supplies mechanisms, but the relevant rules must still be designed and configured correctly.

The slides also list timely response, modifiability, robustness, multiple-user support, and security as expectations. These are system goals, not automatic guarantees of performance or correctness merely from adopting a DBMS.

## 4. Data models, metadata, schemas, and instances

Source: slides 50 and 53; metadata explanation also draws on the diagram on slide 56.

### Data model

A data model provides concepts and rules for describing database structure. It tells us what kinds of structures can represent data, rather than which records exist at a particular moment.

| Level | Focus | Example |
|---|---|---|
| High-level or conceptual model | Application entities, attributes, and relationships | ER model |
| Implementation or record-based model | Structures suitable for logical database implementation | Relational, hierarchical, and network models |
| Low-level or physical model | Record formats, storage organization, and access paths | How records are arranged and located |

The relational model is a type of model. A particular definition of the columns in Student is a schema using that model. The students currently stored are part of an instance.

### Schema versus instance / state

```text
Schema: Student(sid, name, major)

Instance at t1:
(S01, Amy, CS)
(S02, Ben, Math)

Instance at t2:
(S01, Amy, CS)
(S02, Ben, Math)
(S03, Chen, CS)
```

- Inserting the third student changes the **instance**, not the schema.
- Changing Amy's major to Math changes the **instance**, not the schema.
- Adding an email attribute changes the **schema**.
- A defined table with no records still has a schema and an empty instance.

**Metadata is data describing data**, such as table names, column names, types, and constraints. The system catalog or data dictionary stores such descriptions for the DBMS. Amy's name is application data, not metadata.

## 5. Three stages of database design

Source: slide 54.

| Stage | Main question | Enrolment example |
|---|---|---|
| Conceptual design | What objects and business rules must the application represent? | Students, courses, and enrolment relationships |
| Logical design | How are they represented using the target data model? | Student, Course, and Selection relations and constraints |
| Physical design | How will data actually be stored and accessed efficiently? | File organization, indexes, and storage arrangements |

Do not begin with disk formats before understanding the requirements. Conceptual design does not mean entering individual records.

**These design stages and the three-schema architecture in Section 7 are related, but they are different classifications.** Design stages describe a development process; schema levels describe abstraction and interfaces. Do not list the design stages as the names of the three schemas.

## 6. Database languages and users

Source: slides 49 and 55.

### DDL and DML

| Category | Purpose | Recognition examples; syntax comes later |
|---|---|---|
| Data Definition Language (DDL) | Define or modify structures and constraints | CREATE TABLE, ALTER TABLE, DROP TABLE |
| Data Manipulation Language (DML) | Retrieve, insert, delete, and modify data | SELECT, INSERT, DELETE, UPDATE |

The introductory slides use DML broadly to include retrieval. Some other materials call SELECT a separate Data Query Language (DQL); that does not invalidate the classification used here.

**Declarative / non-procedural:** specify the desired result and let the DBMS determine how to obtain it. For example, request the names of CS students.

**Procedural:** specify a sequence of operations, such as reading each student record, checking its major, and outputting the name. SQL queries are generally declarative; later PL/pgSQL material adds variables, branches, and loops.

### Who uses a database?

| Role | Responsibilities |
|---|---|
| Database administrator (DBA) | Schemas, security and authorization, availability, recovery, and performance tuning |
| Application programmer | Programs that access the database to meet application requirements |
| End user | Queries or applications used to complete business tasks |

These are distinct responsibilities, although one person may perform several roles in an organization.

## 7. Three-schema architecture [supplement]

Scope basis: Week 1 on page 1 of the teaching plan. Definitions below supplement the slides rather than reproduce their wording.

| Schema | What it describes |
|---|---|
| External schema | The view presented to a particular user group or application; several may exist |
| Conceptual schema | The database's overall logical structure, including data and constraints |
| Internal schema | Physical storage organization and access methods |

Mappings connect the levels. An external schema can hide information or present computed information. Different views do not require separate database copies.

Definitions: [UCT database course, Chapter 1, “ANSI/SPARC three-level architecture”](https://www.cs.uct.ac.za/mit_notes/database/htmls/chp01.html).

**Original illustration:** a registrar sees full enrolment details; a student sees only their own enrolment list. These are external views. Student, Course, Selection, and their constraints form the overall logical structure. File organization and access paths belong to the internal level.

This architecture is different from the presentation/business/database tiers of application deployment.

## 8. Data independence [supplement]

Scope basis: page 1 of the teaching plan and slide 42.

| Type | What may change? | What should remain unaffected? |
|---|---|---|
| Physical data independence | Internal schema | Conceptual schema and higher-level application interfaces |
| Logical data independence | Conceptual schema | External schemas and the applications using them |

Mappings may need adjustment. Data independence does not promise automatic compatibility with every possible structural change.

Definitions: [Emory course material on the three schemas](https://www.cs.emory.edu/~cheung/Courses/377/Syllabus/1-files/3-schemas.html). For physical/logical separation, also see [Oracle Database Concepts](https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/introduction-to-oracle-database.html).

### Classifying a change

**Example A (original):** reorganize the underlying files while preserving Student's logical definition and the application's queries. This demonstrates physical data independence.

**Example B (original):** split the student structure into basic information and contact information, then adjust a view mapping so an existing application retains its former student-information interface. This demonstrates logical data independence, provided the information required by the old interface remains derivable. Arbitrary table splitting is not automatically harmless.

**Example C (original):** changing Amy's phone number changes a data value. It is not an example of logical data independence.

Use the order **user views → overall logical structure → physical storage**. Identify the level that changes, then explain which higher-level interface is protected.

## 9. Understanding the DBMS component diagram

Source: slide 56; the original diagram was visually inspected. The explanation below is functional, not a guaranteed execution sequence for every product.

| Component | Basic function |
|---|---|
| DDL compiler | Process structural definitions and provide their descriptions to the catalog |
| System catalog / data dictionary | Store metadata about database structures |
| Query compiler | Process a query into a representation suitable for subsequent execution |
| Query optimizer | Choose a suitable query execution plan |
| Runtime database processor | Handle database requests during execution |
| Stored data manager | Manage low-level data access and I/O |
| Concurrency-control / backup / recovery subsystems | Coordinate concurrent operations and support backup and recovery |

For an interactive query, use this simplified flow:

```text
User query → query compilation → optimization → runtime processing → data access → result
                                                    ↕
                                      catalog supplies metadata
```

The original figure also includes application precompilation, DML compilation, and host-language compilation. Recognize these as additional entry paths; compiler implementation details are outside this chapter.

**Keep the viewpoints separate:** schema architecture explains levels of data description; the component diagram explains which software modules handle requests.

## 10. Database types: recognize categories, not live rankings

Source: slides 20 and 51–52.

Relational databases mainly organize data as relations/tables. The slides also introduce key-value, document, graph, and column-family models. Examples in the deck include PostgreSQL and MySQL for relational systems, Redis for key-value storage, MongoDB for documents, and Cassandra for column-family storage. These examples identify models; they are not current market rankings or exhaustive descriptions of product capabilities.

NoSQL does not mean “no structure.” A relational database is more than a collection of unrelated spreadsheets. The rest of this revision series primarily concerns relational databases.

## 11. Common distinctions

| Pair | Distinction |
|---|---|
| Database / DBMS | Related data / software managing it |
| Schema / instance | Structural description / actual contents at a particular time |
| Data model / schema | Concepts for describing structures / a particular structure defined using them |
| Metadata / data | Descriptions of structures and related information / application facts |
| Redundancy / inconsistency | Repeated storage / conflicting copies |
| Integrity / security | Whether data obeys rules / who may access or modify it |
| DDL / DML | Define structures / retrieve and change contents |
| Design stages / schema levels | Development process / levels of data abstraction |
| Physical / logical independence | Shield higher levels from storage changes / shield external interfaces from overall logical changes |
| Atomicity / concurrency | Whether one unit of work takes effect completely / how overlapping operations share data |

## 12. Revision checklist and short-answer language

These are learning goals, not a formal practice test or an official mark allocation.

- [ ] Explain the four foundational concepts with an example of each.
- [ ] Explain at least four file-based limitations using cause and consequence.
- [ ] Distinguish the problems illustrated by a failed transfer and overlapping withdrawals.
- [ ] Classify record insertion, value updates, and adding a column as instance or schema changes.
- [ ] Distinguish data models, design stages, and schema levels.
- [ ] Identify the level affected by a change and explain the relevant form of independence.
- [ ] Explain DDL, DML, the DBA's role, and the functions of core DBMS components.

Useful short-answer formulations:

> A database is a collection of related data, whereas a DBMS is the software used to create and manage it.

> A schema describes the database structure; an instance contains the actual data at a particular time.

> Physical data independence allows storage changes without changing the conceptual schema.

> Logical data independence allows conceptual-schema changes while preserving existing external interfaces through suitable mappings.

> Atomicity means that a transaction's changes take effect as a whole or do not take effect at all.

## Sources and preparation record

- Lecturer's introductory deck: [Week 1A - IntroductionNEW.pptx](../../slides/Week%201A%20-%20IntroductionNEW.pptx), mainly slides 17–57; component diagram on slide 56.
- Lecturer's plan: [CSC5041_Teaching_Plan.pdf](../../slides/CSC5041_Teaching_Plan.pdf), page 1, Week 1 and Test 1.
- Supplementary web references support the architecture and independence definitions in Sections 7–8. Original examples are labelled. External references do not determine the lecturer's intended examination depth.
- Prepared by Codex in this conversation. Source numbering and bilingual alignment were self-checked; no independent Reviewer review was performed. Source files were unchanged. These are personal study notes, not an assignment submission or official question bank.
- Input versions: introductory deck SHA-256 `d36c2d15a77083931046168738d794558c2e9821d452701f64ef524e45e87a7c`; teaching plan SHA-256 `b62c7356961bf10585f2e7d5fbf29bcb8401970a99d09d80fe6675fa63cea463`.
- Next: continue with the next notes chapter when requested. After all notes are complete, prepare one English practice test based on Tutorial 1 and another based on Tutorial 2. No tests have been generated yet.
