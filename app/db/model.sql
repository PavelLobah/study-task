create table tasks
( id bigint primary key ,
  name varchar not null,
  description varchar not null,
  created_at timestamp not null
  );


insert into tasks values (1, 'task1', 'description1', '2019-01-01 07:00:00');
insert into tasks values (2, 'task2', 'description2', '2019-01-04 15:00:00');
insert into tasks values (3, 'task3', 'description3', '2019-01-05 23:00:00');
insert into tasks values (4, 'task4', 'description4', '2019-01-08 23:00:00');
insert into tasks values (5, 'task5', 'description5', '2019-01-11 23:00:00');
insert into tasks values (6, 'task6', 'description6', '2019-01-11 22:00:00');
insert into tasks values (7, 'task7', 'description7', '2019-01-11 23:00:00');
insert into tasks values (8, 'task8', 'description8', '2019-01-12 23:00:00');
insert into tasks values (9, 'task9', 'description9', '2019-01-12 23:00:00');

drop table tasks

select * from tasks