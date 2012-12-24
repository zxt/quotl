drop table if exists quotes;
create table quotes (
  id integer primary key autoincrement,
  quote string not null,
  author string not null
);
