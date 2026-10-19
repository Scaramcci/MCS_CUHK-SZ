-- Table of data about bars
-- e.g. ('Australia Hotel','The Rocks',123456)
create table Bars (
	Name        varchar(30),
	Addr        varchar(30),
	License     integer,
	primary key (License)
);

insert into Bars values ('Australia Hotel','The Rocks',123456);
insert into Bars values ('Coogee Bay Hotel','Coogee',966500);
insert into Bars values ('Lord Nelson','The Rocks',123888);
insert into Bars values ('Marble Bar','Sydney',122123);
insert into Bars values ('Regent Hotel','Kingsford',987654);
insert into Bars values ('Adam','Randwick',938500);



-- Table of data about drinkers
-- e.g. ('Adam','Randwick','9385-4444')

create table Drinkers (
	Name        varchar(30),
    Addr        varchar(30),
	Phone       varchar(10) check (Phone like '____-____'),
	primary key (Phone)
);

insert into Drinkers values ('Adam','Randwick','9385-4444');
insert into Drinkers values ('Gernot','Newtown','9415-3378');
insert into Drinkers values ('John','Clovelly','9665-1234');
insert into Drinkers values ('Justin','Mosman','9845-4321');



-- Table of data about beers
-- e.g. ('COMP3311','Database Systems','jas',340)

create table Beers (
	Name        varchar(50),
	Manf        varchar(50),
	primary key (Name)
);

insert into Beers values ('80/-','Caledonian');
insert into Beers values ('Bigfoot Barley Wine','Sierra Nevada');
insert into Beers values ('Burragorang Bock','George IV Inn');
insert into Beers values ('Crown Lager','Carlton');
insert into Beers values ('Fosters Lager','Carlton');
insert into Beers values ('Invalid Stout','Carlton');
insert into Beers values ('Melbourne Bitter','Carlton');
insert into Beers values ('New','Toohey''s');
insert into Beers values ('Old','Toohey''s');
insert into Beers values ('Old Admiral','Lord Nelson');
insert into Beers values ('Pale Ale','Sierra Nevada');
insert into Beers values ('Prenium Lager','Cascade');
insert into Beers values ('Red','Toohey''s');
insert into Beers values ('Sheaf Stout','Toohey''s');
insert into Beers values ('Sparkling Ale','Cooper''s');
insert into Beers values ('Stout','Cooper''s');
insert into Beers values ('Three Sheets','Lord Nelson');
insert into Beers values ('Victoria Bitter','Carlton');


create table Frequents (
	Drinker     varchar(10),
	Bar         varchar(30)
);

create table Likes (
	Drinker     varchar(10),
	Beer        varchar(30)
);

create table Sells (
	Bar         varchar(30),
	Beer        varchar(30),
    Price       float
);

INSERT INTO Frequents (Drinker, Bar)
VALUES
    ('Adam', 'Coogee Bay Hotel'),
    ('Gernot', 'Lord Nelson'),
    ('John', 'Coogee Bay Hotel'),
    ('John', 'Lord Nelson'),
    ('John', 'Australia Hotel'),
    ('Justin', 'Regent Hotel'),
    ('Justin', 'Marble Bar');

INSERT INTO Likes (Drinker, Beer)
VALUES
    ('Adam', 'Crown Lager'),
    ('Adam', 'Fosters Lager'),
    ('Adam', 'New'),
    ('Gernot', 'Premium Lager'),
    ('Gernot', 'Sparkling Ale'),
    ('John', '80/-'),
    ('John', 'Bigfoot Barley Wine'),
    ('John', 'Pale Ale'),
    ('John', 'Three Sheets'),
    ('Justin', 'Sparkling Ale'),
    ('Justin', 'Victoria Bitter');

INSERT INTO Sells (Bar, Beer, Price)
VALUES
    ('Australia Hotel', 'Burragorang Bock', 3.5),
    ('Coogee Bay Hotel', 'New', 2.25),
    ('Coogee Bay Hotel', 'Old', 2.5),
    ('Coogee Bay Hotel', 'Sparkling Ale', 2.8),
    ('Coogee Bay Hotel', 'Victoria Bitter', 2.3),
    ('Lord Nelson', 'Three Sheets', 3.75),
    ('Lord Nelson', 'Old Admiral', 3.75),
    ('Marble Bar', 'New', 2.8),
    ('Marble Bar', 'Old', 2.8),
    ('Marble Bar', 'Victoria Bitter', 2.8),
    ('Regent Hotel', 'New', 2.2),
    ('Regent Hotel', 'Victoria Bitter', 2.2),
    ('Royal Hotel', 'New', 2.3),
    ('Royal Hotel', 'Old', 2.3),
    ('Royal Hotel', 'Victoria Bitter', 2.3);




