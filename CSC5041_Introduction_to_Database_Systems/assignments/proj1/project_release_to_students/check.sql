-- CSC5041 2026 Project 1 Check
--
-- MyDATASET Check
--
-- Load order:  MyDATASET.dump  ->  check.sql  ->  proj1.sql (student)  ->  correct.sql

SET client_min_messages TO WARNING;

-- proj1_table_exists:
-- * checks whether a table with the given name already exists

create or replace function
	proj1_table_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_class
	where relname=tname and relkind='r';
	return (_check = 1);
end;
$$ language plpgsql;

-- proj1_view_exists:
-- * checks whether a view with the given name already exists

create or replace function
	proj1_view_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_class
	where relname=tname and relkind='v';
	return (_check = 1);
end;
$$ language plpgsql;

-- proj1_function_exists:
-- * checks whether a function with the given name already exists

create or replace function
	proj1_function_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_proc
	where proname=tname;
	return (_check > 0);
end;
$$ language plpgsql;

-- proj1_check_result:
-- * determines appropriate message, based on count of
--   excess and missing tuples in user output vs expected output

create or replace function
	proj1_check_result(nexcess integer, nmissing integer) returns text
as $$
begin
	if (nexcess = 0 and nmissing = 0) then
		return 'correct';
	elsif (nexcess > 0 and nmissing = 0) then
		return 'too many result tuples';
	elsif (nexcess = 0 and nmissing > 0) then
		return 'missing result tuples';
	elsif (nexcess > 0 and nmissing > 0) then
		return 'incorrect result tuples';
	end if;
end;
$$ language plpgsql;

-- proj1_check:
-- * compares output of user view/function against expected output
-- * returns string (text message) containing analysis of results

create or replace function
	proj1_check(_type text, _name text, _res text, _query text) returns text
as $$
declare
	nexcess integer;
	nmissing integer;
	excessQ text;
	missingQ text;
begin
	if (_type = 'view' and not proj1_view_exists(_name)) then
		return 'No '||_name||' view; did it load correctly?';
	elsif (_type = 'function' and not proj1_function_exists(_name)) then
		return 'No '||_name||' function; did it load correctly?';
	elsif (not proj1_table_exists(_res)) then
		return _res||': No expected results!';
	else
		excessQ := 'select count(*) '||
				 'from (('||_query||') except '||
				 '(select * from '||_res||')) as X';
		-- raise notice 'Q: %',excessQ;
		execute excessQ into nexcess;
		missingQ := 'select count(*) '||
				 'from ((select * from '||_res||') '||
				 'except ('||_query||')) as X';
		-- raise notice 'Q: %',missingQ;
		execute missingQ into nmissing;
		return proj1_check_result(nexcess,nmissing);
	end if;
	return '???';
end;
$$ language plpgsql;

-- proj1_rescheck:
-- * compares output of user function against expected result
-- * returns string (text message) containing analysis of results

create or replace function
	proj1_rescheck(_type text, _name text, _res text, _query text) returns text
as $$
declare
	_sql text;
	_chk boolean;
begin
	if (_type = 'function' and not proj1_function_exists(_name)) then
		return 'No '||_name||' function; did it load correctly?';
	elsif (_res is null) then
		_sql := 'select ('||_query||') is null';
		-- raise notice 'SQL: %',_sql;
		execute _sql into _chk;
		-- raise notice 'CHK: %',_chk;
	else
		_sql := 'select ('||_query||') = '||quote_literal(_res);
		-- raise notice 'SQL: %',_sql;
		execute _sql into _chk;
		-- raise notice 'CHK: %',_chk;
	end if;
	if (_chk) then
		return 'correct';
	else
		return 'incorrect result';
	end if;
end;
$$ language plpgsql;

-- check_all:
-- * run all of the checks and return a table of results

drop type if exists TestingResult cascade;
create type TestingResult as (test text, result text);

create or replace function
	check_all() returns setof TestingResult
as $$
declare
	i int;
	testQ text;
	result text;
	out TestingResult;
	tests text[] := array['q1', 'q2', 'q3', 'q4', 'q5','q6','q7','q8','q9','q10'];
begin
	for i in array_lower(tests,1) .. array_upper(tests,1)
	loop
		testQ := 'select check_'||tests[i]||'()';
		execute testQ into result;
		out := (tests[i],result);
		return next out;
	end loop;
	return;
end;
$$ language plpgsql;


--
-- Check functions for specific test-cases in Project 1
--

create or replace function check_q1() returns text
as $chk$
	select proj1_check('view', 'q1', 'q1_expected',
	                   $$select * from q1$$)
$chk$ language sql;

create or replace function check_q2() returns text
as $chk$
	select proj1_check('view','q2','q2_expected',
	                   $$select * from q2$$)
$chk$ language sql;

create or replace function check_q3() returns text
as $chk$
	select proj1_check('view','q3','q3_expected',
	                   $$select * from q3$$)
$chk$ language sql;

create or replace function check_q4() returns text
as $chk$
	select proj1_check('view','q4','q4_expected',
	                   $$select * from q4$$)
$chk$ language sql;

create or replace function check_q5() returns text
as $chk$
	select proj1_check('view','q5','q5_expected',
	                   $$select * from q5$$)
$chk$ language sql;

create or replace function check_q6() returns text
as $chk$
	select proj1_check('view','q6','q6_expected',
	                   $$select * from q6$$)
$chk$ language sql;

create or replace function check_q7() returns text
as $chk$
	select proj1_check('view','q7','q7_expected',
	                   $$select * from q7$$)
$chk$ language sql;

create or replace function check_q8() returns text
as $chk$
	select proj1_check('view','q8','q8_expected',
	                   $$select * from q8$$)
$chk$ language sql;

create or replace function check_q9() returns text
as $chk$
	select proj1_check('view','q9','q9_expected',
	                   $$select * from q9$$)
$chk$ language sql;

create or replace function check_q10() returns text
as $chk$
	select proj1_check('view','q10','q10_expected',
	                   $$select * from q10$$)
$chk$ language sql;

--
-- Tables of expected results for test cases
--

drop table if exists q1_expected;
create table q1_expected (
	subject_code character(8)
);

drop table if exists q2_expected;
create table q2_expected (
	course_id integer
);

drop table if exists q3_expected;
create table q3_expected (
	unswid integer, name longname
);

drop table if exists q4_expected;
create table q4_expected (
	facility mediumstring
);

drop table if exists q5_expected;
create table q5_expected (
	name longname, ncourses integer
);

drop table if exists q6_expected;
create table q6_expected (
	school_name longstring, stream_count integer
);

drop table if exists q7_expected;
create table q7_expected (
	subject_code character(8), avg_mark numeric(4,2)
);

drop table if exists q8_expected;
create table q8_expected (
	subject_code character(8), inc_rate numeric
);

drop table if exists q9_expected;
create table q9_expected (
	unsw_id integer, name longname, academic_standing text
);

drop table if exists q10_expected;
create table q10_expected (
	subject_code character(8), year courseyeartype, term character(2), fail_rate numeric
);

--
-- Expected data (computed from the MyDATASET.dump dataset shipped with this project)
--

COPY q1_expected (subject_code) FROM stdin;
COMP8505
COMP8506
COMP8509
COMP8512
COMP8514
COMP8518
COMP8530
COMP8542
COMP8548
COMP8560
COMP8572
COMP8612
COMP8618
COMP8624
COMP9945
COMP8522
COMP9912
COMP8524
\.

COPY q2_expected (course_id) FROM stdin;
68619
70427
\.

COPY q3_expected (unswid, name) FROM stdin;
3115148	Andrew Jackson
9466637	Betty Wong
6882728	Diane Enahoro
3178237	Sehne Avsar
7676135	Trevor Stegman
9995228	Peter Nichols
3129186	Abu Shonchoy
8085382	Louise Zieme
3218828	Hugh Bainbridge
3217878	Devorah Wainer
3150458	Quan Gan
3389919	Denise Bunting
9857057	Raymond Durham
8421419	Chung-Sok Suh
3227548	Elaine Franco
3281877	Vasile Caprar
9026074	David Morgan
3247239	Vincent Wong
9643409	Suk-Joong Kim
9985688	Pradeep Ray
3128697	Zahid Riaz
8553813	Donna Wilcox
3021175	Yue Wang
9130234	Barbara Hendrischke
8997961	Kenneth Ashwell
9854333	Denzil Fiebig
8837004	Tien Nguyen
8831950	Diane Fieldes
9213794	Tracy Wilcox
3266526	Simon Restubog
3210320	Suzanne Chan-Serafin
3089715	Louis Wang
3344027	Jennifer Foster
3149611	Edward Harbor
8545418	Judith Watson
6987539	Ian Wilkinson
9155962	Noor-E-Alam Ahmed
3307694	Ricardo Flores
3228131	Ben Greiner
3138847	Benoit Julien
3382677	Chen Qiu
\.

COPY q4_expected (facility) FROM stdin;
Document camera
Hearing loop
Neck microphone
Slide projector
Fan ventilation
Whiteboard
\.

COPY q5_expected (name, ncourses) FROM stdin;
Susan Hagon	248
\.

COPY q6_expected (school_name, stream_count) FROM stdin;
School of Economics	57
School of Education	127
School of the Arts and Media	108
School of Public Health & Community Medicine	54
School of International Studies	111
School of Humanities and Languages	83
School of Social Sciences	92
School of Biological, Earth and Environmental Sciences	111
\.

COPY q7_expected (subject_code, avg_mark) FROM stdin;
COMP9020	60.04
COMP9021	55.39
COMP9024	59.20
COMP9101	62.07
COMP9317	76.17
COMP9331	55.35
COMP9414	68.75
COMP9441	76.58
GSOE9210	66.17
\.

COPY q8_expected (subject_code, inc_rate) FROM stdin;
ACCT3610	0.1984
\.

COPY q9_expected (unsw_id, name, academic_standing) FROM stdin;
3135602	Shirley Caws	Good
3138484	Sean Turle	Good
3138391	Damchu Tenzin	Good
3136192	Blake Croll	Good
3137680	Benny Mok	Good
3137600	Frances Sangster	Good
3132013	Kathleen MacLaine	Good
3137261	Kabbara Reda	Good
3138159	Robert Neo	Good
3137694	Paul Tench	Referral
3137415	Derek Tejwani	Good
3135986	Hui Goh	Good
3133614	Olivia Tyng	Referral
3134640	Steve Seelin	Good
3139955	Margarita Kaplinovsky	Good
3132152	Kwok Low	Good
3139033	Alberto Hofbrucker	Referral
3133527	Frederik Murtada	Good
3138713	Selby Wilheim	Good
3133650	Jen Paramananthakarasu	Probation
3138579	Toby Le Pavoux	Good
3132330	Lauren Makin	Good
3138174	Kaylin Doughty	Good
3134788	Michelle Flower	Good
3130445	Corey O'Loughlan	Referral
3132948	Joseph Nik Mohd Zamri	Good
3137927	Torunn Kotze	Good
3132145	Rosemary Morisset	Good
3134072	Hamish Flick	Good
3132540	Jin-Oh Paick	Good
3132483	Shannelle Sijabat	Good
3133285	Lian Ogilvie	Good
3134514	Christine Jaschuk	Good
3133828	Victor Efendi	Good
3132054	Shannon Phipps	Good
3137205	Wing Sam	Good
\.

COPY q10_expected (subject_code, year, term, fail_rate) FROM stdin;
COMP1911	2011	S1	0.1212
COMP1917	2012	S1	0.1030
COMP1927	2012	S2	0.1812
\.
