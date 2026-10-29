-- Independent synthetic fixture generator, TEST ONLY, never assignment data.
-- Runs within transaction on verifier-only DB; all changes rolled back.
\set ON_ERROR_STOP on
SET statement_timeout='120s';
BEGIN;
SELECT 'TRUNCATE '||string_agg(format('%I.%I',schemaname,tablename),',')||' CASCADE;' FROM pg_tables WHERE schemaname='public' \gexec
CREATE FUNCTION pg_temp.assert_rows(label text, actual text, expected text) RETURNS void LANGUAGE plpgsql AS $$
DECLARE n integer;
BEGIN
 EXECUTE 'SELECT count(*) FROM (('||actual||' EXCEPT ALL '||expected||') UNION ALL ('||expected||' EXCEPT ALL '||actual||')) x' INTO n;
 IF n<>0 THEN RAISE EXCEPTION 'FAIL % difference %',label,n; END IF;
 RAISE NOTICE 'PASS %',label;
END $$;
INSERT INTO orgunit_types(id,name) VALUES (1,'School'),(2,'Faculty');
INSERT INTO orgunits(id,utype,name,longname) VALUES
(1,1,'CSE','School of Computer Science and Engineering'),(2,1,'Chem','School of Chemistry'),(3,1,'Acc','School of Accounting'),(4,2,'Other','Faculty'),(5,1,'Sub','Subschool');
INSERT INTO orgunit_groups VALUES (1,5);
INSERT INTO subjects(id,code,name,uoc,career,offeredby) VALUES
(1,'TEST0001','Test',7,'PG',1),(2,'TEST0002','Test',6,'PG',1),(3,'TEST0003','Test',7,'UG',1),(4,'TEST0004','Test',7,'PG',5),(5,'TEST0001','Version',7,'PG',1);
SELECT pg_temp.assert_rows('Q1 direct PG >6 and duplicate codes','SELECT * FROM q1',$$VALUES ('TEST0001')$$);
INSERT INTO semesters(id,unswid,year,term,name,longname,starting,ending) VALUES
(1,1,2010,'S1','Test','Test','2010-01-01','2010-06-01'),(2,2,2008,'S1','Test','Test','2008-01-01','2008-06-01'),(3,3,2008,'S2','Test','Test','2008-07-01','2008-12-01'),(4,4,2012,'S1','Test','Test','2012-01-01','2012-06-01'),(5,5,2012,'S2','Test','Test','2012-07-01','2012-12-01');
INSERT INTO courses(id,subject,semester) VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,1,4),(7,2,4),(8,3,4),(9,4,5);
INSERT INTO buildings(id,unswid,name,campus,gridref) VALUES (1,'B1','B1','K','C1'),(2,'B2','B2','P','C2'),(3,'B3','B3','K','D1'),(4,'B4','B4','K',NULL);
INSERT INTO rooms(id,unswid,name,building) VALUES (1,'R1','R1',1),(2,'R2','R2',1),(3,'R3','R3',2),(4,'R4','R4',3),(5,'R5','R5',4);
INSERT INTO class_types(id,unswid,name) VALUES (1,'STU','Studio'),(2,'LEC','Lecture');
INSERT INTO classes(id,course,room,ctype,dayofwk,starttime,endtime,startdate,enddate)
SELECT row_number()over(),v.*,1,9,10,'2010-01-01'::date,'2010-06-01'::date FROM (VALUES(1,1,1),(1,2,1),(1,3,1),(1,4,1),(2,1,1),(2,2,1),(2,3,1),(2,4,2))v(c,r,t);
SELECT pg_temp.assert_rows('Q2 three DISTINCT Studio buildings','SELECT * FROM q2','VALUES (1)');
INSERT INTO people(id,unswid,password,given,sortname,name,email)
SELECT i,4000000+i,'TEST_ONLY','Synthetic','Synthetic','Synthetic','test@example.invalid' FROM generate_series(1,1100)i;
INSERT INTO students(id) SELECT id FROM people;
UPDATE people SET name='Hemma Margareta' WHERE id=1;
INSERT INTO people(id,unswid,password,given,sortname,name,email) VALUES (2001,9001,'TEST_ONLY','Same','Same','Same','test@example.invalid'),(2002,9002,'TEST_ONLY','Same','Same','Same','test@example.invalid'),(2003,9003,'TEST_ONLY','Other','Other','Other','test@example.invalid');
INSERT INTO staff(id,employed) VALUES(2001,'2000-01-01'),(2002,'2000-01-01'),(2003,'2000-01-01');
INSERT INTO staff_roles(id,name) VALUES(1,'Course Convenor'),(2,'Tutor'),(3,'Course Convenor');
INSERT INTO course_staff VALUES(1,2001,1),(1,2001,2),(1,2001,3),(2,2001,1),(1,2002,1),(2,2002,1),(1,2003,2);
INSERT INTO course_enrolments(student,course,mark) VALUES(1,1,50),(1,2,50);
SELECT pg_temp.assert_rows('Q3 multiple paths deduplicated','SELECT * FROM q3',$$VALUES (9001,'Same'),(9002,'Same'),(9003,'Other')$$);
SELECT pg_temp.assert_rows('Q5 ties distinct courses same display names multiplicity','SELECT * FROM q5',$$VALUES ('Same',2),('Same',2)$$);
INSERT INTO facilities VALUES(1,'Target'),(2,'Elsewhere'),(3,'Nowhere'),(4,'NullGrid');
INSERT INTO room_facilities VALUES(1,1),(3,1),(3,2),(4,2),(5,4);
SELECT pg_temp.assert_rows('Q4 anti-join campus grid never installed','SELECT * FROM q4',$$VALUES('Elsewhere'),('Nowhere'),('NullGrid')$$);
INSERT INTO streams(id,code,name,offeredby) VALUES(1,'AA0001','Test',1),(2,'AA0002','Test',2),(3,'AA0003','Test',2),(4,'AA0004','Test',3),(5,'AA0005','Test',4),(6,'AA0006','Test',4),(7,'AA0007','Test',5);
SELECT pg_temp.assert_rows('Q6 strict school direct stream count','SELECT * FROM q6',$$VALUES('School of Chemistry',2)$$);
DELETE FROM streams WHERE offeredby=1;
SELECT pg_temp.assert_rows('Q6 zero stream CSE','SELECT * FROM q6',$$VALUES('School of Chemistry',2),('School of Accounting',1),('Subschool',1)$$);
DELETE FROM course_enrolments;
INSERT INTO course_enrolments(student,course,mark) SELECT i,1,CASE WHEN i=11 THEN NULL ELSE 55 END FROM generate_series(1,11)i;
INSERT INTO course_enrolments(student,course,mark) SELECT i,2,80 FROM generate_series(1,10)i;
INSERT INTO course_enrolments(student,course,mark) SELECT i,5,60 FROM generate_series(1,11)i;
SELECT pg_temp.assert_rows('Q7 >10 NULL as zero courses separate same-code versions','SELECT * FROM q7',$$VALUES('TEST0001',50.00::numeric),('TEST0001',60.00::numeric)$$);
-- Q8 two exact ties, and a strictly inferior increase that rounds identically.
INSERT INTO subjects(id,code,name,offeredby) VALUES(10,'CHEM0001','Test',2),(11,'ACCT0001','Test',3),(12,'CHEM0002','Test',2),(13,'CHEM0003','Zero base',2),(14,'CHEM0004','No S2 marks',2);
INSERT INTO courses(id,subject,semester) SELECT 100+s.id*2+t,s.id,t FROM subjects s CROSS JOIN generate_series(2,3)t WHERE s.id BETWEEN 10 AND 14;
INSERT INTO course_enrolments(student,course,mark)
SELECT i,c.id,CASE WHEN c.subject=13 THEN 0 WHEN c.subject=14 AND c.semester=3 THEN NULL WHEN c.subject IN(10,11) AND c.semester=3 AND i=1 THEN 51 ELSE 50 END FROM courses c CROSS JOIN generate_series(1,1001)i WHERE c.subject BETWEEN 10 AND 14;
SELECT pg_temp.assert_rows('Q8 exact ranking prior rounding ties NULL zero baseline','SELECT * FROM q8',$$VALUES('CHEM0001',0.0000::numeric),('ACCT0001',0.0000::numeric)$$);
-- Q9 all branches, 50 pass boundary, all-null exclusion, wrong term and prefix.
UPDATE people SET unswid=3130000+id WHERE id BETWEEN 1 AND 7;
INSERT INTO course_enrolments(student,course,mark) VALUES (1,6,49),(2,6,50),(3,6,49),(3,7,0),(4,6,50),(4,7,49),(5,6,50),(5,7,50),(5,8,49),(6,6,NULL),(7,6,50),(7,7,NULL),(8,6,90),(1,9,90);
SELECT pg_temp.assert_rows('Q9 complete branches and exclusions','SELECT * FROM q9',$$VALUES(3130001,'Hemma Margareta','Referral'),(3130002,'Synthetic','Good'),(3130003,'Synthetic','Probation'),(3130004,'Synthetic','Referral'),(3130005,'Synthetic','Good'),(3130007,'Synthetic','Good')$$);
-- Q10 exact >150, tied offerings across subject versions, NULL enrolments included.
INSERT INTO subjects(id,code,name,offeredby) VALUES(20,'COMP0001','Old',1),(21,'COMP0001','New',1),(22,'COMP0002','150 only',1),(23,'COMP0003','No marks',1),(24,'TEST0010','Not COMP',1);
INSERT INTO courses(id,subject,semester) VALUES(201,20,2),(202,20,3),(203,21,1),(204,22,1),(205,23,1),(206,24,1);
INSERT INTO course_enrolments(student,course,mark) SELECT i,201,0 FROM generate_series(1,151)i;
INSERT INTO course_enrolments(student,course,mark) SELECT i,202,CASE WHEN i<=50 THEN 49 WHEN i<=100 THEN 50 ELSE NULL END FROM generate_series(1,152)i;
INSERT INTO course_enrolments(student,course,mark) SELECT i,203,50 FROM generate_series(1,152)i;
INSERT INTO course_enrolments(student,course,mark) SELECT i,204,49 FROM generate_series(1,150)i;
INSERT INTO course_enrolments(student,course,mark) SELECT i,205,NULL FROM generate_series(1,151)i;
INSERT INTO course_enrolments(student,course,mark) SELECT i,206,49 FROM generate_series(1,152)i;
SELECT pg_temp.assert_rows('Q10 max ties threshold null enrolments fail denominator versions','SELECT * FROM q10',$$VALUES('COMP0001',2008,'S2',0.5000::numeric),('COMP0001',2010,'S1',0.0000::numeric),('COMP0003',2010,'S1',NULL::numeric)$$);
-- Reproduce mandated Q7 type limitation rather than silently ignoring it.
UPDATE course_enrolments SET mark=100 WHERE course=1;
DO $$ BEGIN
 PERFORM * FROM q7;
 RAISE EXCEPTION 'Expected numeric overflow absent';
EXCEPTION WHEN numeric_value_out_of_range THEN RAISE NOTICE 'CONFIRMED Q7 numeric(4,2) cannot hold 100.00'; END $$;
ROLLBACK;
