--drop table if exists entries;
create table moz_places (
    id integer,
    url  text,
    title text,
    rev_host text,
    visit_count integer,
    hidden integer,
    typed integer,
    favicon text,
    frecency integer,
    last_visit_date integer,
    guid text,
    foreign_count integer,
    url_hash integer,
    description Null,
    preview_image_url Null
    );
