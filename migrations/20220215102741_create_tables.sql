-- migrate:up

CREATE TABLE IF NOT EXISTS provider_details (
   provider_details_id INT PRIMARY KEY,
   details json NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
   document_id SERIAL PRIMARY KEY,
   numbers VARCHAR(256),
   expires_at DATE,
   iin VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS passenger (
   passenger_id SERIAL PRIMARY KEY,
   ticket_type VARCHAR(256),
   first_name VARCHAR(256),
   last_name VARCHAR(256),
   date_of_birth DATE,
   citizenship VARCHAR(256),
   document_id INT REFERENCES documents (document_id)
);


CREATE TABLE IF NOT EXISTS booking (
   offer_id VARCHAR(256) PRIMARY KEY,
   phone VARCHAR(256),
   email VARCHAR(256),
   provider_details_id INT REFERENCES provider_details (provider_details_id),
   passenger_id INT REFERENCES passenger (passenger_id)
);

CREATE INDEX index_phone_mail on booking (
   phone,
   email
);

-- migrate:down