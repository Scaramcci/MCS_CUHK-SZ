# CSC5041 — Practice Paper 2

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

## Q1. Database fundamentals and keys [10 marks]

**(a) [3 marks]** Account(accountID, email, displayName) has the following rules: accountID and email are each globally unique and mandatory; displayName need not be unique. No other uniqueness rules are given. List all candidate keys, and give one superkey that is not a candidate key.

**(b) [2 marks]** Classify each operation as changing the schema or only the instance:

1. Insert a new Account tuple.
2. Add a dateOfBirth attribute to Account's definition.

**(c) [3 marks]** Name the DBMS component responsible for each task:

1. Storing descriptions of table structures and constraints.
2. Choosing a suitable query execution plan.
3. Managing low-level stored-data access and I/O.

**(d) [2 marks]** A person's address is stored in two independent files. One copy is updated while the other is not. Name the two file-management problems illustrated: the initial duplication, and the disagreement after the update.

## Q2. Conceptual design and relational mapping [30 marks]

A lending archive stores the following information.

A publisher has a unique `publisherID`, a name, and an address consisting of city and street. A publisher publishes one or more books, and each book has exactly one publisher. A book has a unique `ISBN` and a title.

Each book has one or more editions. Editions are numbered `1,2,3,...` within their book; the same `editionNo` may occur for different books. An edition has a publication date and a price. Each edition has one or more physical copies. Copies are numbered `1,2,3,...` within their edition; the same `copyNo` may occur in different editions. A copy records its acquisition date.

An author has a unique `authorID` and a name. An author may write zero or more books, and every book has one or more authors. Record a `contributionPercent` for each author–book association. It is positive, and the percentages for all authors of one book must sum to 100. There is at most one association per author–book pair.

A reader has a unique `readerID`, a name, and zero or more phone numbers. A loan has a unique `loanID`, a checkout date, a due date, and a return date that is NULL while the loan is open. Each loan concerns exactly one reader and exactly one physical copy. Readers and copies may participate in zero or more loans over time. The same reader may borrow the same copy repeatedly, with a different loanID each time. At most one open loan is allowed for a physical copy at any moment.

**(a) [5 marks]** List entity types and attributes. Identify keys; for each weak entity give its partial key, owner, and full identifier.

**(b) [9 marks]** Draw the ER diagram, including attributes, relationship attributes, cardinality ratios, participation constraints, and identifying relationships. State any additional assumptions.

**(c) [12 marks]** Produce the relational schema using the standard mapping. Show all primary keys, complete foreign-key groups, and non-null requirements needed for the associations. State which relationships or attributes create separate relations. Preserve repeated loan events.

**(d) [4 marks]** Express two stated business constraints not guaranteed by the primary-key and foreign-key declarations in your mapping alone. For each, name a suitable additional enforcement mechanism.

## Q3. Relational integrity [10 marks]

Use this independent schema:

```text
Desk(buildingID, deskNo, zone)
  PK{buildingID,deskNo}; all attributes NOT NULL

Reservation(resID, buildingID, deskNo, duration)
  PK{resID}
  FK{buildingID,deskNo} → Desk{buildingID,deskNo}
  resID and duration are NOT NULL; CHECK(duration > 0)
```

For this question, the composite foreign key must be either **entirely NULL**, or **entirely non-NULL and matching one Desk key**. This is the lecture convention explicitly adopted for this question, not a claim about every SQL implementation's default.

Initial state:

| Desk.buildingID | deskNo | zone |
|---|---|---|
| B1 | D1 | Quiet |
| B2 | D2 | Group |

| Reservation.resID | buildingID | deskNo | duration |
|---|---|---|---|
| R1 | B1 | D1 | 2 |
| R2 | NULL | NULL | 3 |

Assess each operation **independently from this initial state**. No automatic cascades or reference repairs are configured. State **valid/invalid** and the applicable constraint or reason. **[2 marks each]**

1. Insert `(R3,B1,D2,1)` into Reservation.
2. Insert `(R3,B1,NULL,1)` into Reservation.
3. Change the duration of Reservation R1 to 0.
4. Delete `(B2,D2,'Group')` from Desk.
5. Insert `(B3,NULL,'Quiet')` into Desk.

## Schema for Q4 and Q5

```text
Customer(uid, uname, city, status)         PK{uid}
Vehicle(vid, model, category, dailyRate)   PK{vid}
Rental(uid, vid, startDate, endDate, charge)
  PK{uid,vid,startDate}
Agent(aid, aname, city)                   PK{aid}
Handles(aid, uid, vid, startDate)          PK{aid,uid,vid,startDate}
```

- Rental.uid references Customer.uid; Rental.vid references Vehicle.vid.
- Handles.aid references Agent.aid. Handles.(uid,vid,startDate) references the complete Rental key.
- A Handles tuple links an agent to one particular rental. Several agents may handle the same rental; an agent may handle several rentals.
- startDate and endDate have DATE type. endDate is NULL for an ongoing rental; charge is numeric and NULL until billing. All other attributes are non-NULL.
- A customer may rent the same vehicle repeatedly on different start dates. Customer and agent cities need not agree.
- “Has rented” means a Rental tuple exists, including ongoing or unbilled rentals. Consider all dates unless a subpart specifies otherwise.

## Q4. Relational algebra [25 marks]

**(a) [3 marks]** Return the models of Hybrid vehicles whose dailyRate is less than 80.

**(b) [4 marks]** Return the names of customers who have a rental handled by agent `'A2'`. Match the complete rental identity.

**(c) [5 marks]** Return the names of customers who have rented:

1. At least one Electric vehicle or at least one Hybrid vehicle, using a set union.
2. At least one vehicle from each category, using a set intersection.

**(d) [4 marks]** Return the names of customers who have never rented any vehicle. Use set difference.

**(e) [6 marks]** Return the names of customers who have rented every Electric vehicle in Vehicle. Rentals may be on different dates, and vehicles in other categories are allowed. Assume at least one Electric vehicle exists. Use division, or a correct expression using basic operators.

**(f) [3 marks]** For each category represented in Vehicle, return the category, number of vehicles, and average dailyRate. Use γ.

## Q5. SQL [25 marks]

**(a) [4 marks]** Return vid, model, and dailyRate for vehicles whose dailyRate exceeds the average dailyRate of all vehicles. Use a scalar subquery. Sort by dailyRate descending, then vid ascending.

**(b) [5 marks]** Return distinct customer IDs and names for customers with a rental beginning on `DATE '2026-10-01'` that is handled by agent `'A2'`. Ensure that the agent is linked to that particular rental, not another rental by the same customer or for the same vehicle.

**(c) [5 marks]** For each vehicle category rented by at least two distinct customers, return the category, number of distinct customers, and average available charge per rental. Count ongoing and unbilled rentals towards the customer requirement, but use only non-NULL charges in the average. Sort by category. A repeated equal charge is still a separate rental charge, not a value to deduplicate.

**(d) [4 marks]** Return customer IDs and names for customers who have never rented an Electric vehicle, including customers who have never rented anything. Use NOT EXISTS.

**(e) [7 marks]** This subpart uses only the following table:

| Payment.pid | amount |
|---|---|
| P1 | NULL |
| P2 | 20 |
| P3 | 20 |
| P4 | NULL |

1. Give the single result row of the following query. **[4 marks]**

   ```sql
   SELECT COUNT(*), COUNT(amount), SUM(amount), AVG(amount)
   FROM Payment;
   ```

2. Give the payment IDs returned below, and justify the result in one sentence. **[2 marks]**

   ```sql
   SELECT pid
   FROM Payment
   WHERE amount NOT IN (
       SELECT amount FROM Payment WHERE pid IN ('P1','P2')
   );
   ```

3. State the truth value of the following expression. **[1 mark]**

   ```sql
   NOT EXISTS (SELECT 1 FROM Payment WHERE amount < 0)
   ```

---

**End of Paper 2 — 100 marks.**

Scope sources: [Teaching plan](../../syllabus/CSC5041_Teaching_Plan.pdf), p. 1 Weeks 1–5 and p. 2 Tutorials 1–2; [Tutorial 1](../../slides/Tutorial1.pdf), p. 1; [Tutorial 2](../../slides/Tutorial%202.pdf), p. 1. Questions, scenarios, data, timings, and mark allocations in this paper are original practice material.
