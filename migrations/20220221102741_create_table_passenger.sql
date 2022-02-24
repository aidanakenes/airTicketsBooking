-- migrate:up

CREATE TABLE IF NOT EXISTS passenger (
    passenger_id SERIAL PRIMARY KEY,
    ticket_type VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    citizenship VARCHAR(4),
    numbers VARCHAR(10),
    expires_at DATE,
    iin VARCHAR(16)

);

-- migrate:down

DROP TABLE IF EXISTS passenger CASCADE;