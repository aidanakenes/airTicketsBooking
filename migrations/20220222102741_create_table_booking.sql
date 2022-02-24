-- migrate:up

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
