-- migrate:up

CREATE TABLE IF NOT EXISTS booking (
    uid SERIAL PRIMARY KEY,
    booking_id uuid,
    phone VARCHAR(12),
    email VARCHAR(100),
    created_at TIMESTAMP,
    passengers json NOT NULL,
    offer_details_id INT REFERENCES offer_details (offer_details_id)
);

CREATE INDEX index_phone_mail on booking (
    phone,
    email
);

-- migrate:down

DROP TABLE IF EXISTS booking;