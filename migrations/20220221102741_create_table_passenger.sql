-- migrate:up

CREATE TABLE IF NOT EXISTS passenger (
    passenger_id SERIAL PRIMARY KEY,
    ticket_type VARCHAR(256),
    first_name VARCHAR(256),
    last_name VARCHAR(256),
    date_of_birth DATE,
    citizenship VARCHAR(256),
    numbers VARCHAR(256),
    expires_at DATE,
    iin VARCHAR(256)

);

-- migrate:down

DROP TABLE IF EXISTS passenger CASCADE;