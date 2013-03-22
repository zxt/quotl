drop table if exists quotes;
create table quotes (
  id integer primary key autoincrement,
  quote text not null,
  author text not null
);
