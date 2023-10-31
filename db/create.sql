CREATE DATABASE web_dev;

\c web_dev;

create table tasks
( issue_id SERIAL PRIMARY KEY,
  name varchar not null,
  description varchar null,
  created_at timestamp not null DEFAULT NOW()
  );
