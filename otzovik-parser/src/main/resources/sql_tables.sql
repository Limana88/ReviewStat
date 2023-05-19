CREATE TABLE review (
                        id serial primary key,
                        create_date timestamp,
                        source_name varchar,
                        title varchar,
                        description text,
                        date varchar,
                        rate int,
                        company_id bigint references company(id)
);

create table company (
                         id serial primary key,
                         create_date timestamp,
                         name varchar,
                         url varchar
);
