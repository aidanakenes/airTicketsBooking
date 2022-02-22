-- migrate:up

CREATE TABLE IF NOT EXISTS offer_details (
    offer_details_id SERIAL PRIMARY KEY,
    details json NOT NULL
);

-- migrate:down
