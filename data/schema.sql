CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE fragrances (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER references users,
    name TEXT,
    designer TEXT,
    nose TEXT,
    description TEXT,
    notes TEXT,
    created_in INTEGER,
    visible INTEGER
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible INTEGER
);

CREATE TABLE designers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible INTEGER
);

CREATE TABLE perfumers (
    id SERIAL PRIMARY KEY,
    name TEXT,
    visible INTEGER
);

CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    name TEXT,
    user_id INTEGER references users,
    favourite_id INTEGER references fragrances,
    fragrance_id INTEGER references fragrances
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    review INTEGER,
    sent_at TIMESTAMP,
    fragrance_id INTEGER references fragrances,
    user_id INTEGER references users,
    comment TEXT
);
