-- migrate:up

CREATE TABLE IF NOT EXISTS offer_details (
    offer_details_id SERIAL PRIMARY KEY,
    details json NOT NULL
);

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


CREATE TABLE IF NOT EXISTS booking (
    offer_id VARCHAR(256) PRIMARY KEY,
    phone VARCHAR(256),
    email VARCHAR(256),
    offer_details_id INT REFERENCES offer_details (offer_details_id),
    passenger_id INT REFERENCES passenger (passenger_id)
);

CREATE INDEX index_phone_mail on booking (
    phone,
    email
);

-- migrate:down
