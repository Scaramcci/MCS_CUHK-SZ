-- CSC5041 2026 Project 1
-- MyDATASET: self-contained plain SQL views.

-- Q1: Subjects offered directly by CSE.
create or replace view Q1(subject_code)
as
select distinct s.code
from subjects as s
join orgunits as o on o.id = s.offeredby
where o.longname = 'School of Computer Science and Engineering'
  and s.career = 'PG'
  and s.uoc > 6;

-- Q2: Several rooms in the same building count as one building.
create or replace view Q2(course_id)
as
select c.id
from courses as c
join classes as cl on cl.course = c.id
join class_types as ct on ct.id = cl.ctype
join rooms as r on r.id = cl.room
where ct.name = 'Studio'
group by c.id
having count(distinct r.building) >= 3;

-- Q3: A staff member is returned once even after multiple teaching paths.
create or replace view Q3(unswid, name)
as
select distinct teacher.unswid, teacher.name
from people as teacher
join course_staff as cs on cs.staff = teacher.id
join course_enrolments as ce on ce.course = cs.course
join people as student on student.id = ce.student
where student.name = 'Hemma Margareta';

-- Q4: Start with all facilities, including those installed in no room.
create or replace view Q4(facility)
as
select distinct f.description
from facilities as f
where not exists (
    select 1
    from room_facilities as rf
    join rooms as r on r.id = rf.room
    join buildings as b on b.id = r.building
    where rf.facility = f.id
      and b.campus = 'K'
      and b.gridref like 'C%'
);

-- Q5: Group by staff identity; preserve everyone tied for first place.
create or replace view Q5(name, ncourses)
as
with lic_counts as (
    select cs.staff, count(distinct cs.course)::integer as ncourses
    from course_staff as cs
    join staff_roles as sr on sr.id = cs.role
    where sr.name = 'Course Convenor'
    group by cs.staff
)
select p.name, lc.ncourses
from lic_counts as lc
join people as p on p.id = lc.staff
where lc.ncourses = (select max(ncourses) from lic_counts);

-- Q6: Only direct offerings count; a school with no streams has count zero.
create or replace view Q6(school_name, stream_count)
as
with school_counts as (
    select o.id, o.longname, count(s.id)::integer as stream_count
    from orgunits as o
    join orgunit_types as ot on ot.id = o.utype
    left join streams as s on s.offeredby = o.id
    where ot.name = 'School'
    group by o.id, o.longname
)
select sc.longname, sc.stream_count
from school_counts as sc
where sc.stream_count > (
    select coalesce(sum(cse.stream_count), 0)
    from school_counts as cse
    where cse.longname = 'School of Computer Science and Engineering'
);

-- Q7: NULL marks contribute zero and still count toward enrolment.
create or replace view Q7(subject_code, avg_mark)
as
select s.code, avg(coalesce(ce.mark, 0))::numeric(4,2)
from subjects as s
join orgunits as o on o.id = s.offeredby
join courses as c on c.subject = s.id
join semesters as sem on sem.id = c.semester
join course_enrolments as ce on ce.course = c.id
where o.longname = 'School of Computer Science and Engineering'
  and s.career = 'PG'
  and sem.year = 2010
  and sem.term = 'S1'
group by c.id, s.code
having count(*) > 10;

-- Q8: Compare unrounded relative increases, then round the winning values.
create or replace view Q8(subject_code, inc_rate)
as
with semester_means as (
    select s.code,
           avg(ce.mark) filter (where sem.term = 'S1') as s1_mean,
           avg(ce.mark) filter (where sem.term = 'S2') as s2_mean
    from subjects as s
    join orgunits as o on o.id = s.offeredby
    join courses as c on c.subject = s.id
    join semesters as sem on sem.id = c.semester
    join course_enrolments as ce on ce.course = c.id
    where o.longname in ('School of Chemistry', 'School of Accounting')
      and sem.year = 2008
      and sem.term in ('S1', 'S2')
      and ce.mark is not null
    group by s.code
), increases as (
    select code, (s2_mean - s1_mean) / nullif(s1_mean, 0) as rate
    from semester_means
    where s1_mean is not null and s2_mean is not null
)
select code, round(rate, 4)
from increases
where rate = (select max(rate) from increases);

-- Q9: Only marked courses enter either count; one failed course is Referral.
create or replace view Q9(unsw_id, name, academic_standing)
as
select p.unswid, p.name,
       case
           when count(*) > 1 and count(*) filter (where ce.mark >= 50) = 0
               then 'Probation'
           when 2 * count(*) filter (where ce.mark >= 50) <= count(*)
               then 'Referral'
           else 'Good'
       end
from people as p
join course_enrolments as ce on ce.student = p.id
join courses as c on c.id = ce.course
join semesters as sem on sem.id = c.semester
where p.unswid::text like '313%'
  and sem.year = 2012
  and sem.term = 'S1'
  and ce.mark is not null
group by p.id, p.unswid, p.name;

-- Q10: Rank offerings by enrolment, including NULL marks; retain tied terms.
create or replace view Q10(subject_code, year, term, fail_rate)
as
with course_counts as (
    select c.id, s.code, sem.year, sem.term,
           count(*) as enrolled,
           count(ce.mark) as marked,
           count(*) filter (where ce.mark < 50) as failed
    from subjects as s
    join courses as c on c.subject = s.id
    join semesters as sem on sem.id = c.semester
    join course_enrolments as ce on ce.course = c.id
    where s.code like 'COMP%'
    group by c.id, s.code, sem.year, sem.term
    having count(*) > 150
), ranked_courses as (
    select code, year, term, marked, failed,
           rank() over (partition by code order by enrolled desc) as enrolment_rank
    from course_counts
)
select code, year, term, round(failed::numeric / nullif(marked, 0), 4)
from ranked_courses
where enrolment_rank = 1;
