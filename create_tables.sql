
-- Creating Variables table
CREATE TABLE IF NOT EXISTS public."Variables" (
    id serial PRIMARY KEY,
    name varchar(255) NOT NULL
);

-- Creating Measurements table
CREATE TABLE IF NOT EXISTS public."Measurements" (
    id serial PRIMARY KEY,
    time_point integer NOT NULL,
    timestamp_id integer,
    FOREIGN KEY (timestamp_id)
        REFERENCES public.timestamps (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

-- Creating Measurement_Values table
CREATE TABLE IF NOT EXISTS public."Measurement_Values" (
    id serial PRIMARY KEY,
    measurement_id integer,
    variable_id integer
    value_id integer,
    etl_date date,
    FOREIGN KEY (measurement_id)
        REFERENCES public."Measurements" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    FOREIGN KEY (variable_id)
        REFERENCES public."Variables" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    FOREIGN KEY (value_id)
        REFERENCES public."values" (id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

-- Creating timestamps table
CREATE TABLE IF NOT EXISTS public.timestamps (
    id serial PRIMARY KEY,
    "timestamp" timestamp without time zone NOT NULL
);

-- Creating values table
CREATE TABLE IF NOT EXISTS public."values" (
    id serial PRIMARY KEY,
    value double precision NOT NULL
);

COMMIT;
