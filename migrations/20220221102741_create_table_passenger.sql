-- migrate:up

CREATE TABLE IF NOT EXISTS passenger (
    passenger_id SERIAL PRIMARY KEY,
    info json NOT NULL
);

-- migrate:down

DROP TABLE IF EXISTS passenger CASCADE;