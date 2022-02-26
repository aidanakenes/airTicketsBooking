-- migrate:up

CREATE TABLE IF NOT EXISTS passenger (
    passenger_id SERIAL PRIMARY KEY,
    details json NOT NULL
);

-- migrate:down

DROP TABLE IF EXISTS passenger CASCADE;