--drop table if exists entries;
create table HISTORY (
    rec_id integer,
    id integer,
    url  text,
    title text,
    visit_count integer,
    last_visit integer,
    last_visit_readable text,
    );
