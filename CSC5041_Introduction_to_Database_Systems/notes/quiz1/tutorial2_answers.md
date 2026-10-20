# Tutorial 2 — Compact Answers

[Question sheet](../../slides/Tutorial%202.pdf), p. 1, Q1(a)–(b). Model answers, not an official marking scheme.

```text
S = Student     C = Course     E = Enrolled
I = Instructor  T = Teaches
⋈ = natural join; γ = grouping/aggregation; ← = intermediate relation.
```

## Q1(a) Relational algebra

### (i)

```text
π_{title}(σ_{dept='CS' ∧ credits>3}(C))
```

### (ii)

```text
π_{sname}(S ⋈ E ⋈ σ_{iid='I1'}(T))
```

`E ⋈ T` matches both cid and term.

### (iii)

```text
A ← π_{sid}(E ⋈ σ_{dept='CS'}(C))
B ← π_{sid}(E ⋈ σ_{dept='Math'}(C))

OR:    π_{sname}(S ⋈ (A ∪ B))
BOTH:  π_{sname}(S ⋈ (A ∩ B))
```

### (iv)

```text
π_{sname}(S ⋈ (π_{sid}(S) − π_{sid}(E)))
```

### (v)

```text
D ← π_{cid}(σ_{dept='CS'}(C))
R ← π_{sid,cid}(E)
U ← π_{sid}(S)

Q ← U − π_{sid}((U × D) − R)
Answer ← π_{sname}(S ⋈ Q)
```

If D ≠ ∅: `Q = U ∩ (R ÷ D)`. If D = ∅: `Q = U`.

### (vi)

```text
γ_{dept; COUNT(cid)→nCourses, AVG(credits)→avgCredits}(C)
```

## Q1(b) SQL

### (i)

```sql
SELECT sname, level
FROM Student
WHERE major IN ('CS', 'Math');
```

### (ii)

```sql
SELECT s.sname, c.title, e.term
FROM Enrolled AS e
JOIN Student AS s ON s.sid = e.sid
JOIN Course AS c ON c.cid = e.cid;
```

### (iii)

```sql
SELECT DISTINCT c.title
FROM Course AS c
JOIN Teaches AS t ON t.cid = c.cid
WHERE t.iid = 'I1';
```

### (iv)

```sql
SELECT DISTINCT sid
FROM Enrolled
WHERE grade IS NULL;
```

`NULL <> 'A'` is UNKNOWN, so WHERE does not retain those rows.

---

Sources: Tutorial 2.pdf p. 1; [Relational_Algebra.pptx](../../slides/Relational_Algebra.pptx), slides 5–59; [SQLpart1.pptx](../../slides/SQLpart1.pptx), slides 13, 31–36, 44–58. Question-sheet SHA-256: `72c016526c1c0ff02c10fcb5f7f964c1184999c684228671025800936a6cabac`. Expressions/queries are statically derived; SQL has not been executed.
